@echo off
chcp 65001 >nul
echo ========================================
echo メディア・VPN機能のインストール
echo ========================================
echo.
echo このスクリプトは、画像・動画閲覧とVPN機能を
echo インストールします。
echo.

:menu
echo ----------------------------------------
echo インストールモードを選択してください:
echo ----------------------------------------
echo 1. 基本版（軽量）- 約80MB
echo    └ 基本的な画像・動画・VPN機能
echo.
echo 2. 完全版 - 約180MB
echo    └ すべての機能（OCR, 動画編集, VPN等）
echo.
echo 3. 画像処理のみ - 約40MB
echo    └ 画像閲覧・編集・QRコード
echo.
echo 4. 動画処理のみ - 約60MB
echo    └ 動画再生・情報取得
echo.
echo 5. VPN機能のみ - 約20MB
echo    └ プロキシ・SSHトンネル
echo.
echo 0. キャンセル
echo ----------------------------------------
set /p choice="選択してください (0-5): "

call env\Scripts\activate.bat

if "%choice%"=="1" goto install_basic
if "%choice%"=="2" goto install_full
if "%choice%"=="3" goto install_image
if "%choice%"=="4" goto install_video
if "%choice%"=="5" goto install_vpn
if "%choice%"=="0" goto end

echo 無効な選択です。
goto menu

:install_basic
echo.
echo [基本版] 軽量版をインストール中...
echo.
pip install -r requirements_media_basic.txt
echo.
echo ✓ 基本版のインストール完了！
echo.
echo インストールされた機能:
echo - 基本的な画像表示・処理
echo - QRコード生成・読み取り
echo - 動画情報取得・再生
echo - プロキシ・SSHトンネル
goto success

:install_full
echo.
echo [完全版] すべての機能をインストール中...
echo これには5-10分かかる場合があります...
echo.
pip install -r requirements_media_vpn.txt
echo.
echo ✓ 完全版のインストール完了！
echo.
echo インストールされた機能:
echo - 高度な画像処理（OCR, RAW, WebP等）
echo - 動画編集・変換
echo - QRコード・バーコード
echo - VPN・プロキシ・SSHトンネル
echo - セキュアブラウジング
echo - ストリーミング機能
goto success

:install_image
echo.
echo [画像処理のみ] インストール中...
pip install Pillow piexif imageio qrcode pyzbar imagehash opencv-python-headless
echo.
echo ✓ 画像処理機能のインストール完了！
goto success

:install_video
echo.
echo [動画処理のみ] インストール中...
pip install pymediainfo yt-dlp vidgear moviepy ffmpeg-python
echo.
echo ✓ 動画処理機能のインストール完了！
goto success

:install_vpn
echo.
echo [VPN機能のみ] インストール中...
pip install PySocks sshtunnel fake-useragent certifi pyopenssl
echo.
echo ✓ VPN機能のインストール完了！
goto success

:success
echo.
echo ========================================
echo インストール完了！
echo ========================================
echo.
echo 使用方法:
echo.
echo 1. メディアビューワー:
echo    streamlit run media_viewer.py
echo.
echo 2. VPNマネージャー:
echo    streamlit run vpn_manager.py
echo.
echo 3. メインアプリに統合する場合:
echo    import media_viewer
echo    import vpn_manager
echo.
goto continue_menu

:continue_menu
echo.
echo 他の機能もインストールしますか？
echo 1. メニューに戻る
echo 2. 終了
set /p cont="選択 (1-2): "
if "%cont%"=="1" goto menu
goto end

:end
echo.
pause

