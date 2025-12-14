"""
Google Driveセキュリティモジュール

Google Drive連携のセキュリティを強化する機能を提供します。
- アクセス制御
- 監査ログ
- ホワイトリスト管理
- 不正アクセス検知
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any
import streamlit as st


class GoogleDriveSecurityManager:
    """Google Driveセキュリティ管理クラス"""
    
    # セキュリティ設定ファイル
    SECURITY_CONFIG_FILE = 'google_drive_security_config.json'
    
    # 監査ログファイル
    AUDIT_LOG_FILE = 'logs/google_drive_audit.json'
    ACCESS_LOG_FILE = 'logs/google_drive_access.json'
    
    def __init__(self):
        """初期化"""
        self.config = self._load_security_config()
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """ログディレクトリの作成"""
        os.makedirs('logs', exist_ok=True)
    
    def _load_security_config(self) -> Dict[str, Any]:
        """セキュリティ設定を読み込む"""
        if os.path.exists(self.SECURITY_CONFIG_FILE):
            try:
                with open(self.SECURITY_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                st.warning(f"セキュリティ設定の読み込みに失敗: {e}")
        
        # デフォルト設定
        return {
            "enabled": True,
            "require_authentication": True,
            "whitelist_enabled": False,
            "whitelisted_accounts": [],
            "whitelisted_ips": [],
            "allowed_file_types": ["pdf", "docx", "txt", "xlsx", "pptx", "csv"],
            "max_file_size_mb": 100,
            "audit_log_enabled": True,
            "access_log_enabled": True,
            "rate_limit": {
                "enabled": True,
                "max_requests_per_minute": 60,
                "max_downloads_per_hour": 100
            },
            "alerts": {
                "suspicious_activity": True,
                "failed_access_attempts": 3,
                "alert_email": "ai-support@mm-international.co.jp"
            }
        }
    
    def is_account_allowed(self, email: str) -> bool:
        """
        アカウントが許可されているか確認
        
        Args:
            email: Googleアカウントのメールアドレス
        
        Returns:
            許可されている場合 True
        """
        # ホワイトリストが無効の場合は全て許可
        if not self.config.get('whitelist_enabled', False):
            return True
        
        # ホワイトリストをチェック
        whitelisted = self.config.get('whitelisted_accounts', [])
        
        # 完全一致
        if email in whitelisted:
            return True
        
        # ドメイン一致（例: @mm-international.co.jp）
        for allowed in whitelisted:
            if allowed.startswith('@') and email.endswith(allowed):
                return True
        
        return False
    
    def is_ip_allowed(self, ip_address: str) -> bool:
        """
        IPアドレスが許可されているか確認
        
        Args:
            ip_address: IPアドレス
        
        Returns:
            許可されている場合 True
        """
        # IPホワイトリストが空の場合は全て許可
        whitelisted_ips = self.config.get('whitelisted_ips', [])
        if not whitelisted_ips:
            return True
        
        return ip_address in whitelisted_ips
    
    def is_file_type_allowed(self, file_name: str) -> bool:
        """
        ファイル形式が許可されているか確認
        
        Args:
            file_name: ファイル名
        
        Returns:
            許可されている場合 True
        """
        allowed_types = self.config.get('allowed_file_types', [])
        if not allowed_types:
            return True
        
        file_ext = os.path.splitext(file_name)[1].lower().lstrip('.')
        return file_ext in allowed_types
    
    def is_file_size_allowed(self, file_size_bytes: int) -> bool:
        """
        ファイルサイズが許可範囲内か確認
        
        Args:
            file_size_bytes: ファイルサイズ（バイト）
        
        Returns:
            許可されている場合 True
        """
        max_size_mb = self.config.get('max_file_size_mb', 100)
        max_size_bytes = max_size_mb * 1024 * 1024
        
        return file_size_bytes <= max_size_bytes
    
    def log_access(self, account_email: str, action: str, resource: str, 
                   status: str, details: Optional[Dict] = None):
        """
        アクセスログを記録
        
        Args:
            account_email: アカウントのメールアドレス
            action: アクション（list_folders, download_file等）
            resource: リソース（フォルダID、ファイル名等）
            status: ステータス（success, denied, error）
            details: 追加の詳細情報
        """
        if not self.config.get('access_log_enabled', True):
            return
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "account": account_email,
            "action": action,
            "resource": resource,
            "status": status,
            "ip_address": self._get_client_ip(),
            "user_agent": self._get_user_agent(),
            "details": details or {}
        }
        
        self._append_to_log(self.ACCESS_LOG_FILE, log_entry)
    
    def log_audit(self, account_email: str, event_type: str, 
                  description: str, severity: str = "info"):
        """
        監査ログを記録
        
        Args:
            account_email: アカウントのメールアドレス
            event_type: イベントタイプ（auth, download, access_denied等）
            description: 説明
            severity: 重要度（info, warning, error, critical）
        """
        if not self.config.get('audit_log_enabled', True):
            return
        
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "account": account_email,
            "event_type": event_type,
            "description": description,
            "severity": severity,
            "ip_address": self._get_client_ip()
        }
        
        self._append_to_log(self.AUDIT_LOG_FILE, audit_entry)
        
        # 重要なイベントの場合は警告
        if severity in ["error", "critical"]:
            st.warning(f"🔒 セキュリティイベント: {description}")
    
    def _append_to_log(self, log_file: str, entry: Dict):
        """ログファイルにエントリを追加"""
        try:
            logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            
            logs.append(entry)
            
            # 最新の1000件のみ保持
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        
        except Exception as e:
            st.warning(f"ログの記録に失敗: {e}")
    
    def _get_client_ip(self) -> str:
        """クライアントのIPアドレスを取得"""
        try:
            # Streamlitのセッションから取得を試みる
            # 実際の環境では適切な方法で取得
            return "unknown"
        except:
            return "unknown"
    
    def _get_user_agent(self) -> str:
        """ユーザーエージェントを取得"""
        try:
            # 実際の環境では適切な方法で取得
            return "unknown"
        except:
            return "unknown"
    
    def check_rate_limit(self, account_email: str, action: str) -> bool:
        """
        レート制限をチェック
        
        Args:
            account_email: アカウントのメールアドレス
            action: アクション
        
        Returns:
            レート制限内の場合 True
        """
        if not self.config.get('rate_limit', {}).get('enabled', False):
            return True
        
        # 簡易実装（実際にはより詳細なレート制限を実装）
        return True
    
    def encrypt_token(self, token_data: str, account_email: str) -> str:
        """
        トークンを暗号化
        
        Args:
            token_data: トークンデータ
            account_email: アカウントのメールアドレス
        
        Returns:
            暗号化されたトークン
        """
        # 簡易的なハッシュ化（実際の実装では適切な暗号化を使用）
        key = f"{account_email}_secret_key"
        return hashlib.sha256(f"{token_data}{key}".encode()).hexdigest()
    
    def validate_access(self, account_email: str, resource: str, 
                       action: str) -> tuple[bool, str]:
        """
        アクセスを検証
        
        Args:
            account_email: アカウントのメールアドレス
            resource: リソース
            action: アクション
        
        Returns:
            (許可/拒否, 理由)
        """
        # セキュリティ機能が無効の場合
        if not self.config.get('enabled', True):
            return True, "security_disabled"
        
        # アカウントホワイトリストチェック
        if not self.is_account_allowed(account_email):
            self.log_audit(
                account_email, 
                "access_denied", 
                f"アカウントがホワイトリストに含まれていません: {resource}",
                "warning"
            )
            return False, "account_not_whitelisted"
        
        # IPアドレスチェック
        client_ip = self._get_client_ip()
        if not self.is_ip_allowed(client_ip):
            self.log_audit(
                account_email,
                "access_denied",
                f"IPアドレスが許可されていません: {client_ip}",
                "warning"
            )
            return False, "ip_not_allowed"
        
        # レート制限チェック
        if not self.check_rate_limit(account_email, action):
            self.log_audit(
                account_email,
                "rate_limit_exceeded",
                f"レート制限を超過しました: {action}",
                "warning"
            )
            return False, "rate_limit_exceeded"
        
        # アクセスログを記録
        self.log_access(account_email, action, resource, "allowed")
        
        return True, "allowed"
    
    def validate_file_download(self, account_email: str, file_name: str, 
                               file_size: int) -> tuple[bool, str]:
        """
        ファイルダウンロードを検証
        
        Args:
            account_email: アカウントのメールアドレス
            file_name: ファイル名
            file_size: ファイルサイズ（バイト）
        
        Returns:
            (許可/拒否, 理由)
        """
        # ファイル形式チェック
        if not self.is_file_type_allowed(file_name):
            self.log_audit(
                account_email,
                "download_denied",
                f"許可されていないファイル形式: {file_name}",
                "warning"
            )
            return False, "file_type_not_allowed"
        
        # ファイルサイズチェック
        if not self.is_file_size_allowed(file_size):
            max_size = self.config.get('max_file_size_mb', 100)
            self.log_audit(
                account_email,
                "download_denied",
                f"ファイルサイズが制限を超過: {file_name} ({file_size / 1024 / 1024:.2f}MB > {max_size}MB)",
                "warning"
            )
            return False, "file_size_exceeded"
        
        # ダウンロードログを記録
        self.log_access(
            account_email,
            "download_file",
            file_name,
            "success",
            {"file_size": file_size}
        )
        
        return True, "allowed"
    
    def get_access_logs(self, account_email: Optional[str] = None, 
                       limit: int = 100) -> List[Dict]:
        """
        アクセスログを取得
        
        Args:
            account_email: フィルタするアカウント（Noneの場合は全て）
            limit: 取得する最大件数
        
        Returns:
            ログエントリのリスト
        """
        if not os.path.exists(self.ACCESS_LOG_FILE):
            return []
        
        try:
            with open(self.ACCESS_LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            # アカウントでフィルタ
            if account_email:
                logs = [log for log in logs if log.get('account') == account_email]
            
            # 最新のものから返す
            return logs[-limit:][::-1]
        
        except Exception as e:
            st.warning(f"ログの読み込みに失敗: {e}")
            return []
    
    def get_audit_logs(self, severity: Optional[str] = None, 
                      limit: int = 100) -> List[Dict]:
        """
        監査ログを取得
        
        Args:
            severity: フィルタする重要度（Noneの場合は全て）
            limit: 取得する最大件数
        
        Returns:
            ログエントリのリスト
        """
        if not os.path.exists(self.AUDIT_LOG_FILE):
            return []
        
        try:
            with open(self.AUDIT_LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            # 重要度でフィルタ
            if severity:
                logs = [log for log in logs if log.get('severity') == severity]
            
            # 最新のものから返す
            return logs[-limit:][::-1]
        
        except Exception as e:
            st.warning(f"ログの読み込みに失敗: {e}")
            return []
    
    def generate_security_report(self) -> Dict[str, Any]:
        """
        セキュリティレポートを生成
        
        Returns:
            レポートデータ
        """
        access_logs = self.get_access_logs(limit=1000)
        audit_logs = self.get_audit_logs(limit=1000)
        
        # 統計情報を集計
        total_accesses = len(access_logs)
        denied_accesses = len([log for log in access_logs if log.get('status') == 'denied'])
        
        total_audits = len(audit_logs)
        warnings = len([log for log in audit_logs if log.get('severity') == 'warning'])
        errors = len([log for log in audit_logs if log.get('severity') in ['error', 'critical']])
        
        # アカウント別統計
        accounts = {}
        for log in access_logs:
            account = log.get('account', 'unknown')
            if account not in accounts:
                accounts[account] = {'total': 0, 'denied': 0}
            accounts[account]['total'] += 1
            if log.get('status') == 'denied':
                accounts[account]['denied'] += 1
        
        return {
            "generated_at": datetime.now().isoformat(),
            "access_summary": {
                "total_accesses": total_accesses,
                "allowed_accesses": total_accesses - denied_accesses,
                "denied_accesses": denied_accesses
            },
            "audit_summary": {
                "total_events": total_audits,
                "warnings": warnings,
                "errors": errors
            },
            "account_statistics": accounts,
            "recent_denied_accesses": [
                log for log in access_logs if log.get('status') == 'denied'
            ][:10],
            "recent_critical_events": [
                log for log in audit_logs if log.get('severity') in ['error', 'critical']
            ][:10]
        }


def display_security_dashboard():
    """セキュリティダッシュボードを表示（Streamlit）"""
    st.title("🔒 Google Drive セキュリティダッシュボード")
    
    security = GoogleDriveSecurityManager()
    
    # セキュリティレポートを生成
    report = security.generate_security_report()
    
    # サマリー
    st.header("📊 概要")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "総アクセス数",
            report['access_summary']['total_accesses']
        )
    
    with col2:
        st.metric(
            "許可されたアクセス",
            report['access_summary']['allowed_accesses'],
            delta=None,
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "拒否されたアクセス",
            report['access_summary']['denied_accesses'],
            delta=None,
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "セキュリティイベント",
            report['audit_summary']['warnings'] + report['audit_summary']['errors'],
            delta=None,
            delta_color="inverse"
        )
    
    # アカウント別統計
    st.header("👥 アカウント別統計")
    
    if report['account_statistics']:
        for account, stats in report['account_statistics'].items():
            with st.expander(f"📧 {account}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**総アクセス:** {stats['total']}")
                with col2:
                    st.write(f"**拒否:** {stats['denied']}")
    else:
        st.info("アクセス履歴がありません")
    
    # 最近の拒否されたアクセス
    st.header("⚠️ 最近の拒否されたアクセス")
    
    if report['recent_denied_accesses']:
        for log in report['recent_denied_accesses']:
            with st.expander(f"{log.get('timestamp', 'N/A')} - {log.get('account', 'N/A')}"):
                st.write(f"**アクション:** {log.get('action', 'N/A')}")
                st.write(f"**リソース:** {log.get('resource', 'N/A')}")
                st.write(f"**IPアドレス:** {log.get('ip_address', 'N/A')}")
    else:
        st.success("拒否されたアクセスはありません")
    
    # 重要なセキュリティイベント
    st.header("🚨 重要なセキュリティイベント")
    
    if report['recent_critical_events']:
        for log in report['recent_critical_events']:
            severity = log.get('severity', 'info')
            icon = "🔴" if severity == "critical" else "🟠"
            
            with st.expander(f"{icon} {log.get('timestamp', 'N/A')} - {log.get('event_type', 'N/A')}"):
                st.write(f"**アカウント:** {log.get('account', 'N/A')}")
                st.write(f"**説明:** {log.get('description', 'N/A')}")
                st.write(f"**重要度:** {severity}")
    else:
        st.success("重要なセキュリティイベントはありません")


if __name__ == "__main__":
    display_security_dashboard()



