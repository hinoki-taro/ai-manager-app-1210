@echo off
chcp 65001 > nul
echo ============================================================
echo ベクターストア作成 (OpenAI API)
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
    echo OPENAI_API_KEY=sk-proj-...
    echo.
    pause
    exit /b 1
)
echo 完了: .envファイルが見つかりました
echo.

echo [3/3] ベクターストアを作成中 (OpenAI API使用)...
echo これには3-5分かかる場合があります。お待ちください...
echo 💰 推定コスト: 約1-2円程度
echo.
python create_vectorstore_openai.py
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
echo    git add create_vectorstore_openai.py
echo    git commit -m "Add pre-built vectorstore (OpenAI)"
echo    git push origin main
echo 3. Streamlit Cloudでアプリを再起動
echo.
echo 💰 今回のコスト: 約1-2円程度
echo.
pause



