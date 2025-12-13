"""
セキュリティユーティリティモジュール
入力のサニタイゼーション、セキュリティヘッダー設定などを提供します。
"""

import re
import html
from typing import Any


def sanitize_input(text: str) -> str:
    """
    ユーザー入力をサニタイズします
    
    Args:
        text: サニタイズする文字列
        
    Returns:
        str: サニタイズされた文字列
    """
    if not isinstance(text, str):
        return str(text)
    
    # HTMLエスケープ
    text = html.escape(text)
    
    # 制御文字の除去（改行・タブは保持）
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', text)
    
    return text


def validate_input_length(text: str, max_length: int = 10000) -> bool:
    """
    入力文字列の長さを検証します
    
    Args:
        text: 検証する文字列
        max_length: 最大文字数
        
    Returns:
        bool: 長さが適切な場合True
    """
    return len(text) <= max_length


def detect_suspicious_patterns(text: str) -> bool:
    """
    疑わしいパターンを検出します
    
    Args:
        text: 検査する文字列
        
    Returns:
        bool: 疑わしいパターンが見つかった場合True
    """
    # SQLインジェクションのパターン
    sql_patterns = [
        r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)',
        r'(--|;|\/\*|\*\/)',
        r'(\bUNION\b.*\bSELECT\b)',
    ]
    
    # XSSのパターン
    xss_patterns = [
        r'<script[^>]*>',
        r'javascript:',
        r'on\w+\s*=',
    ]
    
    all_patterns = sql_patterns + xss_patterns
    
    for pattern in all_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    return False


def safe_user_input(text: str, max_length: int = 10000) -> tuple[bool, str, str]:
    """
    ユーザー入力を安全に処理します
    
    Args:
        text: ユーザー入力
        max_length: 最大文字数
        
    Returns:
        tuple: (安全性, サニタイズされたテキスト, エラーメッセージ)
    """
    # 長さチェック
    if not validate_input_length(text, max_length):
        return False, "", f"入力が長すぎます（最大{max_length}文字）"
    
    # 疑わしいパターンのチェック
    if detect_suspicious_patterns(text):
        return False, "", "不正な入力が検出されました"
    
    # サニタイズ
    sanitized = sanitize_input(text)
    
    return True, sanitized, ""


def get_security_headers() -> dict:
    """
    セキュリティヘッダーを取得します
    
    Returns:
        dict: セキュリティヘッダーの辞書
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }


def mask_sensitive_data(text: str) -> str:
    """
    センシティブなデータをマスクします
    
    Args:
        text: マスクする文字列
        
    Returns:
        str: マスクされた文字列
    """
    # APIキーのパターン
    text = re.sub(r'(sk-[a-zA-Z0-9]{20,})', 'sk-***MASKED***', text)
    text = re.sub(r'(AIza[a-zA-Z0-9_-]{35})', 'AIza***MASKED***', text)
    
    # パスワードのパターン
    text = re.sub(r'(password["\s:=]+)([^"\s,}]+)', r'\1***MASKED***', text, flags=re.IGNORECASE)
    
    return text


# セキュリティ設定のクラス
class SecurityConfig:
    """セキュリティ設定を管理するクラス"""
    
    def __init__(self):
        self.max_input_length = 10000
        self.session_timeout_minutes = 60
        self.max_login_attempts = 5
        self.enable_ip_whitelist = False
        self.enable_access_log = True
    
    def validate_config(self) -> bool:
        """設定の妥当性を検証します"""
        return (
            self.max_input_length > 0 and
            self.session_timeout_minutes > 0 and
            self.max_login_attempts > 0
        )

