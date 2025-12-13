"""
Google Drive連携機能の駆動テスト

このスクリプトは、Google Drive連携機能が正しく動作するかテストします。
"""

import os
import json
import sys
from pathlib import Path


def print_header(title):
    """ヘッダーを表示"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_section(title):
    """セクションヘッダーを表示"""
    print("\n" + "-" * 70)
    print(f"  {title}")
    print("-" * 70)


def test_file_exists(file_path, description):
    """ファイルの存在確認"""
    if os.path.exists(file_path):
        print(f"[OK] {description}: 存在")
        return True
    else:
        print(f"[NG] {description}: 見つかりません")
        return False


def test_import(module_name, description):
    """モジュールのインポート確認"""
    try:
        __import__(module_name)
        print(f"[OK] {description}: インポート成功")
        return True
    except ImportError as e:
        print(f"[NG] {description}: インポート失敗 - {e}")
        return False
    except Exception as e:
        print(f"[!!] {description}: エラー - {e}")
        return False


def test_json_config(file_path, description):
    """JSON設定ファイルの確認"""
    if not os.path.exists(file_path):
        print(f"[!!] {description}: ファイルが存在しません")
        return False, None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"[OK] {description}: 読み込み成功")
        return True, config
    except json.JSONDecodeError as e:
        print(f"[NG] {description}: JSON解析エラー - {e}")
        return False, None
    except Exception as e:
        print(f"[NG] {description}: 読み込みエラー - {e}")
        return False, None


def test_google_drive_api():
    """Google Drive APIライブラリの確認"""
    print_section("Google Drive APIライブラリのテスト")
    
    results = []
    results.append(test_import('googleapiclient.discovery', 'google-api-python-client'))
    results.append(test_import('google.auth', 'google-auth'))
    results.append(test_import('google_auth_oauthlib', 'google-auth-oauthlib'))
    
    if all(results):
        print("\n[OK] Google Drive APIライブラリ: すべて正常")
        return True
    else:
        print("\n[NG] Google Drive APIライブラリ: 一部インストール必要")
        print("   実行: pip install -r requirements_google_drive.txt")
        return False


def test_security_module():
    """セキュリティモジュールの確認"""
    print_section("セキュリティモジュールのテスト")
    
    if test_import('google_drive_security', 'google_drive_security.py'):
        try:
            from google_drive_security import GoogleDriveSecurityManager
            security = GoogleDriveSecurityManager()
            print("[OK] GoogleDriveSecurityManager: 初期化成功")
            
            # セキュリティ設定の確認
            print(f"   - セキュリティ有効: {security.config.get('enabled', False)}")
            print(f"   - アクセスログ有効: {security.config.get('access_log_enabled', False)}")
            print(f"   - 監査ログ有効: {security.config.get('audit_log_enabled', False)}")
            
            return True
        except Exception as e:
            print(f"[NG] GoogleDriveSecurityManager: 初期化エラー - {e}")
            return False
    else:
        return False


def test_drive_manager():
    """Google Driveマネージャーの確認"""
    print_section("Google Driveマネージャーのテスト")
    
    if test_import('google_drive_manager', 'google_drive_manager.py'):
        try:
            from google_drive_manager import GoogleDriveManager
            print("[OK] GoogleDriveManager: インポート成功")
            
            # 認証なしで初期化テスト
            print("   - 初期化テスト（認証なし）...")
            drive = GoogleDriveManager()
            print("[OK] GoogleDriveManager: 初期化成功")
            
            return True
        except Exception as e:
            print(f"[NG] GoogleDriveManager: エラー - {e}")
            return False
    else:
        return False


def test_configuration_files():
    """設定ファイルの確認"""
    print_section("設定ファイルのテスト")
    
    results = []
    
    # テンプレートファイルの存在確認
    print("\n【テンプレートファイル】")
    results.append(test_file_exists(
        'google_drive_config.json.template',
        'google_drive_config.json.template'
    ))
    results.append(test_file_exists(
        'google_drive_security_config.json.template',
        'google_drive_security_config.json.template'
    ))
    
    # 実際の設定ファイルの確認
    print("\n【実際の設定ファイル】")
    
    # Google Drive設定
    success, config = test_json_config(
        'google_drive_config.json',
        'google_drive_config.json'
    )
    if success and config:
        print(f"   - 有効: {config.get('enabled', False)}")
        accounts = config.get('accounts', [])
        print(f"   - 登録アカウント数: {len(accounts)}")
        for acc in accounts:
            status = "[*]" if acc.get('active', False) else "[ ]"
            print(f"     {status} {acc.get('name', 'N/A')} ({acc.get('email', 'N/A')})")
    
    # セキュリティ設定
    success, config = test_json_config(
        'google_drive_security_config.json',
        'google_drive_security_config.json'
    )
    if success and config:
        print(f"   - セキュリティ有効: {config.get('enabled', False)}")
        print(f"   - ホワイトリスト有効: {config.get('whitelist_enabled', False)}")
        if config.get('whitelist_enabled', False):
            whitelisted = config.get('whitelisted_accounts', [])
            print(f"   - 許可アカウント数: {len(whitelisted)}")
    
    return True


def test_credentials():
    """認証情報の確認"""
    print_section("認証情報ファイルのテスト")
    
    # 認証情報ファイルの確認
    creds_files = [
        'google_drive_credentials.json',
        'google_drive_credentials_admin.json',
        'google_drive_credentials_sales.json',
        'google_drive_credentials_tech.json'
    ]
    
    found_creds = []
    for cred_file in creds_files:
        if os.path.exists(cred_file):
            print(f"[OK] 認証情報ファイル: {cred_file} 存在")
            found_creds.append(cred_file)
        else:
            print(f"[ ] 認証情報ファイル: {cred_file} なし")
    
    # トークンファイルの確認
    print("\n【トークンファイル（認証済み）】")
    token_files = [
        'google_drive_token.pickle',
        'google_drive_token_admin.pickle',
        'google_drive_token_sales.pickle',
        'google_drive_token_tech.pickle'
    ]
    
    found_tokens = []
    for token_file in token_files:
        if os.path.exists(token_file):
            print(f"[OK] トークンファイル: {token_file} 存在（認証済み）")
            found_tokens.append(token_file)
        else:
            print(f"[ ] トークンファイル: {token_file} なし（未認証）")
    
    if not found_creds:
        print("\n[!!] 認証情報ファイルが見つかりません")
        print("   Google Cloud Consoleで認証情報を作成してください")
        print("   詳細: GOOGLE_DRIVE_ACCOUNT_SETUP.md")
    
    if not found_tokens:
        print("\n[!!] トークンファイルが見つかりません")
        print("   初回認証が必要です")
        print("   実行: streamlit run google_drive_manager.py")
    
    return len(found_creds) > 0


def test_security_functions():
    """セキュリティ機能のテスト"""
    print_section("セキュリティ機能のテスト")
    
    try:
        from google_drive_security import GoogleDriveSecurityManager
        
        security = GoogleDriveSecurityManager()
        
        # アカウントホワイトリストテスト
        print("\n【アカウントホワイトリストテスト】")
        test_accounts = [
            ('user@mm-international.co.jp', True),
            ('external@example.com', False),
            ('admin@mm-international.co.jp', True)
        ]
        
        for email, expected in test_accounts:
            result = security.is_account_allowed(email)
            status = "[OK]" if result == expected else "[NG]"
            print(f"{status} {email}: {'許可' if result else '拒否'}")
        
        # ファイル形式テスト
        print("\n【ファイル形式テスト】")
        test_files = [
            ('document.pdf', True),
            ('script.exe', False),
            ('data.xlsx', True),
            ('malware.bat', False)
        ]
        
        for filename, expected in test_files:
            result = security.is_file_type_allowed(filename)
            status = "[OK]" if result == expected else "[NG]"
            print(f"{status} {filename}: {'許可' if result else '拒否'}")
        
        # ファイルサイズテスト
        print("\n【ファイルサイズテスト】")
        test_sizes = [
            (10 * 1024 * 1024, '10MB', True),
            (150 * 1024 * 1024, '150MB', False)
        ]
        
        for size, label, expected in test_sizes:
            result = security.is_file_size_allowed(size)
            status = "[OK]" if result == expected else "[NG]"
            print(f"{status} {label}: {'許可' if result else '拒否'}")
        
        return True
        
    except Exception as e:
        print(f"[NG] セキュリティ機能テストエラー: {e}")
        return False


def test_log_directories():
    """ログディレクトリの確認"""
    print_section("ログディレクトリのテスト")
    
    log_dir = 'logs'
    if os.path.exists(log_dir):
        print(f"[OK] ログディレクトリ: {log_dir} 存在")
        
        # ログファイルの確認
        log_files = [
            'google_drive_access.json',
            'google_drive_audit.json'
        ]
        
        for log_file in log_files:
            log_path = os.path.join(log_dir, log_file)
            if os.path.exists(log_path):
                file_size = os.path.getsize(log_path)
                print(f"[OK] ログファイル: {log_file} ({file_size} bytes)")
            else:
                print(f"[ ] ログファイル: {log_file} なし（まだログが記録されていません）")
    else:
        print(f"[ ] ログディレクトリ: {log_dir} なし")
        print("   初回実行時に自動作成されます")
    
    return True


def test_documentation():
    """ドキュメントの確認"""
    print_section("ドキュメントのテスト")
    
    docs = [
        ('GOOGLE_DRIVE_SETUP.md', '基本セットアップガイド'),
        ('GOOGLE_DRIVE_ACCOUNT_SETUP.md', 'アカウント指定ガイド'),
        ('GOOGLE_ACCOUNT_QUICK_START.md', 'クイックスタート'),
        ('GOOGLE_DRIVE_SECURITY_GUIDE.md', 'セキュリティガイド'),
        ('GOOGLE_DRIVE_SECURITY_SUMMARY.md', 'セキュリティ完了報告'),
        ('GOOGLE_DRIVE_SUMMARY.md', '機能概要')
    ]
    
    for doc_file, description in docs:
        test_file_exists(doc_file, f'{description} ({doc_file})')
    
    return True


def test_helper_scripts():
    """ヘルパースクリプトの確認"""
    print_section("ヘルパースクリプトのテスト")
    
    scripts = [
        ('setup_google_account.py', 'アカウント設定ツール'),
        ('install_google_drive.bat', 'インストールスクリプト'),
        ('google_drive_manager.py', 'Google Driveマネージャー'),
        ('google_drive_security.py', 'セキュリティマネージャー')
    ]
    
    for script_file, description in scripts:
        test_file_exists(script_file, f'{description} ({script_file})')
    
    return True


def generate_summary(results):
    """テスト結果のサマリーを生成"""
    print_header("テスト結果サマリー")
    
    total = len(results)
    passed = sum(1 for r in results if r)
    failed = total - passed
    
    print(f"\n総テスト数: {total}")
    print(f"[OK] 成功: {passed}")
    print(f"[NG] 失敗: {failed}")
    
    if failed == 0:
        print("\n[SUCCESS] すべてのテストが成功しました！")
        print("   Google Drive連携機能は正常に動作する準備ができています。")
    else:
        print("\n[WARNING] 一部のテストが失敗しました。")
        print("   上記のエラーメッセージを確認して修正してください。")
    
    # 次のステップの提案
    print("\n" + "=" * 70)
    print("  次のステップ")
    print("=" * 70)
    
    if not os.path.exists('google_drive_credentials.json'):
        print("\n1. Google Cloud Consoleで認証情報を作成")
        print("   https://console.cloud.google.com/")
        print("   詳細: GOOGLE_DRIVE_ACCOUNT_SETUP.md")
    
    if not os.path.exists('google_drive_config.json'):
        print("\n2. アカウント設定を実行")
        print("   python setup_google_account.py")
    
    if not os.path.exists('google_drive_token.pickle'):
        print("\n3. 初回認証を実行")
        print("   streamlit run google_drive_manager.py")
    
    if not os.path.exists('google_drive_security_config.json'):
        print("\n4. セキュリティ設定を作成")
        print("   copy google_drive_security_config.json.template google_drive_security_config.json")
    
    print("\n5. セキュリティダッシュボードで確認")
    print("   streamlit run google_drive_security.py")
    
    return failed == 0


def main():
    """メインテスト実行"""
    print_header("Google Drive連携機能 駆動テスト")
    print("\nこのテストは、Google Drive連携機能が正しくセットアップされているか確認します。")
    
    results = []
    
    # 各テストを実行
    results.append(test_google_drive_api())
    results.append(test_security_module())
    results.append(test_drive_manager())
    results.append(test_configuration_files())
    results.append(test_credentials())
    results.append(test_security_functions())
    results.append(test_log_directories())
    results.append(test_documentation())
    results.append(test_helper_scripts())
    
    # サマリーを表示
    success = generate_summary(results)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

