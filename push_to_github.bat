@echo off
chcp 65001 > nul
echo ============================================================
echo GitHubへのプッシュとタグ作成
echo ============================================================
echo.

echo [ステップ 1/5] 変更をステージング...
git add .
if %errorlevel% neq 0 (
    echo エラー: git add に失敗しました
    pause
    exit /b 1
)
echo ✓ ステージング完了
echo.

echo [ステップ 2/5] コミット作成...
git commit -m "Add OpenAI vectorstore and update all documentation"
if %errorlevel% neq 0 (
    echo 注意: コミットに失敗しました（変更がない場合は正常です）
)
echo.

echo [ステップ 3/5] GitHubにプッシュ...
git push origin main
if %errorlevel% neq 0 (
    echo エラー: git push に失敗しました
    pause
    exit /b 1
)
echo ✓ プッシュ完了
echo.

echo [ステップ 4/5] タグ v1.0.0 を作成...
git tag -a v1.0.0 -m "Version 1.0.0 - OpenAI vectorstore deployment"
if %errorlevel% neq 0 (
    echo 注意: タグ作成に失敗しました（既に存在する場合は正常です）
)
echo.

echo [ステップ 5/5] タグをGitHubにプッシュ...
git push origin v1.0.0
if %errorlevel% neq 0 (
    echo エラー: タグのプッシュに失敗しました
    pause
    exit /b 1
)
echo ✓ タグのプッシュ完了
echo.

echo ============================================================
echo ✅ 完了しました！
echo ============================================================
echo.
echo 次のステップ:
echo 1. GitHubでタグを確認:
echo    https://github.com/hinoki-taro/ai-manager-app-1210/tags
echo.
echo 2. Streamlit Cloudでアプリをデプロイ:
echo    https://share.streamlit.io/
echo.
pause

