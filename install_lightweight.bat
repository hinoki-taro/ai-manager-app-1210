@echo off
chcp 65001 >nul
echo ========================================
echo 軽量ライブラリセットのインストール
echo ========================================
echo.
echo このスクリプトは、軽量で効率的なライブラリを
echo カテゴリ別にインストールします。
echo.
echo 各セットは約25-100MBで、起動時間への影響は最小限です。
echo.

:menu
echo ----------------------------------------
echo インストールするセットを選択してください:
echo ----------------------------------------
echo  1. 高速テキスト処理（約50MB）
echo  2. 効率的なデータ処理（約40MB）
echo  3. 日本語特化処理（約100MB）★人気
echo  4. Webスクレイピング強化（約60MB）
echo  5. APIクライアント（約30MB）
echo  6. ファイル処理特化（約40MB）
echo  7. パフォーマンス最適化（約35MB）
echo  8. ユーティリティ強化（約25MB）
echo  9. エンタープライズ対応（約45MB）
echo 10. 開発者ツール（約30MB）
echo ----------------------------------------
echo 11. すべてインストール（約455MB）
echo 12. 推奨セット（1,3,7,8のみ 約210MB）★おすすめ
echo  0. キャンセル
echo ----------------------------------------
set /p choice="選択してください (0-12): "

call env\Scripts\activate.bat

if "%choice%"=="1" goto install_01
if "%choice%"=="2" goto install_02
if "%choice%"=="3" goto install_03
if "%choice%"=="4" goto install_04
if "%choice%"=="5" goto install_05
if "%choice%"=="6" goto install_06
if "%choice%"=="7" goto install_07
if "%choice%"=="8" goto install_08
if "%choice%"=="9" goto install_09
if "%choice%"=="10" goto install_10
if "%choice%"=="11" goto install_all
if "%choice%"=="12" goto install_recommended
if "%choice%"=="0" goto end

echo 無効な選択です。
goto menu

:install_01
echo.
echo [セット01] 高速テキスト処理をインストール中...
pip install -r requirements_lightweight_01.txt --quiet
echo ✓ 完了！高速JSON/YAML/CSV処理が使えます
goto success

:install_02
echo.
echo [セット02] 効率的なデータ処理をインストール中...
pip install -r requirements_lightweight_02.txt --quiet
echo ✓ 完了！メモリ効率的なデータ処理が使えます
goto success

:install_03
echo.
echo [セット03] 日本語特化処理をインストール中...
pip install -r requirements_lightweight_03.txt --quiet
echo ✓ 完了！高度な日本語処理が使えます
goto success

:install_04
echo.
echo [セット04] Webスクレイピング強化をインストール中...
pip install -r requirements_lightweight_04.txt --quiet
echo ✓ 完了！効率的なWebスクレイピングが使えます
goto success

:install_05
echo.
echo [セット05] APIクライアントをインストール中...
pip install -r requirements_lightweight_05.txt --quiet
echo ✓ 完了！各種API連携が使えます
goto success

:install_06
echo.
echo [セット06] ファイル処理特化をインストール中...
pip install -r requirements_lightweight_06.txt --quiet
echo ✓ 完了！高度なファイル処理が使えます
goto success

:install_07
echo.
echo [セット07] パフォーマンス最適化をインストール中...
pip install -r requirements_lightweight_07.txt --quiet
echo ✓ 完了！並列処理・非同期処理が使えます
goto success

:install_08
echo.
echo [セット08] ユーティリティ強化をインストール中...
pip install -r requirements_lightweight_08.txt --quiet
echo ✓ 完了！便利なユーティリティが使えます
goto success

:install_09
echo.
echo [セット09] エンタープライズ対応をインストール中...
pip install -r requirements_lightweight_09.txt --quiet
echo ✓ 完了！エンタープライズ機能が使えます
goto success

:install_10
echo.
echo [セット10] 開発者ツールをインストール中...
pip install -r requirements_lightweight_10.txt --quiet
echo ✓ 完了！開発効率化ツールが使えます
goto success

:install_all
echo.
echo [すべて] 全セットをインストール中...
echo これには5-10分かかる場合があります...
for %%f in (requirements_lightweight_*.txt) do (
    echo %%f をインストール中...
    pip install -r %%f --quiet
)
echo ✓ すべてのインストール完了！
goto success

:install_recommended
echo.
echo [推奨セット] セット1,3,7,8をインストール中...
pip install -r requirements_lightweight_01.txt --quiet
echo ✓ セット01完了
pip install -r requirements_lightweight_03.txt --quiet
echo ✓ セット03完了
pip install -r requirements_lightweight_07.txt --quiet
echo ✓ セット07完了
pip install -r requirements_lightweight_08.txt --quiet
echo ✓ セット08完了
echo.
echo ✓ 推奨セットのインストール完了！
goto success

:success
echo.
echo ========================================
echo ✓ インストール完了！
echo ========================================
echo.
goto continue_menu

:continue_menu
echo 他のセットもインストールしますか？
echo 1. メニューに戻る
echo 2. 終了
set /p cont="選択 (1-2): "
if "%cont%"=="1" goto menu
goto end

:end
echo.
pause

