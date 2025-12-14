@echo off
chcp 65001 > nul
echo ============================================================
echo 完全無料版への切り替え
echo Google Gemini APIでベクターストアを再作成
echo ============================================================
echo.

echo この作業は、Google Gemini APIの無料枠がリセットされた後
echo （通常、最後に使用してから24時間後）に実行してください。
echo.
echo 24時間経過していない場合、クォータエラーが発生します。
echo.
pause

echo [1/3] 仮想環境をアクティベート中...
call env\Scripts\activate.bat
if errorlevel 1 (
    echo エラー: 仮想環境のアクティベートに失敗しました
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

echo [3/3] ベクターストアを作成中 (Google Gemini API使用)...
echo これには5-10分かかる場合があります。お待ちください...
echo 💰 コスト: 完全無料
echo.
python create_vectorstore_local.py
if errorlevel 1 (
    echo.
    echo エラー: ベクターストアの作成に失敗しました
    echo.
    echo 429エラー（クォータ超過）の場合:
    echo - 24時間待ってから再実行してください
    echo - または、別のGoogleアカウントで新しいAPIキーを作成してください
    echo.
    echo その他のエラーの場合:
    echo - 上記のエラーメッセージを確認してください
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 完了！完全無料版への切り替えが完了しました！
echo ============================================================
echo.
echo 次のステップ:
echo 1. vectorstore\フォルダが作成されたことを確認
echo 2. 以下のコマンドでGitHubにプッシュ:
echo    git add vectorstore\
echo    git commit -m "Switch to free tier (Google Gemini Embeddings)"
echo    git push origin main
echo 3. Streamlit Cloudでアプリを再起動
echo.
echo 💰 今後のコスト: 完全無料！
echo.
pause



