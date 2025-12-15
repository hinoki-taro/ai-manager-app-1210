"""
このファイルは、画面表示以外の様々な関数定義のファイルです。
"""

############################################################
# ライブラリの読み込み
############################################################
import os
import time
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import constants as ct
from langchain_enhanced import (
    get_rate_limiter,
    # get_query_cache,  # キャッシュ機能を無効化
    get_langchain_logger,
    get_conversation_manager,
    InputValidator,
    ErrorHandler,
    StreamHandler
)


############################################################
# 設定関連
############################################################
# 「.env」ファイルで定義した環境変数の読み込み
load_dotenv()


############################################################
# 関数定義
############################################################

def get_source_icon(source):
    """
    メッセージと一緒に表示するアイコンの種類を取得

    Args:
        source: 参照元のありか

    Returns:
        メッセージと一緒に表示するアイコンの種類
    """
    # 参照元がWebページの場合
    if source.startswith("http"):
        return ct.LINK_SOURCE_ICON
    
    # ファイルの場合、拡張子に応じてアイコンを変更
    import os
    ext = os.path.splitext(source)[1].lower()
    
    # ファイル形式ごとのアイコンマッピング
    icon_map = {
        ".pdf": "📄",
        ".docx": "📘",
        ".doc": "📘",
        ".xlsx": "📊",
        ".xls": "📊",
        ".csv": "📊",
        ".pptx": "📊",
        ".ppt": "📊",
        ".txt": "📝",
        ".md": "📝",
        ".jpg": "🖼️",
        ".jpeg": "🖼️",
        ".png": "🖼️",
        ".gif": "🖼️",
        ".bmp": "🖼️",
        ".webp": "🖼️",
        ".mp4": "🎥",
        ".avi": "🎥",
        ".mov": "🎥",
        ".wmv": "🎥",
        ".mkv": "🎥"
    }
    
    return icon_map.get(ext, ct.DOC_SOURCE_ICON)


def get_file_type_label(source):
    """
    ファイルの種類ラベルを取得

    Args:
        source: 参照元のありか

    Returns:
        ファイルの種類ラベル（例: "PDFファイル", "Excelファイル"）
    """
    import os
    ext = os.path.splitext(source)[1].lower()
    
    # ファイル形式ごとのラベルマッピング
    type_map = {
        ".pdf": "PDFファイル",
        ".docx": "Wordファイル",
        ".doc": "Wordファイル",
        ".xlsx": "Excelファイル",
        ".xls": "Excelファイル",
        ".csv": "CSVファイル",
        ".pptx": "PowerPointファイル",
        ".ppt": "PowerPointファイル",
        ".txt": "テキストファイル",
        ".md": "Markdownファイル",
        ".jpg": "画像ファイル",
        ".jpeg": "画像ファイル",
        ".png": "画像ファイル",
        ".gif": "画像ファイル",
        ".bmp": "画像ファイル",
        ".webp": "画像ファイル",
        ".mp4": "動画ファイル",
        ".avi": "動画ファイル",
        ".mov": "動画ファイル",
        ".wmv": "動画ファイル",
        ".mkv": "動画ファイル"
    }
    
    return type_map.get(ext, "ファイル")


def build_error_message(message):
    """
    エラーメッセージと管理者問い合わせテンプレートの連結

    Args:
        message: 画面上に表示するエラーメッセージ

    Returns:
        エラーメッセージと管理者問い合わせテンプレートの連結テキスト
    """
    return "\n".join([f"❌ {message}", ct.COMMON_ERROR_MESSAGE])


def get_llm_response(chat_message):
    """
    LLMからの回答取得（強化版）
    
    機能：
    - 入力検証
    - レート制限
    - キャッシング
    - エラーハンドリング
    - 詳細なログ記録

    Args:
        chat_message: ユーザー入力値

    Returns:
        LLMからの回答
    """
    start_time = time.time()
    
    # インスタンスを取得
    rate_limiter = get_rate_limiter()
    # query_cache = get_query_cache()  # キャッシュ機能を無効化
    logger = get_langchain_logger()
    conversation_manager = get_conversation_manager()
    
    try:
        # 1. 入力検証
        is_valid, error_message = InputValidator.validate(chat_message)
        if not is_valid:
            st.error(error_message)
            return None
        
        # 2. レート制限チェック
        session_id = st.session_state.get("session_id", "default")
        is_allowed, remaining = rate_limiter.is_allowed(session_id)
        
        if not is_allowed:
            st.error("🚫 リクエスト制限に達しました。1分後に再度お試しください。")
            logger.log_query(
                query=chat_message,
                answer="",
                sources=[],
                elapsed_time=time.time() - start_time,
                success=False,
                error="Rate limit exceeded"
            )
            return None
        
        # 残りリクエスト数を表示（残り3回以下の場合）
        if remaining <= 3:
            st.info(f"ℹ️ 残りリクエスト数: {remaining}回（1分ごとにリセット）")
        
        # 3. キャッシュチェック（無効化）
        # cached_answer = query_cache.get(chat_message, max_age=3600)
        # if cached_answer:
        #     st.info("💡 キャッシュから回答を取得しました")
        #     
        #     # キャッシュからの回答をログに記録
        #     logger.log_query(
        #         query=chat_message,
        #         answer=cached_answer,
        #         sources=["cache"],
        #         elapsed_time=time.time() - start_time,
        #         success=True
        #     )
        #     
        #     # 回答を返す（簡易版）
        #     return {
        #         "answer": cached_answer,
        #         "context": [],
        #         "from_cache": True
        #     }
        
        # 4. LLMのオブジェクトを用意（OpenAI優先、フォールバックはGoogle Gemini）
        # APIキーの取得（環境変数またはStreamlit Secrets）
        openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
        google_api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
        
        # OpenAI APIキーが利用可能な場合はOpenAIを優先使用（gpt-4o-miniは128kコンテキスト対応）
        if openai_api_key:
            llm = ChatOpenAI(
                model=ct.MODEL_OPENAI,  # gpt-4o-mini (128k context)
                temperature=ct.TEMPERATURE,
                max_retries=2,
                openai_api_key=openai_api_key
            )
            st.session_state.setdefault("llm_type", "OpenAI (gpt-4o-mini)")
        elif google_api_key:
            llm = ChatGoogleGenerativeAI(
                model=ct.MODEL,
                temperature=ct.TEMPERATURE,
                max_retries=2,
                google_api_key=google_api_key
            )
            st.session_state.setdefault("llm_type", "Google Gemini")
        else:
            raise ValueError(
                "OPENAI_API_KEY または GOOGLE_API_KEY が設定されていません。\n"
                "Streamlit Cloud Secretsで設定してください。"
            )

        # 5. 会話履歴なしでもLLMに理解してもらえる、独立した入力テキストを取得するためのプロンプトテンプレートを作成
        question_generator_template = ct.SYSTEM_PROMPT_CREATE_INDEPENDENT_TEXT
        question_generator_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", question_generator_template),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ]
        )

        # 6. モードによってLLMから回答を取得する用のプロンプトを変更
        if st.session_state.mode == ct.ANSWER_MODE_1:
            # モードが「社内文書検索」の場合のプロンプト
            question_answer_template = ct.SYSTEM_PROMPT_DOC_SEARCH
        else:
            # モードが「社内問い合わせ」の場合のプロンプト
            question_answer_template = ct.SYSTEM_PROMPT_INQUIRY
        
        # LLMから回答を取得する用のプロンプトテンプレートを作成
        question_answer_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", question_answer_template),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ]
        )

        # 7. 会話履歴をトリミング（メモリ管理）
        trimmed_chat_history = conversation_manager.trim_history(st.session_state.chat_history)
        
        # 8. 会話履歴なしでもLLMに理解してもらえる、独立した入力テキストを取得するためのRetrieverを作成
        history_aware_retriever = create_history_aware_retriever(
            llm, st.session_state.retriever, question_generator_prompt
        )

        # 9. LLMから回答を取得する用のChainを作成
        question_answer_chain = create_stuff_documents_chain(llm, question_answer_prompt)
        
        # 10. 「RAG x 会話履歴の記憶機能」を実現するためのChainを作成
        chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        # 11. LLMへのリクエストとレスポンス取得
        llm_response = chain.invoke({
            "input": chat_message,
            "chat_history": trimmed_chat_history
        })
        
        # 12. LLMレスポンスを会話履歴に追加
        st.session_state.chat_history.extend([
            HumanMessage(content=chat_message),
            llm_response["answer"]
        ])
        
        # 13. キャッシュに保存（無効化）
        # query_cache.set(chat_message, llm_response["answer"])
        
        # 14. 参照元を取得
        sources = [doc.metadata.get("source", "unknown") for doc in llm_response.get("context", [])]
        
        # 15. ログに記録
        elapsed_time = time.time() - start_time
        logger.log_query(
            query=chat_message,
            answer=llm_response["answer"],
            sources=sources,
            elapsed_time=elapsed_time,
            success=True
        )
        
        # 処理時間を表示（3秒以上の場合）
        if elapsed_time > 3:
            st.caption(f"⏱️ 処理時間: {elapsed_time:.1f}秒")

        return llm_response
    
    except Exception as e:
        # エラーハンドリング
        error_message = ErrorHandler.handle_llm_error(e)
        st.error(f"❌ {error_message}")
        
        # ログに記録
        logger.log_query(
            query=chat_message,
            answer="",
            sources=[],
            elapsed_time=time.time() - start_time,
            success=False,
            error=str(e)
        )
        
        return None