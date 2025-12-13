@echo off
chcp 65001 >nul
echo ========================================
echo Gemini版に切り替えます
echo ========================================

echo.
echo [1/3] 現在のファイルをバックアップ中...
if exist utils.py (
    copy utils.py utils_openai_backup.py >nul
    echo ✓ utils.pyをバックアップ
)
if exist initialize.py (
    copy initialize.py initialize_openai_backup.py >nul
    echo ✓ initialize.pyをバックアップ
)

echo.
echo [2/3] Gemini版のファイルを復元中...
if exist utils_gemini_backup.py (
    copy utils_gemini_backup.py utils.py >nul
    echo ✓ utils.pyを復元
) else (
    echo ⚠ バックアップが見つかりません。Gitから復元してください。
    echo   コマンド: git checkout utils.py
)

if exist initialize_gemini_backup.py (
    copy initialize_gemini_backup.py initialize.py >nul
    echo ✓ initialize.pyを復元
) else (
    echo ⚠ バックアップが見つかりません。Gitから復元してください。
    echo   コマンド: git checkout initialize.py
)

echo.
echo [3/3] 完了！
echo.
echo ========================================
echo 次のステップ:
echo 1. .envファイルを編集してGOOGLE_API_KEYを設定
echo    例: GOOGLE_API_KEY=AIzaSyxxxxxxxxxx
echo 2. streamlit run main.py でアプリを起動
echo ========================================
echo.
echo Google Gemini APIキーの取得方法:
echo https://aistudio.google.com/app/apikey
echo.

pause

