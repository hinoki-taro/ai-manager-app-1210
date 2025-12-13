"""
Google Driveマネージャーモジュール
Google Driveのフォルダ・ファイルにアクセスする機能を提供します。

使用方法:
    import google_drive_manager as gdm
    
    # 初期化
    drive = gdm.GoogleDriveManager()
    
    # フォルダ一覧を取得
    folders = drive.list_folders()
    
    # ファイルをダウンロード
    drive.download_file(file_id, 'local_path.pdf')
"""

import os
import io
import json
import pickle
from pathlib import Path
from typing import Optional, List, Dict, Any
import streamlit as st

# Google Drive API
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False

# セキュリティマネージャー
try:
    from google_drive_security import GoogleDriveSecurityManager
    SECURITY_AVAILABLE = True
except ImportError:
    SECURITY_AVAILABLE = False


class GoogleDriveManager:
    """Google Drive管理クラス"""
    
    # OAuth2.0のスコープ
    SCOPES = [
        'https://www.googleapis.com/auth/drive.readonly',  # 読み取り専用
        'https://www.googleapis.com/auth/drive.metadata.readonly'  # メタデータ読み取り
    ]
    
    # デフォルトの認証情報保存先
    DEFAULT_TOKEN_FILE = 'google_drive_token.pickle'
    DEFAULT_CREDENTIALS_FILE = 'google_drive_credentials.json'
    
    def __init__(self, account_config: Dict[str, str] = None, enable_security: bool = True):
        """
        初期化
        
        Args:
            account_config: アカウント設定（credentials_file, token_file, email）
            enable_security: セキュリティ機能を有効にするか
        """
        self.service = None
        self.authenticated = False
        self.account_email = None
        
        if not GOOGLE_DRIVE_AVAILABLE:
            st.error("Google Drive APIライブラリが必要です: pip install -r requirements_google_drive.txt")
            return
        
        # セキュリティマネージャーを初期化
        self.security = None
        if enable_security and SECURITY_AVAILABLE:
            self.security = GoogleDriveSecurityManager()
            
            # セキュリティログ: 初期化
            if account_config and account_config.get('email'):
                self.security.log_audit(
                    account_config['email'],
                    "initialization",
                    "Google Driveマネージャーを初期化しました",
                    "info"
                )
        
        # アカウント設定を保存
        if account_config:
            self.credentials_file = account_config.get('credentials_file', self.DEFAULT_CREDENTIALS_FILE)
            self.token_file = account_config.get('token_file', self.DEFAULT_TOKEN_FILE)
            self.account_email = account_config.get('email')
        else:
            self.credentials_file = self.DEFAULT_CREDENTIALS_FILE
            self.token_file = self.DEFAULT_TOKEN_FILE
        
        # 認証を試行
        self._authenticate()
    
    def _authenticate(self):
        """Google Drive APIの認証"""
        creds = None
        
        # トークンファイルが存在する場合は読み込む
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # 認証情報が無効または期限切れの場合
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # トークンをリフレッシュ
                try:
                    creds.refresh(Request())
                    # 更新したトークンを保存
                    with open(self.token_file, 'wb') as token:
                        pickle.dump(creds, token)
                except Exception as e:
                    st.warning(f"トークンのリフレッシュに失敗: {str(e)}")
                    creds = None
            
            # 新規認証が必要
            if not creds:
                if not os.path.exists(self.credentials_file):
                    st.error(f"""
                    Google Drive認証情報が見つかりません: `{self.credentials_file}`
                    
                    **設定手順:**
                    1. Google Cloud Consoleで認証情報を作成
                    2. `{self.credentials_file}` に配置
                    3. アカウント: {self.account_email or '未設定'}
                    
                    詳細は `GOOGLE_DRIVE_ACCOUNT_SETUP.md` を参照してください。
                    """)
                    return
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    
                    # トークンを保存
                    with open(self.token_file, 'wb') as token:
                        pickle.dump(creds, token)
                    
                    if self.account_email:
                        st.success(f"✓ Google Driveの認証に成功しました！\nアカウント: {self.account_email}")
                    else:
                        st.success("✓ Google Driveの認証に成功しました！")
                
                except Exception as e:
                    st.error(f"認証に失敗しました: {str(e)}")
                    return
        
        # Drive APIサービスを構築
        try:
            self.service = build('drive', 'v3', credentials=creds)
            self.authenticated = True
            
            # 認証されたアカウント情報を取得
            if self.account_email is None:
                try:
                    about = self.service.about().get(fields="user").execute()
                    self.account_email = about['user'].get('emailAddress', 'Unknown')
                except Exception:
                    pass
                    
        except Exception as e:
            st.error(f"Google Drive APIの初期化に失敗: {str(e)}")
    
    def is_authenticated(self) -> bool:
        """認証状態を確認"""
        return self.authenticated and self.service is not None
    
    def list_folders(self, parent_folder_id: str = None) -> List[Dict[str, Any]]:
        """
        フォルダ一覧を取得
        
        Args:
            parent_folder_id: 親フォルダID（Noneの場合はルート）
        
        Returns:
            フォルダ情報のリスト
        """
        if not self.is_authenticated():
            st.error("Google Driveに認証されていません")
            return []
        
        # セキュリティチェック
        if self.security:
            allowed, reason = self.security.validate_access(
                self.account_email or "unknown",
                parent_folder_id or "root",
                "list_folders"
            )
            if not allowed:
                st.error(f"アクセスが拒否されました: {reason}")
                return []
        
        try:
            # クエリを構築
            query = "mimeType='application/vnd.google-apps.folder'"
            
            if parent_folder_id:
                query += f" and '{parent_folder_id}' in parents"
            
            query += " and trashed=false"
            
            # フォルダを検索
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, modifiedTime, webViewLink)"
            ).execute()
            
            folders = results.get('files', [])
            
            # セキュリティログ: 成功
            if self.security:
                self.security.log_access(
                    self.account_email or "unknown",
                    "list_folders",
                    parent_folder_id or "root",
                    "success",
                    {"folder_count": len(folders)}
                )
            
            return folders
        
        except Exception as e:
            # セキュリティログ: エラー
            if self.security:
                self.security.log_audit(
                    self.account_email or "unknown",
                    "error",
                    f"フォルダ一覧の取得に失敗: {str(e)}",
                    "error"
                )
            st.error(f"フォルダ一覧の取得に失敗: {str(e)}")
            return []
    
    def list_files(self, folder_id: str = None, file_types: List[str] = None) -> List[Dict[str, Any]]:
        """
        ファイル一覧を取得
        
        Args:
            folder_id: フォルダID（Noneの場合はルート）
            file_types: ファイルタイプのリスト（例: ['pdf', 'docx']）
        
        Returns:
            ファイル情報のリスト
        """
        if not self.is_authenticated():
            st.error("Google Driveに認証されていません")
            return []
        
        try:
            # クエリを構築
            query = "mimeType!='application/vnd.google-apps.folder'"
            
            if folder_id:
                query += f" and '{folder_id}' in parents"
            
            query += " and trashed=false"
            
            # ファイルを検索
            results = self.service.files().list(
                q=query,
                pageSize=1000,
                fields="files(id, name, mimeType, size, modifiedTime, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            # ファイルタイプでフィルタ
            if file_types:
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
            # ファイル情報を取得
            file_info = self.service.files().get(
                fileId=file_id,
                fields="name, size"
            ).execute()
            
            file_name = file_info.get('name', 'unknown')
            file_size = int(file_info.get('size', 0))
            
            # セキュリティチェック: ファイルダウンロード検証
            if self.security:
                allowed, reason = self.security.validate_file_download(
                    self.account_email or "unknown",
                    file_name,
                    file_size
                )
                if not allowed:
                    st.error(f"ダウンロードが拒否されました: {reason}")
                    return False
            
            # ファイルをダウンロード
            request = self.service.files().get_media(fileId=file_id)
            
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            with st.spinner(f"ダウンロード中..."):
                while not done:
                    status, done = downloader.next_chunk()
                    if status:
                        progress = int(status.progress() * 100)
                        st.progress(progress / 100, text=f"進行状況: {progress}%")
            
            # ファイルに書き込み
            with open(destination_path, 'wb') as f:
                f.write(fh.getvalue())
            
            # セキュリティログ: ダウンロード成功
            if self.security:
                self.security.log_access(
                    self.account_email or "unknown",
                    "download_file",
                    file_name,
                    "success",
                    {
                        "file_id": file_id,
                        "file_size": file_size,
                        "destination": destination_path
                    }
                )
            
            st.success(f"✓ ダウンロード完了: {destination_path}")
            return True
        
        except Exception as e:
            # セキュリティログ: エラー
            if self.security:
                self.security.log_audit(
                    self.account_email or "unknown",
                    "download_error",
                    f"ファイルのダウンロードに失敗: {str(e)}",
                    "error"
                )
            st.error(f"ダウンロードに失敗: {str(e)}")
            return False
    
    def download_folder(self, folder_id: str, destination_dir: str) -> int:
        """
        フォルダ全体をダウンロード
        
        Args:
            folder_id: フォルダID
            destination_dir: ダウンロード先ディレクトリ
        
        Returns:
            ダウンロードしたファイル数
        """
        if not self.is_authenticated():
            st.error("Google Driveに認証されていません")
            return 0
        
        try:
            # ディレクトリを作成
            os.makedirs(destination_dir, exist_ok=True)
            
            # フォルダ内のファイルを取得
            files = self.list_files(folder_id)
            
            if not files:
                st.info("フォルダ内にファイルがありません")
                return 0
            
            downloaded_count = 0
            
            with st.progress(0) as progress_bar:
                for i, file in enumerate(files):
                    file_path = os.path.join(destination_dir, file['name'])
                    
                    if self.download_file(file['id'], file_path):
                        downloaded_count += 1
                    
                    # 進捗を更新
                    progress_bar.progress((i + 1) / len(files))
            
            st.success(f"✓ {downloaded_count}個のファイルをダウンロードしました")
            return downloaded_count
        
        except Exception as e:
            st.error(f"フォルダのダウンロードに失敗: {str(e)}")
            return 0
    
    def get_file_info(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        ファイル情報を取得
        
        Args:
            file_id: ファイルID
        
        Returns:
            ファイル情報
        """
        if not self.is_authenticated():
            st.error("Google Driveに認証されていません")
            return None
        
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, size, modifiedTime, webViewLink, parents"
            ).execute()
            
            return file
        
        except Exception as e:
            st.error(f"ファイル情報の取得に失敗: {str(e)}")
            return None
    
    def search_files(self, query: str) -> List[Dict[str, Any]]:
        """
        ファイルを検索
        
        Args:
            query: 検索クエリ（ファイル名）
        
        Returns:
            検索結果のリスト
        """
        if not self.is_authenticated():
            st.error("Google Driveに認証されていません")
            return []
        
        try:
            # クエリを構築
            search_query = f"name contains '{query}' and trashed=false"
            
            # 検索を実行
            results = self.service.files().list(
                q=search_query,
                pageSize=100,
                fields="files(id, name, mimeType, size, modifiedTime, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            return files
        
        except Exception as e:
            st.error(f"検索に失敗: {str(e)}")
            return []


def create_google_drive_path_config():
    """Google Driveパス設定を作成"""
    config = {
        "enabled": False,
        "folders": [
            {
                "name": "社内文書",
                "folder_id": "YOUR_FOLDER_ID_HERE",
                "local_path": "./data/google_drive/社内文書",
                "sync": True,
                "file_types": ["pdf", "docx", "txt"]
            },
            {
                "name": "メディアファイル",
                "folder_id": "YOUR_FOLDER_ID_HERE",
                "local_path": "./data/google_drive/メディア",
                "sync": True,
                "file_types": ["pdf", "docx", "pptx"]
            }
        ]
    }
    
    with open('google_drive_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    
    st.success("Google Driveパス設定ファイルを作成しました: google_drive_config.json")
    return config


def sync_google_drive_folders():
    """設定されたGoogle Driveフォルダを同期（複数アカウント対応）"""
    # 設定ファイルを読み込む
    if not os.path.exists('google_drive_config.json'):
        st.warning("Google Drive設定ファイルが見つかりません。作成しますか？")
        if st.button("設定ファイルを作成"):
            create_google_drive_path_config()
        return
    
    with open('google_drive_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    if not config.get('enabled', False):
        st.info("Google Drive同期が無効になっています")
        return
    
    # アカウントごとにマネージャーを作成
    account_managers = {}
    
    for account in config.get('accounts', []):
        if not account.get('active', False):
            continue
        
        account_name = account['name']
        st.write(f"🔐 認証中: {account_name} ({account.get('email', 'N/A')})")
        
        # アカウント用のマネージャーを作成
        drive = GoogleDriveManager(account_config=account)
        
        if drive.is_authenticated():
            account_managers[account_name] = drive
            st.success(f"✓ {account_name} 認証済み")
        else:
            st.error(f"✗ {account_name} 認証失敗")
    
    if not account_managers:
        # 旧形式のサポート（アカウント設定なし）
        drive = GoogleDriveManager()
        if not drive.is_authenticated():
            st.error("Google Driveの認証が必要です")
            return
        account_managers['default'] = drive
    
    # 各フォルダを同期
    for folder_config in config['folders']:
        if not folder_config.get('sync', False):
            continue
        
        folder_name = folder_config['name']
        account_name = folder_config.get('account', 'default')
        
        # 対応するアカウントのマネージャーを取得
        drive = account_managers.get(account_name)
        if not drive:
            st.warning(f"⚠ フォルダ '{folder_name}' のアカウント '{account_name}' が見つかりません")
            continue
        
        st.write(f"📁 同期中: {folder_name} ({account_name})")
        
        folder_id = folder_config['folder_id']
        local_path = folder_config['local_path']
        file_types = folder_config.get('file_types', [])
        
        # ファイル一覧を取得
        files = drive.list_files(folder_id, file_types)
        
        if files:
            os.makedirs(local_path, exist_ok=True)
            
            for file in files:
                file_path = os.path.join(local_path, file['name'])
                
                # ファイルが存在しない、または更新されている場合のみダウンロード
                if not os.path.exists(file_path):
                    drive.download_file(file['id'], file_path)
        else:
            st.info(f"  フォルダ '{folder_name}' にファイルがありません")


def demo_google_drive_manager():
    """Google Driveマネージャーのデモ（複数アカウント対応）"""
    st.title("☁️ Google Drive マネージャー")
    
    if not GOOGLE_DRIVE_AVAILABLE:
        st.error("Google Drive APIライブラリをインストールしてください")
        st.code("pip install -r requirements_google_drive.txt")
        return
    
    # 設定ファイルを読み込む
    account_config = None
    if os.path.exists('google_drive_config.json'):
        with open('google_drive_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # アクティブなアカウントを取得
        accounts = config.get('accounts', [])
        if accounts:
            active_accounts = [acc for acc in accounts if acc.get('active', False)]
            if active_accounts:
                account_config = active_accounts[0]
                
                # サイドバーにアカウント選択
                with st.sidebar:
                    st.subheader("📧 アカウント")
                    account_names = [acc['name'] for acc in active_accounts]
                    selected_account = st.selectbox("使用アカウント", account_names)
                    
                    # 選択されたアカウントの設定を取得
                    for acc in active_accounts:
                        if acc['name'] == selected_account:
                            account_config = acc
                            break
                    
                    if account_config:
                        st.info(f"**メール:** {account_config.get('email', 'N/A')}")
    
    # 初期化
    drive = GoogleDriveManager(account_config=account_config)
    
    if not drive.is_authenticated():
        st.warning("Google Driveの認証が必要です")
        
        if account_config:
            st.info(f"""
            **アカウント:** {account_config.get('name', 'N/A')}  
            **メール:** {account_config.get('email', 'N/A')}  
            **認証情報:** {account_config.get('credentials_file', 'N/A')}
            """)
        
        with st.expander("📖 認証設定ガイド"):
            st.markdown("""
            ### Google Drive API認証の設定
            
            1. **Google Cloud Consoleにアクセス**
               - https://console.cloud.google.com/
            
            2. **プロジェクトを作成**
               - 新しいプロジェクトを作成
            
            3. **APIを有効化**
               - Google Drive APIを有効化
            
            4. **認証情報を作成**
               - OAuth 2.0クライアントIDを作成
               - アプリケーションの種類: デスクトップアプリ
            
            5. **認証情報をダウンロード**
               - JSONファイルをダウンロード
               - `google_drive_credentials.json` にリネーム
               - アプリのルートディレクトリに配置
            
            6. **アプリを再起動**
               - 初回起動時にブラウザで認証
            """)
        return
    
    # タブ
    tab1, tab2, tab3, tab4 = st.tabs(["フォルダ一覧", "ファイル検索", "ダウンロード", "設定"])
    
    with tab1:
        st.header("フォルダ一覧")
        
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
                                st.write(f"**リンク:** {folder['webViewLink']}")
                            
                            # フォルダ内のファイルを表示
                            if st.button(f"ファイルを表示", key=f"show_{folder['id']}"):
                                files = drive.list_files(folder['id'])
                                if files:
                                    st.write(f"{len(files)}個のファイル:")
                                    for file in files[:10]:  # 最初の10件
                                        st.write(f"- {file['name']}")
                else:
                    st.info("フォルダが見つかりませんでした")
    
    with tab2:
        st.header("ファイル検索")
        
        search_query = st.text_input("検索キーワード")
        
        if st.button("検索"):
            if search_query:
                with st.spinner("検索中..."):
                    results = drive.search_files(search_query)
                    
                    if results:
                        st.success(f"{len(results)}件見つかりました")
                        
                        for file in results:
                            with st.expander(f"📄 {file['name']}"):
                                st.write(f"**ID:** `{file['id']}`")
                                st.write(f"**タイプ:** {file.get('mimeType', 'N/A')}")
                                st.write(f"**サイズ:** {file.get('size', 'N/A')} bytes")
                                if 'webViewLink' in file:
                                    st.write(f"**リンク:** {file['webViewLink']}")
                    else:
                        st.info("ファイルが見つかりませんでした")
    
    with tab3:
        st.header("ファイルダウンロード")
        
        file_id = st.text_input("ファイルID")
        destination = st.text_input("保存先パス", "downloaded_file.pdf")
        
        if st.button("ダウンロード"):
            if file_id:
                drive.download_file(file_id, destination)
    
    with tab4:
        st.header("設定")
        
        if st.button("パス設定ファイルを作成"):
            create_google_drive_path_config()
        
        if st.button("フォルダを同期"):
            sync_google_drive_folders()


if __name__ == "__main__":
    demo_google_drive_manager()

