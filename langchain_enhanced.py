"""
LangChain強化モジュール
高度なLangChain機能とセキュリティ機能を提供します。

機能：
- ストリーミング対応
- レート制限
- 入力検証
- キャッシング
- エラーハンドリング
- 詳細なログ
"""

import time
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

import streamlit as st
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult


class StreamHandler(BaseCallbackHandler):
    """
    ストリーミング表示用のコールバックハンドラー
    LLMからのレスポンスをリアルタイムで表示します
    """
    
    def __init__(self, container):
        self.container = container
        self.text = ""
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """新しいトークンが生成されたときに呼ばれる"""
        self.text += token
        self.container.markdown(self.text)


class RateLimiter:
    """
    レート制限を実装するクラス
    ユーザーごとのAPIリクエスト回数を制限します
    """
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        """
        Args:
            max_requests: 時間枠内の最大リクエスト数
            time_window: 時間枠（秒）
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}
    
    def is_allowed(self, user_id: str = "default") -> tuple[bool, int]:
        """
        リクエストが許可されるかチェックします
        
        Args:
            user_id: ユーザーID
            
        Returns:
            tuple: (許可されるか, 残りリクエスト数)
        """
        current_time = time.time()
        
        # ユーザーのリクエスト履歴を取得
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # 時間枠外の古いリクエストを削除
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if current_time - req_time < self.time_window
        ]
        
        # リクエスト数をチェック
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(current_time)
            remaining = self.max_requests - len(self.requests[user_id])
            return True, remaining
        
        return False, 0


class QueryCache:
    """
    クエリのキャッシング機能
    同じ質問に対する回答をキャッシュして効率化します
    """
    
    def __init__(self, cache_file: str = "logs/query_cache.json", max_size: int = 100):
        """
        Args:
            cache_file: キャッシュファイルのパス
            max_size: 最大キャッシュサイズ
        """
        self.cache_file = Path(cache_file)
        self.cache_file.parent.mkdir(exist_ok=True)
        self.max_size = max_size
        self.cache = self._load_cache()
    
    def _load_cache(self) -> dict:
        """キャッシュをファイルから読み込む"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_cache(self):
        """キャッシュをファイルに保存"""
        try:
            # 最大サイズを超えたら古いものを削除
            if len(self.cache) > self.max_size:
                # タイムスタンプでソートして古いものを削除
                sorted_items = sorted(
                    self.cache.items(),
                    key=lambda x: x[1].get('timestamp', 0)
                )
                self.cache = dict(sorted_items[-self.max_size:])
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"キャッシュ保存エラー: {e}")
    
    def _get_cache_key(self, query: str) -> str:
        """クエリからキャッシュキーを生成"""
        return hashlib.md5(query.encode()).hexdigest()
    
    def get(self, query: str, max_age: int = 3600) -> Optional[str]:
        """
        キャッシュから回答を取得
        
        Args:
            query: 質問
            max_age: キャッシュの最大有効期間（秒）
            
        Returns:
            キャッシュされた回答、またはNone
        """
        cache_key = self._get_cache_key(query)
        
        if cache_key in self.cache:
            cached_item = self.cache[cache_key]
            timestamp = cached_item.get('timestamp', 0)
            
            # キャッシュが有効期限内かチェック
            if time.time() - timestamp < max_age:
                return cached_item.get('answer')
        
        return None
    
    def set(self, query: str, answer: str):
        """
        回答をキャッシュに保存
        
        Args:
            query: 質問
            answer: 回答
        """
        cache_key = self._get_cache_key(query)
        
        self.cache[cache_key] = {
            'query': query,
            'answer': answer,
            'timestamp': time.time()
        }
        
        self._save_cache()
    
    def clear(self):
        """キャッシュをクリア"""
        self.cache = {}
        self._save_cache()


class InputValidator:
    """
    入力検証クラス
    質問の妥当性をチェックします
    """
    
    @staticmethod
    def validate(query: str, max_length: int = 1000) -> tuple[bool, str]:
        """
        入力を検証
        
        Args:
            query: ユーザーの質問
            max_length: 最大文字数
            
        Returns:
            tuple: (有効かどうか, エラーメッセージ)
        """
        # 空文字チェック
        if not query or not query.strip():
            return False, "質問を入力してください。"
        
        # 長さチェック
        if len(query) > max_length:
            return False, f"質問が長すぎます（最大{max_length}文字）。"
        
        # 最小文字数チェック
        if len(query.strip()) < 2:
            return False, "質問が短すぎます。もう少し詳しく入力してください。"
        
        return True, ""


class LangChainLogger:
    """
    LangChain専用のロガー
    詳細なログを記録します
    """
    
    def __init__(self, log_file: str = "logs/langchain_log.json"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
    
    def log_query(
        self,
        query: str,
        answer: str,
        sources: List[str],
        elapsed_time: float,
        success: bool = True,
        error: str = None
    ):
        """
        クエリをログに記録
        
        Args:
            query: 質問
            answer: 回答
            sources: 参照元のリスト
            elapsed_time: 処理時間（秒）
            success: 成功したか
            error: エラーメッセージ（あれば）
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "answer": answer if success else None,
            "sources": sources,
            "elapsed_time": elapsed_time,
            "success": success,
            "error": error
        }
        
        try:
            # 既存のログを読み込む
            if self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # 新しいログを追加
            logs.append(log_entry)
            
            # 最新100件のみ保持
            logs = logs[-100:]
            
            # ログファイルに書き込む
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"ログ記録エラー: {e}")
    
    def get_logs(self, limit: int = 50) -> list:
        """
        ログを取得
        
        Args:
            limit: 取得する件数
            
        Returns:
            ログエントリのリスト
        """
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                return logs[-limit:]
        except Exception:
            return []
        
        return []


class ConversationManager:
    """
    会話履歴管理クラス
    会話履歴の保存・読み込み・管理を行います
    """
    
    def __init__(self, max_history: int = 10):
        """
        Args:
            max_history: 保持する最大会話数
        """
        self.max_history = max_history
    
    def trim_history(self, chat_history: List[BaseMessage]) -> List[BaseMessage]:
        """
        会話履歴をトリミング
        
        Args:
            chat_history: 会話履歴
            
        Returns:
            トリミングされた会話履歴
        """
        if len(chat_history) > self.max_history * 2:
            # 最新のN件のみ保持（質問と回答のペアなので *2）
            return chat_history[-(self.max_history * 2):]
        return chat_history
    
    def save_conversation(self, session_id: str, chat_history: List[BaseMessage]):
        """
        会話履歴を保存（将来の拡張用）
        
        Args:
            session_id: セッションID
            chat_history: 会話履歴
        """
        # 実装は必要に応じて
        pass


class ErrorHandler:
    """
    エラーハンドリングクラス
    LangChain関連のエラーを適切に処理します
    """
    
    @staticmethod
    def handle_llm_error(error: Exception) -> str:
        """
        LLMエラーを処理
        
        Args:
            error: 発生したエラー
            
        Returns:
            ユーザー向けのエラーメッセージ
        """
        error_str = str(error).lower()
        
        # APIキー関連のエラー
        if "api" in error_str and ("key" in error_str or "auth" in error_str):
            return "APIキーの設定に問題があります。管理者にお問い合わせください。"
        
        # レート制限エラー
        if "rate" in error_str or "quota" in error_str or "429" in error_str:
            return "APIの利用制限に達しました。しばらく待ってから再度お試しください。"
        
        # タイムアウトエラー
        if "timeout" in error_str:
            return "処理がタイムアウトしました。もう少し短い質問をお試しください。"
        
        # ネットワークエラー
        if "network" in error_str or "connection" in error_str:
            return "ネットワークエラーが発生しました。インターネット接続を確認してください。"
        
        # その他のエラー
        return f"エラーが発生しました: {str(error)}\n管理者にお問い合わせください。"


# グローバルインスタンス（シングルトンパターン）
_rate_limiter = None
_query_cache = None
_langchain_logger = None
_conversation_manager = None


def get_rate_limiter() -> RateLimiter:
    """レート制限のインスタンスを取得"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter(max_requests=10, time_window=60)
    return _rate_limiter


def get_query_cache() -> QueryCache:
    """クエリキャッシュのインスタンスを取得"""
    global _query_cache
    if _query_cache is None:
        _query_cache = QueryCache()
    return _query_cache


def get_langchain_logger() -> LangChainLogger:
    """LangChainロガーのインスタンスを取得"""
    global _langchain_logger
    if _langchain_logger is None:
        _langchain_logger = LangChainLogger()
    return _langchain_logger


def get_conversation_manager() -> ConversationManager:
    """会話管理のインスタンスを取得"""
    global _conversation_manager
    if _conversation_manager is None:
        _conversation_manager = ConversationManager(max_history=10)
    return _conversation_manager

