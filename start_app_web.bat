@echo off
echo ===============================================
echo   社内情報特化型生成AI検索アプリ 起動スクリプト
echo   WEB公開版（環境変数から読み込み）
echo ===============================================
echo.

REM 環境変数ファイルの確認
if not exist .env (
    echo [ERROR] .env ファイルが見つかりません
    echo.
    echo 以下のコマンドで作成してください：
    echo   copy env_template.txt .env
    echo.
    echo その後、.env ファイルにAPIキーを記入してください。
    echo.
    pause
    exit /b 1
)

echo [1/2] .env ファイルから環境変数を読み込みます
echo.

echo [2/2] アプリを起動します...
echo        ブラウザで http://localhost:8501 が開きます
echo        初回起動は30秒から1分かかります
echo.
echo ★ 停止する場合は Ctrl+C を押してください
echo.

streamlit run main.py

pause

