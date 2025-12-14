@echo off
chcp 65001 >nul
echo ========================================
echo Streamlit Community Cloud デプロイ準備
echo ========================================
echo.

:menu
echo ----------------------------------------
echo デプロイ準備メニュー:
echo ----------------------------------------
echo 1. デプロイ前チェック
echo 2. GitHubリポジトリの初期化
echo 3. コードをGitHubにプッシュ
echo 4. Streamlit Community Cloudを開く
echo 5. デプロイガイドを表示
echo ----------------------------------------
echo 0. 終了
echo ----------------------------------------
set /p choice="選択してください (0-5): "

if "%choice%"=="1" goto check
if "%choice%"=="2" goto git_init
if "%choice%"=="3" goto git_push
if "%choice%"=="4" goto open_streamlit
if "%choice%"=="5" goto show_guide
if "%choice%"=="0" goto end

echo 無効な選択です。
goto menu

:check
echo.
echo [ステップ1] デプロイ前チェック
echo.
echo [1] .gitignoreの確認...
if exist .gitignore (
    echo [OK] .gitignore が存在します
) else (
    echo [NG] .gitignore が見つかりません
)

echo [2] requirements.txtの確認...
if exist requirements.txt (
    echo [OK] requirements.txt が存在します
) else (
    echo [NG] requirements.txt が見つかりません
)

echo [3] main.pyの確認...
if exist main.py (
    echo [OK] main.py が存在します
) else (
    echo [NG] main.py が見つかりません
)

echo [4] .streamlit/config.tomlの確認...
if exist .streamlit\config.toml (
    echo [OK] .streamlit/config.toml が存在します
) else (
    echo [NG] .streamlit/config.toml が見つかりません
)

echo [5] .streamlit/secrets.tomlの確認...
if exist .streamlit\secrets.toml (
    echo [OK] .streamlit/secrets.toml が存在します（デプロイ時は手動設定が必要）
) else (
    echo [!!] .streamlit/secrets.toml が見つかりません
    echo      Streamlit Community CloudのSecretsに直接設定してください
)

echo.
echo チェック完了
echo.
goto continue_menu

:git_init
echo.
echo [ステップ2] GitHubリポジトリの初期化
echo.
echo Gitリポジトリを初期化しますか？
echo 既にリポジトリが初期化されている場合はスキップしてください。
set /p confirm="初期化しますか？ (Y/n): "

if /i "%confirm%"=="n" (
    echo キャンセルしました
    goto continue_menu
)

git init
git branch -M main
echo.
echo GitHubでリポジトリを作成してください:
echo 1. https://github.com/new にアクセス
echo 2. Repository name: ai-search-app
echo 3. Private を選択
echo 4. Create repository をクリック
echo.
echo リポジトリのURLを入力してください:
echo 例: https://github.com/your-username/ai-search-app.git
set /p repo_url="リポジトリURL: "

git remote add origin %repo_url%
echo.
echo [OK] リポジトリを設定しました
echo.
goto continue_menu

:git_push
echo.
echo [ステップ3] コードをGitHubにプッシュ
echo.
echo 注意: .streamlit/secrets.toml は除外されます
echo.

git add .
git commit -m "Initial commit: AI search app with Google Drive integration"
git push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo [OK] GitHubにプッシュしました
) else (
    echo [NG] プッシュに失敗しました
    echo Git認証情報を確認してください
)
echo.
goto continue_menu

:open_streamlit
echo.
echo [ステップ4] Streamlit Community Cloudを開きます...
echo.
start https://share.streamlit.io/
echo.
echo ブラウザでStreamlit Community Cloudが開きました
echo.
echo 次の手順:
echo 1. GitHubアカウントでログイン
echo 2. New app をクリック
echo 3. リポジトリを選択
echo 4. Branch: main
echo 5. Main file path: main.py
echo 6. Advanced settings → Secrets に設定を追加
echo 7. Deploy をクリック
echo.
goto continue_menu

:show_guide
echo.
echo [ステップ5] デプロイガイド
echo.
echo ========================================
echo Streamlit Community Cloud デプロイ手順
echo ========================================
echo.
echo 1. GitHubリポジトリの準備
echo    - このメニューの「2」でリポジトリを初期化
echo    - このメニューの「3」でコードをプッシュ
echo.
echo 2. Streamlit Community Cloudでデプロイ
echo    - https://share.streamlit.io/ にアクセス
echo    - New app をクリック
echo    - リポジトリを選択
echo    - main.py を指定
echo.
echo 3. Secretsの設定
echo    Settings → Secrets で以下を設定:
echo.
echo    GOOGLE_API_KEY = "your-api-key"
echo.
echo    [passwords]
echo    admin = "your-password-hash"
echo.
echo    [google_drive_service_account]
echo    type = "service_account"
echo    project_id = "your-project-id"
echo    # ... (サービスアカウントJSONの内容)
echo.
echo 4. デプロイ完了
echo    Deploy ボタンをクリック
echo.
echo 詳細: WEB_DEPLOYMENT_WITH_GOOGLE_DRIVE.md
echo.
goto continue_menu

:continue_menu
echo.
echo 他のステップを実行しますか？
echo 1. メニューに戻る
echo 2. 終了
set /p cont="選択 (1-2): "
if "%cont%"=="1" goto menu
goto end

:end
echo.
echo ========================================
echo デプロイ準備完了
echo ========================================
echo.
echo 次のステップ:
echo 1. GitHubにコードをプッシュ
echo 2. Streamlit Community Cloudでデプロイ
echo 3. Secretsを設定
echo 4. アプリが公開される
echo.
echo 詳細: WEB_DEPLOYMENT_WITH_GOOGLE_DRIVE.md
echo.
pause



