@echo off
chcp 65001 > nul
echo ============================================================
echo ベクターストア作成バッチスクリプト
echo ============================================================
echo.

echo [1/3] 仮想環境をアクティベート中...
call env\Scripts\activate.bat
if errorlevel 1 (
    echo エラー: 仮想環境のアクティベートに失敗しました
    echo env\Scripts\activate.bat が存在することを確認してください
    pause
    exit /b 1
)
echo 完了: 仮想環境をアクティベートしました
echo.

echo [2/3] .envファイルを確認中...
if not exist .env (
    echo 警告: .envファイルが見つかりません
    echo プロジェクトのルートに.envファイルを作成してください
    echo.
    echo 内容:
    echo GOOGLE_API_KEY=AIzaSyBlp0GgqOrY5VLVP703PKk-J1UKuDHuhKQ
    echo.
    pause
    exit /b 1
)
echo 完了: .envファイルが見つかりました
echo.

echo [3/3] ベクターストアを作成中...
echo これには5-10分かかる場合があります。お待ちください...
echo.
python create_vectorstore_local.py
if errorlevel 1 (
    echo.
    echo エラー: ベクターストアの作成に失敗しました
    echo 上記のエラーメッセージを確認してください
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 完了しました！
echo ============================================================
echo.
echo 次のステップ:
echo 1. vectorstore\フォルダが作成されたことを確認
echo 2. 以下のコマンドでGitHubにプッシュ:
echo    git add vectorstore\
echo    git add initialize.py
echo    git add create_vectorstore_local.py
echo    git commit -m "Add pre-built vectorstore"
echo    git push origin main
echo 3. Streamlit Cloudでアプリを再起動
echo.
pause



