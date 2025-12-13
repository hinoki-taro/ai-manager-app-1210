@echo off
chcp 65001 >nul
echo ========================================
echo Google Drive連携のセットアップ
echo ========================================
echo.
echo このスクリプトは、Google Drive連携機能を
echo セットアップします。
echo.

:menu
echo ----------------------------------------
echo セットアップステップ:
echo ----------------------------------------
echo 1. ライブラリのインストール
echo 2. 設定ファイルの作成
echo 3. デモアプリを起動（認証）
echo 4. ガイドを表示
echo ----------------------------------------
echo 0. キャンセル
echo ----------------------------------------
set /p choice="選択してください (0-4): "

if "%choice%"=="1" goto install_libs
if "%choice%"=="2" goto create_config
if "%choice%"=="3" goto run_demo
if "%choice%"=="4" goto show_guide
if "%choice%"=="0" goto end

echo 無効な選択です。
goto menu

:install_libs
echo.
echo [ステップ1] ライブラリをインストール中...
echo.
call env\Scripts\activate.bat
pip install -r requirements_google_drive.txt
echo.
echo ✓ ライブラリのインストール完了！
echo.
goto continue_menu

:create_config
echo.
echo [ステップ2] 設定ファイルを作成中...
echo.

if exist google_drive_config.json (
    echo ⚠ google_drive_config.json は既に存在します。
    echo 上書きしますか？ (Y/N)
    set /p overwrite="選択: "
    if /i not "%overwrite%"=="Y" (
        echo キャンセルしました。
        goto continue_menu
    )
)

copy google_drive_config.json.template google_drive_config.json >nul
echo ✓ google_drive_config.json を作成しました
echo.
echo 📝 次のステップ:
echo 1. google_drive_config.json を開く
echo 2. folder_id を実際のGoogle DriveフォルダIDに変更
echo 3. enabled を true に変更
echo.
goto continue_menu

:run_demo
echo.
echo [ステップ3] デモアプリを起動します...
echo.
echo 📌 重要:
echo 1. 初回起動時にブラウザで認証画面が開きます
echo 2. Googleアカウントでログインしてください
echo 3. 権限を許可してください
echo.

if not exist google_drive_credentials.json (
    echo ⚠ エラー: google_drive_credentials.json が見つかりません！
    echo.
    echo Google Cloud Consoleで認証情報を作成し、
    echo google_drive_credentials.json として配置してください。
    echo.
    echo 詳細は GOOGLE_DRIVE_SETUP.md を参照してください。
    echo.
    goto continue_menu
)

call env\Scripts\activate.bat
streamlit run google_drive_manager.py
goto continue_menu

:show_guide
echo.
echo [ステップ4] セットアップガイド
echo.
echo ========================================
echo Google Drive連携セットアップ手順
echo ========================================
echo.
echo 📋 必要な準備:
echo.
echo 1. Google Cloud Console設定
echo    https://console.cloud.google.com/
echo    - プロジェクトを作成
echo    - Google Drive APIを有効化
echo    - OAuth同意画面を設定
echo    - 認証情報（OAuth クライアント ID）を作成
echo.
echo 2. 認証情報ファイルの配置
echo    - ダウンロードしたJSONをリネーム
echo    - google_drive_credentials.json として保存
echo    - このフォルダに配置
echo.
echo 3. Google DriveフォルダIDの取得
echo    - Google Driveでフォルダを開く
echo    - URLから ID をコピー
echo      例: /folders/1aBcDeFgHiJk...
echo                  ↑ この部分
echo.
echo 4. 設定ファイルの編集
echo    - google_drive_config.json を編集
echo    - folder_id を設定
echo    - enabled を true に設定
echo.
echo 📖 詳細は以下を参照:
echo    GOOGLE_DRIVE_SETUP.md
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
echo セットアップ完了
echo ========================================
echo.
echo 📚 次のステップ:
echo.
echo 1. Google Cloud Consoleで認証情報を作成
echo 2. google_drive_credentials.json を配置
echo 3. google_drive_config.json を編集
echo 4. デモアプリで認証（このスクリプトのオプション3）
echo.
echo 詳細: GOOGLE_DRIVE_SETUP.md
echo デモ: streamlit run google_drive_manager.py
echo.
pause

