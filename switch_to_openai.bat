@echo off
chcp 65001 >nul
echo ========================================
echo OpenAI版に切り替えます
echo ========================================

echo.
echo [1/4] 現在のファイルをバックアップ中...
copy utils.py utils_gemini_backup.py >nul
copy initialize.py initialize_gemini_backup.py >nul
echo ✓ バックアップ完了

echo.
echo [2/4] OpenAI版のファイルをコピー中...
copy openai_version\utils_openai.py utils.py >nul
copy openai_version\initialize_openai.py initialize.py >nul
echo ✓ ファイルコピー完了

echo.
echo [3/4] パッケージをインストール中...
call env\Scripts\activate.bat
pip install langchain-openai --quiet
echo ✓ パッケージインストール完了

echo.
echo [4/4] 完了！
echo.
echo ========================================
echo 次のステップ:
echo 1. .envファイルを編集してOPENAI_API_KEYを設定
echo    例: OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
echo 2. streamlit run main.py でアプリを起動
echo ========================================
echo.
echo OpenAI APIキーの取得方法:
echo https://platform.openai.com/api-keys
echo.

pause

