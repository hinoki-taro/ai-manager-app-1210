@echo off
chcp 65001 >nul
echo ========================================
echo 拡張ライブラリのインストール
echo ========================================
echo.
echo このスクリプトは、将来的に必要になる可能性のある
echo 拡張ライブラリをインストールします。
echo.
echo 注意: インストールには15-30分程度かかる場合があります。
echo.

:menu
echo ----------------------------------------
echo インストールモードを選択してください:
echo ----------------------------------------
echo 1. すべての拡張ライブラリをインストール
echo 2. カテゴリ別にインストール
echo 3. 推奨ライブラリのみインストール（軽量）
echo 4. キャンセル
echo ----------------------------------------
set /p choice="選択してください (1-4): "

if "%choice%"=="1" goto install_all
if "%choice%"=="2" goto category_menu
if "%choice%"=="3" goto install_recommended
if "%choice%"=="4" goto end

echo 無効な選択です。もう一度お試しください。
goto menu

:install_all
echo.
echo ========================================
echo すべての拡張ライブラリをインストール中...
echo ========================================
call env\Scripts\activate.bat
pip install -r requirements_extended.txt
goto success

:category_menu
echo.
echo ----------------------------------------
echo カテゴリを選択してください:
echo ----------------------------------------
echo 1. ドキュメント処理拡張（PowerPoint, Excel, OCR）
echo 2. データベース接続（PostgreSQL, MySQL, MongoDB）
echo 3. API・ネットワーク（FastAPI, Selenium）
echo 4. セキュリティ（暗号化, JWT, bcrypt）
echo 5. データ分析・可視化（matplotlib, plotly）
echo 6. 自然言語処理拡張（spacy, sentence-transformers）
echo 7. ベクトルデータベース拡張（Pinecone, Qdrant）
echo 8. 音声処理（音声認識, 音声合成）
echo 9. テスト・品質管理（pytest, black）
echo 0. メインメニューに戻る
echo ----------------------------------------
set /p cat_choice="選択してください (0-9): "

call env\Scripts\activate.bat

if "%cat_choice%"=="1" (
    echo ドキュメント処理拡張をインストール中...
    pip install python-pptx openpyxl xlsxwriter xlrd markdown Pillow pdf2image pytesseract
    goto success
)
if "%cat_choice%"=="2" (
    echo データベース接続をインストール中...
    pip install psycopg2-binary pymysql sqlalchemy pymongo
    goto success
)
if "%cat_choice%"=="3" (
    echo API・ネットワークをインストール中...
    pip install requests httpx fastapi uvicorn selenium lxml
    goto success
)
if "%cat_choice%"=="4" (
    echo セキュリティをインストール中...
    pip install cryptography pyjwt bcrypt
    goto success
)
if "%cat_choice%"=="5" (
    echo データ分析・可視化をインストール中...
    pip install matplotlib seaborn plotly altair scipy
    goto success
)
if "%cat_choice%"=="6" (
    echo 自然言語処理拡張をインストール中...
    pip install nltk spacy sentence-transformers ftfy
    echo.
    echo 日本語モデルをダウンロードしますか？ (Y/N)
    set /p dl_ja="選択: "
    if /i "%dl_ja%"=="Y" python -m spacy download ja_core_news_sm
    goto success
)
if "%cat_choice%"=="7" (
    echo ベクトルデータベース拡張をインストール中...
    pip install pinecone-client weaviate-client qdrant-client faiss-cpu
    goto success
)
if "%cat_choice%"=="8" (
    echo 音声処理をインストール中...
    pip install SpeechRecognition pydub gtts
    goto success
)
if "%cat_choice%"=="9" (
    echo テスト・品質管理をインストール中...
    pip install pytest pytest-cov black isort flake8 mypy
    goto success
)
if "%cat_choice%"=="0" goto menu

echo 無効な選択です。
goto category_menu

:install_recommended
echo.
echo ========================================
echo 推奨ライブラリをインストール中...
echo ========================================
call env\Scripts\activate.bat
pip install python-pptx openpyxl requests fastapi pydantic cryptography loguru pytest matplotlib
goto success

:success
echo.
echo ========================================
echo ✓ インストール完了！
echo ========================================
echo.
echo インストールされたライブラリを確認:
pip list
echo.
goto end

:end
echo.
pause

