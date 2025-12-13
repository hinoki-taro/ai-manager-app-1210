"""
Google Drive サービスアカウント連携モジュール

WEBデプロイ用に、サービスアカウント認証を使用したGoogle Drive連携を提供します。
OAuth 2.0ではなく、サービスアカウントキーを使用するため、
ユーザーのログインなしで自動的にGoogle Driveにアクセスできます。
"""

import os
import io
import json
import streamlit as st
from typing import Optional, List, Dict, Any

# Google Drive API
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    from google.oauth2 import service_account
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False


class GoogleDriveServiceAccount:
    """Google Driveサービスアカウント管理クラス"""
    
    # APIスコープ
    SCOPES = [
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/drive.metadata.readonly'
    ]
    
    def __init__(self):
        """初期化"""
        self.service = None
        self.authenticated = False
        self.service_account_email = None
        
        if not GOOGLE_DRIVE_AVAILABLE:
            st.error("Google Drive APIライブラリが必要です")
            return
        
        # 認証を試行
        self._authenticate()
    
    def _authenticate(self):
        """サービスアカウントで認証"""
        try:
            # Streamlit Secretsから認証情報を取得
            if "google_drive_service_account" in st.secrets:
                service_account_info = dict(st.secrets["google_drive_service_account"])
                
                # 認証情報を作成
                credentials = service_account.Credentials.from_service_account_info(
                    service_account_info,
                    scopes=self.SCOPES
                )
                
                # Drive APIサービスを構築
                self.service = build('drive', 'v3', credentials=credentials)
                self.authenticated = True
                self.service_account_email = service_account_info.get('client_email', 'Unknown')
                
                st.success(f"✓ Google Driveに接続しました")
                st.info(f"サービスアカウント: {self.service_account_email}")
            
            else:
                # 環境変数から取得を試みる
                service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
                
                if service_account_json:
                    service_account_info = json.loads(service_account_json)
                    
                    credentials = service_account.Credentials.from_service_account_info(
                        service_account_info,
                        scopes=self.SCOPES
                    )
                    
                    self.service = build('drive', 'v3', credentials=credentials)
                    self.authenticated = True
                    self.service_account_email = service_account_info.get('client_email', 'Unknown')
                
                else:
                    st.warning("""
                    Google Driveサービスアカウントが設定されていません。
                    
                    **Streamlit Community Cloudでの設定:**
                    1. Settings → Secrets
                    2. サービスアカウントJSONの内容を追加
                    
                    詳細: WEB_DEPLOYMENT_WITH_GOOGLE_DRIVE.md
                    """)
        
        except Exception as e:
            st.error(f"Google Drive認証に失敗: {str(e)}")
    
    def is_authenticated(self) -> bool:
        """認証状態を確認"""
        return self.authenticated and self.service is not None
    
    def list_folders(self, parent_folder_id: str = None) -> List[Dict[str, Any]]:
        """
        フォルダ一覧を取得
        
        Args:
            parent_folder_id: 親フォルダID
        
        Returns:
            フォルダ情報のリスト
        """
        if not self.is_authenticated():
            st.error("Google Driveに認証されていません")
            return []
        
        try:
            query = "mimeType='application/vnd.google-apps.folder'"
            
            if parent_folder_id:
                query += f" and '{parent_folder_id}' in parents"
            
            query += " and trashed=false"
            
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, modifiedTime, webViewLink)"
            ).execute()
            
            folders = results.get('files', [])
            return folders
        
        except Exception as e:
            st.error(f"フォルダ一覧の取得に失敗: {str(e)}")
            return []
    
    def list_files(self, folder_id: str = None, file_types: List[str] = None) -> List[Dict[str, Any]]:
        """
        ファイル一覧を取得
        
        Args:
            folder_id: フォルダID
            file_types: ファイル形式のリスト
        
        Returns:
            ファイル情報のリスト
        """
        if not self.is_authenticated():
            st.error("Google Driveに認証されていません")
            return []
        
        try:
            query = "mimeType!='application/vnd.google-apps.folder'"
            
            if folder_id:
                query += f" and '{folder_id}' in parents"
            
            query += " and trashed=false"
            
            results = self.service.files().list(
                q=query,
                pageSize=1000,
                fields="files(id, name, mimeType, size, modifiedTime, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            # ファイル形式でフィルタ
            if file_types:
                from pathlib import Path
                filtered_files = []
                for file in files:
                    file_ext = Path(file['name']).suffix.lower().lstrip('.')
                    if file_ext in file_types:
                        filtered_files.append(file)
                return filtered_files
            
            return files
        
        except Exception as e:
            st.error(f"ファイル一覧の取得に失敗: {str(e)}")
            return []
    
    def download_file(self, file_id: str, destination_path: str) -> bool:
        """
        ファイルをダウンロード
        
        Args:
            file_id: ファイルID
            destination_path: ダウンロード先のパス
        
        Returns:
            成功したかどうか
        """
        if not self.is_authenticated():
            st.error("Google Driveに認証されていません")
            return False
        
        try:
            request = self.service.files().get_media(fileId=file_id)
            
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    progress_bar.progress(progress / 100)
                    status_text.text(f"ダウンロード中: {progress}%")
            
            # ファイルに書き込み
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            with open(destination_path, 'wb') as f:
                f.write(fh.getvalue())
            
            progress_bar.empty()
            status_text.empty()
            st.success(f"✓ ダウンロード完了: {os.path.basename(destination_path)}")
            return True
        
        except Exception as e:
            st.error(f"ダウンロードに失敗: {str(e)}")
            return False
    
    def download_folder(self, folder_id: str, destination_dir: str, file_types: List[str] = None) -> int:
        """
        フォルダ全体をダウンロード
        
        Args:
            folder_id: フォルダID
            destination_dir: ダウンロード先ディレクトリ
            file_types: 対象ファイル形式
        
        Returns:
            ダウンロードしたファイル数
        """
        if not self.is_authenticated():
            st.error("Google Driveに認証されていません")
            return 0
        
        try:
            os.makedirs(destination_dir, exist_ok=True)
            
            files = self.list_files(folder_id, file_types)
            
            if not files:
                st.info("フォルダ内にファイルがありません")
                return 0
            
            downloaded_count = 0
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, file in enumerate(files):
                status_text.text(f"ダウンロード中: {file['name']} ({i+1}/{len(files)})")
                
                file_path = os.path.join(destination_dir, file['name'])
                
                if self.download_file(file['id'], file_path):
                    downloaded_count += 1
                
                progress_bar.progress((i + 1) / len(files))
            
            progress_bar.empty()
            status_text.empty()
            
            st.success(f"✓ {downloaded_count}個のファイルをダウンロードしました")
            return downloaded_count
        
        except Exception as e:
            st.error(f"フォルダのダウンロードに失敗: {str(e)}")
            return 0
    
    def sync_folders(self, config_file: str = 'google_drive_config.json'):
        """
        設定ファイルに基づいてフォルダを同期
        
        Args:
            config_file: 設定ファイルのパス
        """
        if not self.is_authenticated():
            st.warning("Google Driveに認証されていません")
            return
        
        if not os.path.exists(config_file):
            st.warning(f"設定ファイルが見つかりません: {config_file}")
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if not config.get('enabled', False):
                st.info("Google Drive同期が無効になっています")
                return
            
            folders = config.get('folders', [])
            
            for folder_config in folders:
                if not folder_config.get('sync', False):
                    continue
                
                folder_name = folder_config['name']
                folder_id = folder_config['folder_id']
                local_path = folder_config['local_path']
                file_types = folder_config.get('file_types', [])
                
                st.write(f"📁 同期中: {folder_name}")
                
                self.download_folder(folder_id, local_path, file_types)
        
        except Exception as e:
            st.error(f"同期に失敗: {str(e)}")


def setup_service_account_demo():
    """サービスアカウント設定のデモ"""
    st.title("☁️ Google Drive サービスアカウント連携")
    
    st.markdown("""
    このページでは、サービスアカウントを使用したGoogle Drive連携のセットアップを行います。
    """)
    
    # 認証状態の確認
    drive = GoogleDriveServiceAccount()
    
    if drive.is_authenticated():
        st.success("✓ Google Driveに接続されています")
        
        # サービスアカウント情報
        with st.expander("サービスアカウント情報"):
            st.write(f"**メール:** {drive.service_account_email}")
        
        # フォルダ一覧を表示
        st.subheader("📁 アクセス可能なフォルダ")
        
        if st.button("フォルダを取得"):
            with st.spinner("読み込み中..."):
                folders = drive.list_folders()
                
                if folders:
                    st.success(f"{len(folders)}個のフォルダが見つかりました")
                    
                    for folder in folders:
                        with st.expander(f"📁 {folder['name']}"):
                            st.write(f"**ID:** `{folder['id']}`")
                            st.write(f"**更新日:** {folder.get('modifiedTime', 'N/A')}")
                            
                            if 'webViewLink' in folder:
                                st.write(f"[Google Driveで開く]({folder['webViewLink']})")
                else:
                    st.warning("""
                    アクセス可能なフォルダがありません。
                    
                    **対処法:**
                    1. Google Driveで共有したいフォルダを開く
                    2. 「共有」をクリック
                    3. サービスアカウントのメールアドレスを追加
                    4. 権限を「閲覧者」に設定
                    """)
    
    else:
        st.error("Google Driveに接続できません")
        
        st.markdown("""
        ### 📋 設定手順
        
        1. **Google Cloud Consoleでサービスアカウントを作成**
           - https://console.cloud.google.com/
           - 「IAMと管理」→「サービスアカウント」
           - サービスアカウントキー（JSON）をダウンロード
        
        2. **Streamlit Secretsに設定**
           
           **ローカル環境:**
           - `.streamlit/secrets.toml` を作成
           - サービスアカウントJSONの内容を追加
           
           **Streamlit Community Cloud:**
           - Settings → Secrets
           - サービスアカウントJSONの内容を貼り付け
        
        3. **Google Driveでフォルダを共有**
           - サービスアカウントのメールアドレスを共有相手に追加
           - 権限を「閲覧者」に設定
        
        詳細: `WEB_DEPLOYMENT_WITH_GOOGLE_DRIVE.md`
        """)


if __name__ == "__main__":
    setup_service_account_demo()

