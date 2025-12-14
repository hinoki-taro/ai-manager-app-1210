@echo off
chcp 65001 > nul
echo ============================================================
echo langchain-openai インストール
echo ============================================================
echo.

echo [1/2] 仮想環境をアクティベート中...
call env\Scripts\activate.bat
if errorlevel 1 (
    echo エラー: 仮想環境のアクティベートに失敗しました
    pause
    exit /b 1
)
echo 完了: 仮想環境をアクティベートしました
echo.

echo [2/2] langchain-openai をインストール中...
pip install langchain-openai==0.3.3
if errorlevel 1 (
    echo エラー: インストールに失敗しました
    pause
    exit /b 1
)
echo.

echo ============================================================
echo 完了！
echo ============================================================
echo.
echo 確認:
python -c "from langchain_openai import OpenAIEmbeddings; print('langchain-openai: インストール済み')"
echo.
echo 次のステップ:
echo .envファイルにOPENAI_API_KEYを設定してください
echo.
pause



