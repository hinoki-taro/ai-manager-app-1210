"""
このファイルは、最初の画面読み込み時にのみ実行される初期化処理が記述されたファイルです。
"""

############################################################
# ライブラリの読み込み
############################################################
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from uuid import uuid4
import sys
import unicodedata
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st
from docx import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import constants as ct


############################################################
# 設定関連
############################################################
# 「.env」ファイルで定義した環境変数の読み込み
load_dotenv()


############################################################
# 関数定義
############################################################

def initialize():
    """
    画面読み込み時に実行する初期化処理
    """
    # 初期化データの用意
    initialize_session_state()
    # ログ出力用にセッションIDを生成
    initialize_session_id()
    # ログ出力の設定
    initialize_logger()
    # RAGのRetrieverを作成
    initialize_retriever()


def initialize_logger():
    """
    ログ出力の設定
    """
    # 指定のログフォルダが存在すれば読み込み、存在しなければ新規作成
    os.makedirs(ct.LOG_DIR_PATH, exist_ok=True)
    
    # 引数に指定した名前のロガー（ログを記録するオブジェクト）を取得
    # 再度別の箇所で呼び出した場合、すでに同じ名前のロガーが存在していれば読み込む
    logger = logging.getLogger(ct.LOGGER_NAME)

    # すでにロガーにハンドラー（ログの出力先を制御するもの）が設定されている場合、同じログ出力が複数回行われないよう処理を中断する
    if logger.hasHandlers():
        return

    # 1日単位でログファイルの中身をリセットし、切り替える設定
    log_handler = TimedRotatingFileHandler(
        os.path.join(ct.LOG_DIR_PATH, ct.LOG_FILE),
        when="D",
        encoding="utf8"
    )
    # 出力するログメッセージのフォーマット定義
    # - 「levelname」: ログの重要度（INFO, WARNING, ERRORなど）
    # - 「asctime」: ログのタイムスタンプ（いつ記録されたか）
    # - 「lineno」: ログが出力されたファイルの行番号
    # - 「funcName」: ログが出力された関数名
    # - 「session_id」: セッションID（誰のアプリ操作か分かるように）
    # - 「message」: ログメッセージ
    formatter = logging.Formatter(
        f"[%(levelname)s] %(asctime)s line %(lineno)s, in %(funcName)s, session_id={st.session_state.session_id}: %(message)s"
    )

    # 定義したフォーマッターの適用
    log_handler.setFormatter(formatter)

    # ログレベルを「INFO」に設定
    logger.setLevel(logging.INFO)

    # 作成したハンドラー（ログ出力先を制御するオブジェクト）を、
    # ロガー（ログメッセージを実際に生成するオブジェクト）に追加してログ出力の最終設定
    logger.addHandler(log_handler)


def initialize_session_id():
    """
    セッションIDの作成
    """
    if "session_id" not in st.session_state:
        # ランダムな文字列（セッションID）を、ログ出力用に作成
        st.session_state.session_id = uuid4().hex


def initialize_retriever():
    """
    画面読み込み時にRAGのRetriever（ベクターストアから検索するオブジェクト）を作成
    
    既存のベクターストアがあればそれを読み込み、なければエラーを表示
    """
    # ロガーを読み込むことで、後続の処理中に発生したエラーなどがログファイルに記録される
    logger = logging.getLogger(ct.LOGGER_NAME)

    # すでにRetrieverが作成済みの場合、後続の処理を中断
    if "retriever" in st.session_state:
        return
    
    try:
        # ベクターストアのパス
        vectorstore_path = "./vectorstore"
        
        # 既存のベクターストアが存在するか確認
        if os.path.exists(vectorstore_path):
            # 既存のベクターストアを読み込む
            # ベクターストアを読み込み中（ログのみ）
            logger.info("事前作成されたベクターストアを読み込んでいます")
            
            # APIキーの取得（どちらのAPIキーが設定されているかを確認）
            openai_api_key = os.getenv("OPENAI_API_KEY")
            google_api_key = os.getenv("GOOGLE_API_KEY")
            
            # Streamlit Secretsからも取得を試みる
            if not openai_api_key and "OPENAI_API_KEY" in st.secrets:
                openai_api_key = st.secrets["OPENAI_API_KEY"]
            if not google_api_key and "GOOGLE_API_KEY" in st.secrets:
                google_api_key = st.secrets["GOOGLE_API_KEY"]
            
            # ベクターストアはOpenAI Embeddingsで作成されているため、
            # 読み込み時もOpenAI Embeddingsを使用する必要があります
            if openai_api_key:
                logger.info("OpenAI Embeddings を使用してベクターストアを読み込みます")
                from langchain_openai import OpenAIEmbeddings
                embeddings = OpenAIEmbeddings(
                    model=ct.EMBEDDING_MODEL_OPENAI,
                    openai_api_key=openai_api_key
                )
            else:
                st.error("""
                ❌ **OpenAI APIキーが見つかりません**
                
                このベクターストアはOpenAI Embeddingsで作成されています。
                読み込むには以下のいずれかの対応が必要です：
                
                1. **Streamlit SecretsにOpenAI APIキーを追加**（推奨）
                   - Settings → Secrets で `OPENAI_API_KEY = "sk-..."` を追加
                   - 読み込み時のみ使用（費用はほぼゼロ）
                
                2. **ベクターストアをGemini Embeddingsで再作成**（完全無料）
                   - ローカルで `switch_to_free.bat` を実行
                   - GitHubにプッシュして再デプロイ
                """)
                raise ValueError("OPENAI_API_KEY が設定されていません。ベクターストアの読み込みに失敗しました。")
                st.write("利用可能なSecretsのキー:", list(st.secrets.keys()))
                raise ValueError(
                    "OPENAI_API_KEY または GOOGLE_API_KEY が設定されていません。\n"
                    "Streamlit CloudのSecretsで設定してください。"
                )
            
            # 既存のベクターストアを読み込み
            db = Chroma(
                persist_directory=vectorstore_path,
                embedding_function=embeddings
            )
            
            # ベクターストアの内容を確認（デバッグ用）
            try:
                collection = db._collection
                doc_count = collection.count()
                logger.info(f"ベクターストア内のドキュメント数: {doc_count}件")
                
                if doc_count == 0:
                    st.error("⚠️ ベクターストアが空です！ベクターストアを再作成する必要があります。")
                else:
                    logger.info(f"ベクターストアの読み込みが完了しました（{doc_count}件のドキュメント）")
            except Exception as e:
                st.warning(f"ベクターストアの確認中にエラー: {e}")
                logger.info("ベクターストアの読み込みが完了しました")
            
            # ベクターストアを検索するRetrieverの作成
            st.session_state.retriever = db.as_retriever(search_kwargs={"k": ct.RETRIEVER_SEARCH_K})
            # 初期化完了（ログのみ）
            logger.info("ベクターストアを読み込みました")
            
        else:
            # ベクターストアが存在しない場合はエラー
            error_msg = (
                "ベクターストアが見つかりません。\n\n"
                "ローカル環境で以下を実行してください:\n"
                "1. python create_vectorstore_local.py\n"
                "2. git add vectorstore/\n"
                "3. git commit -m 'Add vectorstore'\n"
                "4. git push origin main\n"
                "5. Streamlit Cloudでアプリを再起動"
            )
            st.error(f"❌ {error_msg}")
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
    except Exception as e:
        error_msg = f"初期化中にエラーが発生しました: {str(e)}"
        logger.error(error_msg, exc_info=True)
        st.error(f"❌ {error_msg}")
        st.error("詳細なエラー情報:")
        st.exception(e)
        raise


def initialize_session_state():
    """
    初期化データの用意
    """
    if "messages" not in st.session_state:
        # 「表示用」の会話ログを順次格納するリストを用意
        st.session_state.messages = []
        # 「LLMとのやりとり用」の会話ログを順次格納するリストを用意
        st.session_state.chat_history = []
    
    # モードの初期値を「社内問い合わせ」に設定
    if "mode" not in st.session_state:
        st.session_state.mode = ct.ANSWER_MODE_2  # 「社内問い合わせ」


def load_data_sources():
    """
    RAGの参照先となるデータソースの読み込み

    Returns:
        読み込んだ通常データソース
    """
    # データソースを格納する用のリスト
    docs_all = []
    
    # 複数のフォルダから読み込む
    for folder_path in ct.RAG_FOLDER_PATHS:
        if os.path.exists(folder_path):
            print(f"📂 読み込み中: {folder_path}")
            recursive_file_check(folder_path, docs_all)
        else:
            print(f"⚠️ フォルダが見つかりません: {folder_path}")

    web_docs_all = []
    # ファイルとは別に、指定のWebページ内のデータも読み込み
    # 読み込み対象のWebページ一覧に対して処理
    for web_url in ct.WEB_URL_LOAD_TARGETS:
        # 指定のWebページを読み込み
        loader = WebBaseLoader(web_url)
        web_docs = loader.load()
        # for文の外のリストに読み込んだデータソースを追加
        web_docs_all.extend(web_docs)
    # 通常読み込みのデータソースにWebページのデータを追加
    docs_all.extend(web_docs_all)

    return docs_all


def recursive_file_check(path, docs_all):
    """
    RAGの参照先となるデータソースの読み込み

    Args:
        path: 読み込み対象のファイル/フォルダのパス
        docs_all: データソースを格納する用のリスト
    """
    # パスがフォルダかどうかを確認
    if os.path.isdir(path):
        # フォルダの場合、フォルダ内のファイル/フォルダ名の一覧を取得
        files = os.listdir(path)
        # 各ファイル/フォルダに対して処理
        for file in files:
            # ファイル/フォルダ名だけでなく、フルパスを取得
            full_path = os.path.join(path, file)
            # フルパスを渡し、再帰的にファイル読み込みの関数を実行
            recursive_file_check(full_path, docs_all)
    else:
        # パスがファイルの場合、ファイル読み込み
        file_load(path, docs_all)


def file_load(path, docs_all):
    """
    ファイル内のデータ読み込み

    Args:
        path: ファイルパス
        docs_all: データソースを格納する用のリスト
    """
    # ファイルの拡張子を取得
    file_extension = os.path.splitext(path)[1]
    # ファイル名（拡張子を含む）を取得
    file_name = os.path.basename(path)

    # 想定していたファイル形式の場合のみ読み込む
    if file_extension in ct.SUPPORTED_EXTENSIONS:
        # Excelファイルの場合は特別な処理
        if file_extension in ['.xlsx', '.xls']:
            try:
                import pandas as pd
                from langchain.docstore.document import Document
                
                # Excelファイルを読み込む
                df = pd.read_excel(path)
                
                # DataFrameを文字列に変換
                content = df.to_string(index=False)
                
                # ドキュメントとして追加
                doc = Document(
                    page_content=content,
                    metadata={"source": path}
                )
                docs_all.append(doc)
            except Exception as e:
                print(f"Warning: Failed to load Excel file {path}: {e}")
        # PowerPointファイルの場合は特別な処理
        elif file_extension in ['.pptx', '.ppt']:
            try:
                from pptx import Presentation
                from langchain.docstore.document import Document
                
                # PowerPointファイルを読み込む
                prs = Presentation(path)
                
                # テキストを抽出
                text_content = []
                for slide_num, slide in enumerate(prs.slides, 1):
                    slide_text = f"\n--- Slide {slide_num} ---\n"
                    for shape in slide.shapes:
                        if hasattr(shape, "text"):
                            slide_text += shape.text + "\n"
                    text_content.append(slide_text)
                
                content = "\n".join(text_content)
                
                # ドキュメントとして追加
                doc = Document(
                    page_content=content,
                    metadata={"source": path}
                )
                docs_all.append(doc)
            except Exception as e:
                print(f"Warning: Failed to load PowerPoint file {path}: {e}")
        # 画像ファイルの場合は特別な処理
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            try:
                from langchain.docstore.document import Document
                
                # ファイルのメタデータを取得
                file_stat = os.stat(path)
                file_size_kb = round(file_stat.st_size / 1024, 2)
                modified_time = datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                
                # ファイル名から情報を抽出
                file_name_only = os.path.splitext(os.path.basename(path))[0]
                
                # メタデータをテキスト化
                content = f"""画像ファイル: {file_name_only}
ファイル形式: {file_extension.upper()}
ファイルパス: {path}
ファイルサイズ: {file_size_kb} KB
最終更新日時: {modified_time}

このファイルは画像ファイルです。
ファイル名: {file_name_only}
"""
                
                # ドキュメントとして追加
                doc = Document(
                    page_content=content,
                    metadata={"source": path, "type": "image"}
                )
                docs_all.append(doc)
            except Exception as e:
                print(f"Warning: Failed to load image file {path}: {e}")
        # 動画ファイルの場合は特別な処理
        elif file_extension in ['.mp4', '.avi', '.mov', '.wmv', '.mkv']:
            try:
                from langchain.docstore.document import Document
                
                # ファイルのメタデータを取得
                file_stat = os.stat(path)
                file_size_mb = round(file_stat.st_size / (1024 * 1024), 2)
                modified_time = datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                
                # ファイル名から情報を抽出
                file_name_only = os.path.splitext(os.path.basename(path))[0]
                
                # メタデータをテキスト化
                content = f"""動画ファイル: {file_name_only}
ファイル形式: {file_extension.upper()}
ファイルパス: {path}
ファイルサイズ: {file_size_mb} MB
最終更新日時: {modified_time}

このファイルは動画ファイルです。
ファイル名: {file_name_only}
"""
                
                # ドキュメントとして追加
                doc = Document(
                    page_content=content,
                    metadata={"source": path, "type": "video"}
                )
                docs_all.append(doc)
            except Exception as e:
                print(f"Warning: Failed to load video file {path}: {e}")
        else:
            # ファイルの拡張子に合ったdata loaderを使ってデータ読み込み
            if ct.SUPPORTED_EXTENSIONS[file_extension] is not None:
                loader = ct.SUPPORTED_EXTENSIONS[file_extension](path)
                docs = loader.load()
                docs_all.extend(docs)


def adjust_string(s):
    """
    Windows環境でRAGが正常動作するよう調整
    
    Args:
        s: 調整を行う文字列
    
    Returns:
        調整を行った文字列
    """
    # 調整対象は文字列のみ
    if type(s) is not str:
        return s

    # OSがWindowsの場合、Unicode正規化と、cp932（Windows用の文字コード）で表現できない文字を除去
    if sys.platform.startswith("win"):
        s = unicodedata.normalize('NFC', s)
        s = s.encode("cp932", "ignore").decode("cp932")
        return s
    
    # OSがWindows以外の場合はそのまま返す
    return s