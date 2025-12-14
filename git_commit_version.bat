@echo off
chcp 65001 > nul
echo ============================================================
echo Gitバージョン管理
echo v1.0.0 - 完全無料運用対応版
echo ============================================================
echo.

echo [1/4] すべての変更をステージング中...
git add .
if errorlevel 1 (
    echo エラー: git add に失敗しました
    pause
    exit /b 1
)
echo 完了: すべての変更をステージングしました
echo.

echo [2/4] コミット中...
git commit -m "v1.0.0: Add vectorstore and free tier migration tools

Features:
- Add pre-built vectorstore with OpenAI Embeddings
- Add automatic API switching (OpenAI/Google Gemini)
- Add free tier migration tools and documentation
- Update initialize.py to support both embedding models
- Add comprehensive documentation for deployment and operation

Files added:
- create_vectorstore_openai.py/bat
- create_vectorstore_local.py
- switch_to_free.bat
- install_langchain_openai.bat
- fix_numpy.bat
- FREE_TIER_MIGRATION_GUIDE.md
- FUTURE_OPERATION_GUIDE.md
- VECTORSTORE_SETUP_GUIDE.md
- COMPLETE_FREE_SETUP_SUMMARY.md
- STREAMLIT_NEW_APP_DEPLOY_GUIDE.md
- vectorstore/ (pre-built)

Files modified:
- initialize.py (automatic API switching)
- constants.py (embedding model definitions)
- requirements.txt (add langchain-openai)

Cost: ~1-2 yen for initial vectorstore creation
Future: Free tier operation with Google Gemini API"

if errorlevel 1 (
    echo エラー: git commit に失敗しました
    pause
    exit /b 1
)
echo 完了: コミットしました
echo.

echo [3/4] バージョンタグを作成中...
git tag -a v1.0.0 -m "Version 1.0.0 - Complete Free Tier Support

Major Features:
- Pre-built vectorstore for quota-free startup
- Automatic API switching (OpenAI/Google Gemini)
- Complete free tier migration support
- Comprehensive documentation

Cost Model:
- Current: OpenAI Embeddings (~360 yen/year)
- Future: Google Gemini Embeddings (completely free)

Target: 株式会社エムエムインターナショナル
App: mmi-ai-manager
Date: 2025-12-13"

if errorlevel 1 (
    echo エラー: git tag に失敗しました
    pause
    exit /b 1
)
echo 完了: バージョンタグ v1.0.0 を作成しました
echo.

echo [4/4] GitHubにプッシュ中...
echo コミットをプッシュしています...
git push origin main
if errorlevel 1 (
    echo エラー: git push に失敗しました
    pause
    exit /b 1
)
echo.
echo タグをプッシュしています...
git push origin v1.0.0
if errorlevel 1 (
    echo エラー: git push (tag) に失敗しました
    pause
    exit /b 1
)
echo 完了: GitHubにプッシュしました
echo.

echo ============================================================
echo 完了！バージョン管理が完了しました
echo ============================================================
echo.
echo バージョン情報:
echo - バージョン: v1.0.0
echo - 日付: 2025年12月13日
echo - 内容: 完全無料運用対応版
echo.
echo GitHubで確認:
echo https://github.com/hinoki-taro/ai-manager-app-1210
echo.
echo 次のステップ:
echo 1. Streamlit Cloudでアプリを再起動
echo 2. 動作確認
echo.
pause



