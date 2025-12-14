@echo off
chcp 65001 > nul
echo ============================================================
echo バージョンタグの作成とプッシュ
echo ============================================================
echo.

echo [1/2] バージョンタグを作成中...
git tag -a v1.0.0 -m "Version 1.0.0 - Complete Free Tier Support"
if errorlevel 1 (
    echo エラー: タグの作成に失敗しました
    echo 既にタグが存在する可能性があります
    echo.
    echo 既存のタグを削除して再作成する場合:
    echo   git tag -d v1.0.0
    echo   git push origin :refs/tags/v1.0.0
    echo.
    pause
    exit /b 1
)
echo 完了: タグ v1.0.0 を作成しました
echo.

echo [2/2] タグをGitHubにプッシュ中...
git push origin v1.0.0
if errorlevel 1 (
    echo エラー: タグのプッシュに失敗しました
    pause
    exit /b 1
)
echo 完了: タグをGitHubにプッシュしました
echo.

echo ============================================================
echo 完了！
echo ============================================================
echo.
echo 確認してください:
echo https://github.com/hinoki-taro/ai-manager-app-1210/tags
echo.
pause



