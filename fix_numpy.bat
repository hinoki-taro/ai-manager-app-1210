@echo off
chcp 65001 > nul
echo ============================================================
echo NumPy 1.x系へのダウングレード
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

echo [2/2] NumPyをダウングレード中...
echo 現在のNumPyをアンインストールしています...
pip uninstall numpy -y
echo.
echo NumPy 1.x系をインストールしています...
pip install "numpy<2.0.0"
echo.

echo ============================================================
echo 完了！
echo ============================================================
echo.
echo 確認:
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
echo.
echo NumPyのバージョンが 1.x.x であることを確認してください。
echo.
echo 次のステップ:
echo create_vectorstore.bat を再度実行してください
echo.
pause

