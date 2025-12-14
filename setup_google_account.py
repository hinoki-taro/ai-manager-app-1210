"""
Google Driveアカウント設定ユーティリティ

特定のGoogleアカウントを簡単に設定するためのインタラクティブスクリプト
"""

import json
import os
from pathlib import Path

def setup_account():
    """アカウント設定のインタラクティブセットアップ"""
    
    print("=" * 60)
    print("Google Driveアカウント設定")
    print("=" * 60)
    print()
    
    # 既存の設定を読み込む
    config = {}
    if os.path.exists('google_drive_config.json'):
        try:
            with open('google_drive_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("✓ 既存の設定を読み込みました")
        except Exception as e:
            print(f"⚠ 設定ファイルの読み込みに失敗: {e}")
    else:
        # 新規作成
        config = {
            "enabled": False,
            "accounts": [],
            "folders": [],
            "sync_on_startup": False,
            "auto_sync_interval_minutes": 60
        }
        print("新規設定を作成します")
    
    print()
    print("-" * 60)
    print("アカウント情報の入力")
    print("-" * 60)
    print()
    
    # アカウント名
    account_name = input("アカウント名（例: 社内共有アカウント）: ").strip()
    if not account_name:
        account_name = "メインアカウント"
    
    # メールアドレス
    email = input("Googleアカウントのメールアドレス: ").strip()
    if not email:
        print("❌ メールアドレスは必須です")
        return
    
    # 認証情報ファイル名
    print()
    print("認証情報ファイル名を入力してください")
    print("（Google Cloud Consoleからダウンロードしたファイルの名前）")
    credentials_file = input("ファイル名（デフォルト: google_drive_credentials.json）: ").strip()
    if not credentials_file:
        credentials_file = "google_drive_credentials.json"
    
    # トークンファイル名（自動生成）
    if credentials_file == "google_drive_credentials.json":
        token_file = "google_drive_token.pickle"
    else:
        # credentials_file から拡張子を除いて token_file を生成
        base_name = Path(credentials_file).stem
        token_file = f"{base_name.replace('credentials', 'token')}.pickle"
    
    print(f"トークンファイル: {token_file}")
    
    # アクティブ設定
    print()
    active_input = input("このアカウントをアクティブにしますか？ (Y/n): ").strip().lower()
    active = active_input != 'n'
    
    # アカウント情報を作成
    new_account = {
        "name": account_name,
        "email": email,
        "credentials_file": credentials_file,
        "token_file": token_file,
        "active": active
    }
    
    # 既存のアカウントを確認
    accounts = config.get('accounts', [])
    existing_index = -1
    for i, acc in enumerate(accounts):
        if acc['email'] == email:
            existing_index = i
            break
    
    if existing_index >= 0:
        print()
        print(f"⚠ このメールアドレスは既に登録されています")
        overwrite = input("上書きしますか？ (Y/n): ").strip().lower()
        if overwrite != 'n':
            accounts[existing_index] = new_account
            print("✓ アカウント情報を更新しました")
        else:
            print("キャンセルしました")
            return
    else:
        accounts.append(new_account)
        print()
        print("✓ アカウント情報を追加しました")
    
    config['accounts'] = accounts
    
    # Google Drive連携を有効化
    if active:
        config['enabled'] = True
    
    # 設定を保存
    print()
    print("-" * 60)
    print("設定を保存しています...")
    print("-" * 60)
    
    try:
        with open('google_drive_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        print("✓ google_drive_config.json に保存しました")
    except Exception as e:
        print(f"❌ 保存に失敗: {e}")
        return
    
    # 次のステップを表示
    print()
    print("=" * 60)
    print("次のステップ")
    print("=" * 60)
    print()
    print(f"1. Google Cloud Consoleで '{email}' の認証情報を作成")
    print("   https://console.cloud.google.com/")
    print()
    print(f"2. ダウンロードしたJSONファイルを '{credentials_file}' にリネーム")
    print()
    print(f"3. '{credentials_file}' をこのフォルダに配置")
    print()
    print("4. デモアプリで認証:")
    print("   streamlit run google_drive_manager.py")
    print()
    print("5. フォルダIDを取得してフォルダ設定を追加")
    print("   python add_folder.py")
    print()
    print("=" * 60)
    print()
    print("詳細: GOOGLE_DRIVE_ACCOUNT_SETUP.md")
    print()


def list_accounts():
    """設定済みアカウントの一覧表示"""
    
    if not os.path.exists('google_drive_config.json'):
        print("❌ 設定ファイルが見つかりません")
        return
    
    try:
        with open('google_drive_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ 設定ファイルの読み込みに失敗: {e}")
        return
    
    accounts = config.get('accounts', [])
    
    if not accounts:
        print("登録されているアカウントがありません")
        return
    
    print()
    print("=" * 60)
    print("登録済みアカウント")
    print("=" * 60)
    print()
    
    for i, acc in enumerate(accounts, 1):
        print(f"{i}. {acc['name']}")
        print(f"   メール: {acc['email']}")
        print(f"   認証情報: {acc['credentials_file']}")
        print(f"   トークン: {acc['token_file']}")
        print(f"   状態: {'🟢 アクティブ' if acc.get('active', False) else '⚪ 非アクティブ'}")
        
        # 認証情報ファイルの存在確認
        if os.path.exists(acc['credentials_file']):
            print(f"   認証情報ファイル: ✓ 存在")
        else:
            print(f"   認証情報ファイル: ❌ 未配置")
        
        # トークンファイルの存在確認
        if os.path.exists(acc['token_file']):
            print(f"   トークンファイル: ✓ 認証済み")
        else:
            print(f"   トークンファイル: ⚠ 未認証")
        
        print()


def add_folder():
    """フォルダ設定の追加"""
    
    print("=" * 60)
    print("Google Driveフォルダの追加")
    print("=" * 60)
    print()
    
    # 設定を読み込む
    if not os.path.exists('google_drive_config.json'):
        print("❌ 設定ファイルが見つかりません")
        print("先に 'python setup_google_account.py' を実行してください")
        return
    
    try:
        with open('google_drive_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ 設定ファイルの読み込みに失敗: {e}")
        return
    
    # アカウント一覧を表示
    accounts = config.get('accounts', [])
    if not accounts:
        print("❌ アカウントが登録されていません")
        return
    
    print("登録済みアカウント:")
    for i, acc in enumerate(accounts, 1):
        status = "🟢" if acc.get('active', False) else "⚪"
        print(f"{i}. {status} {acc['name']} ({acc['email']})")
    print()
    
    # フォルダ情報の入力
    folder_name = input("フォルダ名（例: 社内文書）: ").strip()
    if not folder_name:
        print("❌ フォルダ名は必須です")
        return
    
    print()
    print("Google DriveでフォルダのURLを開き、フォルダIDをコピーしてください")
    print("例: https://drive.google.com/drive/folders/1aBcDeFg...")
    print("                                          ↑ この部分")
    print()
    folder_id = input("フォルダID: ").strip()
    if not folder_id:
        print("❌ フォルダIDは必須です")
        return
    
    local_path = input(f"ローカル保存先（デフォルト: ./data/google_drive/{folder_name}）: ").strip()
    if not local_path:
        local_path = f"./data/google_drive/{folder_name}"
    
    print()
    print("対象ファイル形式（カンマ区切り、例: pdf,docx,txt）")
    file_types_input = input("ファイル形式（デフォルト: pdf,docx,txt）: ").strip()
    if not file_types_input:
        file_types = ["pdf", "docx", "txt"]
    else:
        file_types = [ft.strip() for ft in file_types_input.split(',')]
    
    # アカウント選択
    print()
    account_index = input(f"使用するアカウント（1-{len(accounts)}）: ").strip()
    try:
        account_index = int(account_index) - 1
        if account_index < 0 or account_index >= len(accounts):
            raise ValueError()
        account_name = accounts[account_index]['name']
    except:
        print("❌ 無効な選択です")
        return
    
    sync = input("自動同期を有効にしますか？ (Y/n): ").strip().lower() != 'n'
    
    # フォルダ設定を作成
    new_folder = {
        "name": folder_name,
        "folder_id": folder_id,
        "local_path": local_path,
        "sync": sync,
        "file_types": file_types,
        "account": account_name
    }
    
    # 設定に追加
    folders = config.get('folders', [])
    folders.append(new_folder)
    config['folders'] = folders
    
    # 保存
    try:
        with open('google_drive_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        print()
        print("✓ フォルダ設定を追加しました")
        print()
        print(f"フォルダ名: {folder_name}")
        print(f"フォルダID: {folder_id}")
        print(f"保存先: {local_path}")
        print(f"アカウント: {account_name}")
        print(f"同期: {'有効' if sync else '無効'}")
    except Exception as e:
        print(f"❌ 保存に失敗: {e}")


if __name__ == "__main__":
    print()
    print("=" * 60)
    print("Google Driveアカウント設定ユーティリティ")
    print("=" * 60)
    print()
    print("1. アカウントを追加・設定")
    print("2. 登録済みアカウントを表示")
    print("3. フォルダを追加")
    print("0. 終了")
    print()
    
    choice = input("選択してください (0-3): ").strip()
    
    if choice == "1":
        setup_account()
    elif choice == "2":
        list_accounts()
    elif choice == "3":
        add_folder()
    elif choice == "0":
        print("終了します")
    else:
        print("無効な選択です")



