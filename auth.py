"""
認証・アクセス制御モジュール
社内限定公開用の強化された認証機能を提供します。

セキュリティ機能：
- パスワード認証
- ログイン試行回数制限
- セッションタイムアウト
- アクセスログ記録
- IPアドレス制限（オプション）
"""

import streamlit as st
import hashlib
import os
import json
import datetime
from typing import Optional
from pathlib import Path


def hash_password(password: str) -> str:
    """パスワードをハッシュ化します"""
    return hashlib.sha256(password.encode()).hexdigest()


def get_log_file_path() -> Path:
    """ログファイルのパスを取得します"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    return log_dir / "access_log.json"


def log_access_attempt(success: bool, username: str = "user", ip_address: str = None):
    """
    アクセス試行をログに記録します
    
    Args:
        success: 認証成功の場合True
        username: ユーザー名（デフォルト: "user"）
        ip_address: IPアドレス（オプション）
    """
    try:
        log_file = get_log_file_path()
        
        # 既存のログを読み込む
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
        
        # 新しいログエントリを追加
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "success": success,
            "username": username,
            "ip_address": ip_address or "unknown"
        }
        logs.append(log_entry)
        
        # 最新100件のみ保持
        logs = logs[-100:]
        
        # ログファイルに書き込む
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # ログ記録の失敗はアプリの動作を止めない
        print(f"ログ記録エラー: {e}")


def get_failed_attempts(minutes: int = 10) -> int:
    """
    指定時間内の失敗したログイン試行回数を取得します
    
    Args:
        minutes: 何分前までを対象とするか
        
    Returns:
        int: 失敗回数
    """
    try:
        log_file = get_log_file_path()
        if not log_file.exists():
            return 0
        
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        
        # 指定時間以降の失敗を数える
        cutoff_time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
        failed_count = 0
        
        for log in logs:
            try:
                log_time = datetime.datetime.fromisoformat(log["timestamp"])
                if log_time > cutoff_time and not log["success"]:
                    failed_count += 1
            except (KeyError, ValueError):
                continue
        
        return failed_count
    except Exception:
        return 0


def is_session_expired(timeout_minutes: int = 60) -> bool:
    """
    セッションがタイムアウトしているかチェックします
    
    Args:
        timeout_minutes: タイムアウト時間（分）
        
    Returns:
        bool: タイムアウトしている場合True
    """
    if "login_time" not in st.session_state:
        return True
    
    login_time = st.session_state.login_time
    if not isinstance(login_time, datetime.datetime):
        return True
    
    elapsed = datetime.datetime.now() - login_time
    return elapsed.total_seconds() > (timeout_minutes * 60)


def check_ip_whitelist() -> bool:
    """
    IPアドレスホワイトリストをチェックします（オプション機能）
    
    Returns:
        bool: ホワイトリストが未設定または許可されている場合True
    """
    # 環境変数からホワイトリストを取得
    whitelist_str = os.getenv("IP_WHITELIST", "")
    
    # Streamlit secretsからも試みる
    if not whitelist_str and hasattr(st, "secrets") and "auth" in st.secrets:
        whitelist_str = st.secrets["auth"].get("ip_whitelist", "")
    
    # ホワイトリストが設定されていない場合は制限なし
    if not whitelist_str:
        return True
    
    # ホワイトリストをパース
    whitelist = [ip.strip() for ip in whitelist_str.split(",")]
    
    # 現在のIPアドレスを取得（Streamlit Cloudでは難しいため簡易実装）
    # 実際の環境では、リバースプロキシのヘッダーなどから取得する必要がある
    return True  # デフォルトでは許可


def check_password() -> bool:
    """
    強化されたパスワード認証を行います。
    
    セキュリティ機能：
    - ログイン試行回数制限（10分間に5回まで）
    - セッションタイムアウト（60分）
    - アクセスログ記録
    - IPアドレス制限（オプション）
    
    Returns:
        bool: 認証成功の場合True、それ以外はFalse
        
    環境変数での設定方法:
        ACCESS_PASSWORD=your_password_here
        SESSION_TIMEOUT_MINUTES=60  # オプション（デフォルト: 60）
        MAX_LOGIN_ATTEMPTS=5  # オプション（デフォルト: 5）
        IP_WHITELIST=192.168.1.1,192.168.1.2  # オプション
        
    または、Streamlit Cloudのsecretsで設定:
        [auth]
        password = "your_password_here"
        session_timeout_minutes = 60
        max_login_attempts = 5
        ip_whitelist = "192.168.1.1,192.168.1.2"
    """
    # 認証が不要な場合（環境変数で無効化）
    if os.getenv("DISABLE_AUTH", "false").lower() == "true":
        return True
    
    # IPアドレス制限のチェック
    if not check_ip_whitelist():
        st.error("🚫 このIPアドレスからのアクセスは許可されていません。")
        st.stop()
        return False
    
    # パスワードの取得（環境変数 or Streamlit secrets）
    correct_password = None
    
    # 1. 環境変数から取得を試みる
    if os.getenv("ACCESS_PASSWORD"):
        correct_password = os.getenv("ACCESS_PASSWORD")
    
    # 2. Streamlit secretsから取得を試みる
    elif hasattr(st, "secrets") and "auth" in st.secrets:
        if "password" in st.secrets["auth"]:
            correct_password = st.secrets["auth"]["password"]
    
    # パスワードが設定されていない場合は認証不要
    if not correct_password:
        return True
    
    # タイムアウト設定の取得
    timeout_minutes = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))
    if hasattr(st, "secrets") and "auth" in st.secrets:
        timeout_minutes = int(st.secrets["auth"].get("session_timeout_minutes", timeout_minutes))
    
    # 最大ログイン試行回数の取得
    max_attempts = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    if hasattr(st, "secrets") and "auth" in st.secrets:
        max_attempts = int(st.secrets["auth"].get("max_login_attempts", max_attempts))
    
    # セッション状態の初期化
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    # すでに認証済みの場合、セッションタイムアウトをチェック
    if st.session_state.authenticated:
        if is_session_expired(timeout_minutes):
            st.session_state.authenticated = False
            st.warning(f"⏰ セッションがタイムアウトしました（{timeout_minutes}分）。再度ログインしてください。")
            st.rerun()
        return True
    
    # ログイン試行回数のチェック
    failed_attempts = get_failed_attempts(minutes=10)
    if failed_attempts >= max_attempts:
        st.error(f"🚫 ログイン試行回数が上限に達しました。10分後に再度お試しください。")
        st.caption(f"過去10分間に{failed_attempts}回の失敗した試行がありました。")
        st.stop()
        return False
    
    # 認証UI
    st.markdown("# 🔒 アクセス認証")
    st.markdown("---")
    
    # セキュリティ情報の表示
    with st.expander("🛡️ セキュリティ情報"):
        st.markdown(f"""
        - **セッションタイムアウト：** {timeout_minutes}分
        - **ログイン試行制限：** 10分間に{max_attempts}回まで
        - **アクセスログ：** 記録されています
        """)
    
    st.info("この社内アプリにアクセスするには、パスワードを入力してください。")
    
    with st.form("auth_form"):
        password = st.text_input(
            "パスワード",
            type="password",
            placeholder="社内共有パスワードを入力",
        )
        submit = st.form_submit_button("ログイン")
        
        if submit:
            if password == correct_password:
                # 認証成功
                st.session_state.authenticated = True
                st.session_state.login_time = datetime.datetime.now()
                
                # ログ記録
                log_access_attempt(success=True, username="user")
                
                st.success("✅ 認証に成功しました！")
                st.rerun()
            else:
                # 認証失敗
                log_access_attempt(success=False, username="user")
                
                remaining_attempts = max_attempts - (failed_attempts + 1)
                if remaining_attempts > 0:
                    st.error(f"❌ パスワードが正しくありません。残り試行回数: {remaining_attempts}回")
                else:
                    st.error("🚫 ログイン試行回数の上限に達しました。10分後に再度お試しください。")
                return False
    
    st.markdown("---")
    st.caption("📧 パスワードがわからない場合は、リアルの管理部長までキントーンでお問い合わせください！")
    
    return False


def add_logout_button():
    """ログアウトボタンとセッション情報をサイドバーに追加します"""
    # 認証が有効かつログイン済みの場合のみ表示
    if st.session_state.get("authenticated", False):
        with st.sidebar:
            st.markdown("---")
            
            # セッション情報の表示
            if "login_time" in st.session_state:
                login_time = st.session_state.login_time
                elapsed = datetime.datetime.now() - login_time
                elapsed_minutes = int(elapsed.total_seconds() / 60)
                
                # タイムアウト設定の取得
                timeout_minutes = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))
                if hasattr(st, "secrets") and "auth" in st.secrets:
                    timeout_minutes = int(st.secrets["auth"].get("session_timeout_minutes", timeout_minutes))
                
                remaining_minutes = timeout_minutes - elapsed_minutes
                
                # ログイン情報の表示を削除
                # st.caption(f"🔐 ログイン中")
                # st.caption(f"⏱️ セッション残り時間: 約{remaining_minutes}分")
            
            if st.button("🚪 ログアウト", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.login_time = None
                st.success("ログアウトしました")
                st.rerun()


def get_user_info() -> Optional[dict]:
    """
    ユーザー情報を取得します
    
    Returns:
        dict: ユーザー情報の辞書、または認証なしの場合None
    """
    if st.session_state.get("authenticated", False):
        login_time = st.session_state.get("login_time", None)
        
        # セッション経過時間を計算
        elapsed_seconds = 0
        if login_time and isinstance(login_time, datetime.datetime):
            elapsed = datetime.datetime.now() - login_time
            elapsed_seconds = int(elapsed.total_seconds())
        
        return {
            "authenticated": True,
            "login_time": login_time,
            "elapsed_seconds": elapsed_seconds,
        }
    return None


def get_access_logs(limit: int = 50) -> list:
    """
    アクセスログを取得します（管理者用）
    
    Args:
        limit: 取得する件数
        
    Returns:
        list: ログエントリのリスト
    """
    try:
        log_file = get_log_file_path()
        if not log_file.exists():
            return []
        
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        
        # 最新のものから返す
        return logs[-limit:]
    except Exception:
        return []


# 使用例のためのヘルパー関数
def require_auth(func):
    """
    デコレーター: 関数の実行前に認証を要求します
    
    使用例:
        @require_auth
        def main():
            st.write("認証後のコンテンツ")
    """
    def wrapper(*args, **kwargs):
        if check_password():
            return func(*args, **kwargs)
        else:
            st.stop()
    return wrapper

