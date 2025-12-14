"""
システム統合テスト
主要な機能が正常に動作することを確認します
"""

import os
import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Windows コンソールのエンコーディング問題対策
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

def test_1_environment_setup():
    """テスト1: 環境変数と設定ファイルの確認"""
    print("\n" + "="*60)
    print("テスト1: 環境設定の確認")
    print("="*60)
    
    # .envファイルの存在確認
    env_file = project_root / ".env"
    assert env_file.exists(), "[FAIL] .envファイルが見つかりません"
    print("[OK] .envファイルが存在します")
    
    # APIキーの存在確認
    from dotenv import load_dotenv
    load_dotenv()
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    assert google_api_key or openai_api_key, "❌ APIキーが設定されていません"
    
    if openai_api_key:
        print(f"✅ OpenAI APIキーが設定されています (先頭10文字: {openai_api_key[:10]}...)")
    if google_api_key:
        print(f"✅ Google APIキーが設定されています (先頭10文字: {google_api_key[:10]}...)")
    
    print("✅ テスト1: 合格")


def test_2_vectorstore_exists():
    """テスト2: ベクターストアの存在確認"""
    print("\n" + "="*60)
    print("テスト2: ベクターストアの確認")
    print("="*60)
    
    vectorstore_path = project_root / "vectorstore"
    assert vectorstore_path.exists(), "❌ vectorstoreフォルダが見つかりません"
    print("✅ vectorstoreフォルダが存在します")
    
    chroma_db = vectorstore_path / "chroma.sqlite3"
    assert chroma_db.exists(), "❌ chroma.sqlite3が見つかりません"
    
    db_size_mb = round(chroma_db.stat().st_size / (1024 * 1024), 2)
    print(f"✅ chroma.sqlite3が存在します (サイズ: {db_size_mb} MB)")
    
    assert db_size_mb > 1, "❌ ベクターストアのサイズが小さすぎます"
    print("✅ ベクターストアのサイズは正常です")
    
    print("✅ テスト2: 合格")


def test_3_data_files_structure():
    """テスト3: dataフォルダの構造確認"""
    print("\n" + "="*60)
    print("テスト3: データファイルの構造確認")
    print("="*60)
    
    data_path = project_root / "data"
    assert data_path.exists(), "❌ dataフォルダが見つかりません"
    print("✅ dataフォルダが存在します")
    
    # 必要なサブフォルダの確認
    required_folders = [
        "01_会社情報",
        "02_事業・サービス",
        "03_社内規程・ルール",
        "04_管理資料"
    ]
    
    for folder in required_folders:
        folder_path = data_path / folder
        assert folder_path.exists(), f"❌ {folder}フォルダが見つかりません"
        print(f"✅ {folder}フォルダが存在します")
    
    # ファイル数のカウント
    total_files = 0
    file_types = {}
    
    for root, dirs, files in os.walk(data_path):
        for file in files:
            total_files += 1
            ext = Path(file).suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
    
    print(f"\n📊 データファイルの統計:")
    print(f"   総ファイル数: {total_files}")
    for ext, count in sorted(file_types.items()):
        print(f"   {ext}: {count}ファイル")
    
    assert total_files > 0, "❌ データファイルが見つかりません"
    print("\n✅ テスト3: 合格")


def test_4_supported_file_formats():
    """テスト4: サポートされているファイル形式の確認"""
    print("\n" + "="*60)
    print("テスト4: サポートファイル形式の確認")
    print("="*60)
    
    import constants as ct
    
    supported = ct.SUPPORTED_EXTENSIONS.keys()
    print(f"サポートされているファイル形式: {len(supported)}種類")
    
    required_formats = ['.pdf', '.docx', '.xlsx', '.pptx', '.md']
    for fmt in required_formats:
        assert fmt in supported, f"❌ {fmt}形式がサポートされていません"
        print(f"✅ {fmt}形式: サポート済み")
    
    # 画像と動画のサポート確認
    image_formats = ['.jpg', '.png', '.gif']
    video_formats = ['.mp4', '.avi', '.mov']
    
    for fmt in image_formats:
        assert fmt in supported, f"❌ 画像形式{fmt}がサポートされていません"
    print(f"✅ 画像形式: サポート済み ({len(image_formats)}種類)")
    
    for fmt in video_formats:
        assert fmt in supported, f"❌ 動画形式{fmt}がサポートされていません"
    print(f"✅ 動画形式: サポート済み ({len(video_formats)}種類)")
    
    print("✅ テスト4: 合格")


def test_5_utils_functions():
    """テスト5: ユーティリティ関数の確認"""
    print("\n" + "="*60)
    print("テスト5: ユーティリティ関数の確認")
    print("="*60)
    
    import utils
    
    # get_source_icon関数のテスト
    test_files = {
        "test.pdf": "📄",
        "test.docx": "📘",
        "test.xlsx": "📊",
        "test.pptx": "📊",
        "test.jpg": "🖼️",
        "test.mp4": "🎥"
    }
    
    for filename, expected_icon in test_files.items():
        icon = utils.get_source_icon(filename)
        assert icon == expected_icon, f"❌ {filename}のアイコンが正しくありません"
        print(f"✅ {filename} → {icon}")
    
    # get_file_type_label関数のテスト
    label_tests = {
        "test.pdf": "PDFファイル",
        "test.xlsx": "Excelファイル",
        "test.pptx": "PowerPointファイル"
    }
    
    for filename, expected_label in label_tests.items():
        label = utils.get_file_type_label(filename)
        assert label == expected_label, f"❌ {filename}のラベルが正しくありません"
        print(f"✅ {filename} → {label}")
    
    print("✅ テスト5: 合格")


def test_6_auth_module():
    """テスト6: 認証モジュールの確認"""
    print("\n" + "="*60)
    print("テスト6: 認証モジュールの確認")
    print("="*60)
    
    import auth
    
    # パスワードハッシュ化のテスト
    password = "test123"
    hashed = auth.hash_password(password)
    assert len(hashed) == 64, "❌ ハッシュ化されたパスワードの長さが正しくありません"
    print(f"✅ パスワードハッシュ化: 正常 (長さ: {len(hashed)})")
    
    # 同じパスワードは同じハッシュになることを確認
    hashed2 = auth.hash_password(password)
    assert hashed == hashed2, "❌ 同じパスワードで異なるハッシュが生成されました"
    print("✅ ハッシュの一貫性: 正常")
    
    # 非推奨関数が使用されていないことを確認
    import inspect
    source = inspect.getsource(auth.get_client_ip)
    assert "_get_websocket_headers" not in source, "❌ 非推奨の関数が使用されています"
    assert "st.context.headers" in source, "❌ 推奨される新しい方法が使用されていません"
    print("✅ 非推奨警告: 修正済み (st.context.headers使用)")
    
    print("✅ テスト6: 合格")


def test_7_constants_configuration():
    """テスト7: 定数設定の確認"""
    print("\n" + "="*60)
    print("テスト7: 定数設定の確認")
    print("="*60)
    
    import constants as ct
    
    # アプリ名の確認
    assert "AI管理部長" in ct.APP_NAME, "❌ アプリ名に「AI管理部長」が含まれていません"
    print(f"✅ アプリ名: {ct.APP_NAME}")
    
    # モード名の確認
    assert "管理部への問い合わせ" == ct.ANSWER_MODE_2, "❌ モード2の名称が正しくありません"
    print(f"✅ モード1: {ct.ANSWER_MODE_1}")
    print(f"✅ モード2: {ct.ANSWER_MODE_2}")
    
    # RAGパラメータの確認
    assert ct.RETRIEVER_SEARCH_K >= 5, "❌ 検索結果数が少なすぎます"
    print(f"✅ 検索結果数: {ct.RETRIEVER_SEARCH_K}")
    
    assert ct.CHUNK_SIZE >= 500, "❌ チャンクサイズが小さすぎます"
    print(f"✅ チャンクサイズ: {ct.CHUNK_SIZE}")
    
    assert ct.CHUNK_OVERLAP >= 50, "❌ チャンクオーバーラップが小さすぎます"
    print(f"✅ チャンクオーバーラップ: {ct.CHUNK_OVERLAP}")
    
    # エラーメッセージの改善確認
    assert "担当部門へ直接問い合わせてください" in ct.SYSTEM_PROMPT_INQUIRY, \
        "❌ エラーメッセージが改善されていません"
    print("✅ エラーメッセージ: 改善済み")
    
    print("✅ テスト7: 合格")


def run_all_tests():
    """すべてのテストを実行"""
    print("\n" + "=" * 60)
    print("[TEST] システム統合テストを開始します")
    print("=" * 60)
    
    tests = [
        test_1_environment_setup,
        test_2_vectorstore_exists,
        test_3_data_files_structure,
        test_4_supported_file_formats,
        test_5_utils_functions,
        test_6_auth_module,
        test_7_constants_configuration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ テスト失敗: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ 予期しないエラー: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print("📊 テスト結果サマリー")
    print("="*60)
    print(f"✅ 合格: {passed}/{len(tests)}")
    print(f"❌ 失敗: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n[SUCCESS] すべてのテストに合格しました！")
        return True
    else:
        print(f"\n[WARNING] {failed}個のテストが失敗しました")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

