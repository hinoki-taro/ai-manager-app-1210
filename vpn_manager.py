"""
VPN・プロキシ管理モジュール
セキュアなネットワーク接続を提供します。

使用方法:
    import vpn_manager
    vpn_manager.setup_proxy("socks5://localhost:1080")
    vpn_manager.secure_request("https://example.com")
"""

import os
import requests
from typing import Optional, Dict
import streamlit as st

# プロキシサポート
try:
    import socks
    import socket
    SOCKS_AVAILABLE = True
except ImportError:
    SOCKS_AVAILABLE = False

# SSHトンネル
try:
    from sshtunnel import SSHTunnelForwarder
    SSH_TUNNEL_AVAILABLE = True
except ImportError:
    SSH_TUNNEL_AVAILABLE = False

# User-Agent偽装
try:
    from fake_useragent import UserAgent
    UA_AVAILABLE = True
except ImportError:
    UA_AVAILABLE = False


class ProxyManager:
    """プロキシ管理クラス"""
    
    def __init__(self):
        self.proxy_config = None
        self.session = requests.Session()
    
    def set_proxy(self, proxy_url: str, proxy_type: str = "http"):
        """
        プロキシを設定
        
        Args:
            proxy_url: プロキシのURL（例: "localhost:8080"）
            proxy_type: プロキシタイプ（"http", "https", "socks5"）
        """
        try:
            if proxy_type in ["http", "https"]:
                self.proxy_config = {
                    "http": f"http://{proxy_url}",
                    "https": f"https://{proxy_url}"
                }
            elif proxy_type == "socks5":
                if not SOCKS_AVAILABLE:
                    st.error("SOCKS5プロキシにはPySocksが必要です: pip install PySocks")
                    return False
                
                self.proxy_config = {
                    "http": f"socks5://{proxy_url}",
                    "https": f"socks5://{proxy_url}"
                }
            
            self.session.proxies.update(self.proxy_config)
            return True
        
        except Exception as e:
            st.error(f"プロキシの設定に失敗: {str(e)}")
            return False
    
    def clear_proxy(self):
        """プロキシ設定をクリア"""
        self.proxy_config = None
        self.session.proxies.clear()
    
    def get_request(self, url: str, **kwargs) -> Optional[requests.Response]:
        """
        プロキシ経由でGETリクエスト
        
        Args:
            url: リクエスト先URL
            **kwargs: requestsの追加パラメータ
        
        Returns:
            レスポンスオブジェクト
        """
        try:
            response = self.session.get(url, **kwargs)
            return response
        
        except Exception as e:
            st.error(f"リクエストに失敗: {str(e)}")
            return None
    
    def test_connection(self, test_url: str = "https://www.google.com") -> bool:
        """
        プロキシ接続をテスト
        
        Args:
            test_url: テスト用URL
        
        Returns:
            接続成功かどうか
        """
        try:
            response = self.session.get(test_url, timeout=10)
            return response.status_code == 200
        
        except Exception:
            return False


class SSHTunnelManager:
    """SSHトンネル管理クラス"""
    
    def __init__(self):
        self.tunnel = None
    
    def create_tunnel(
        self,
        ssh_host: str,
        ssh_port: int,
        ssh_user: str,
        ssh_password: str = None,
        ssh_key_file: str = None,
        remote_bind_address: tuple = ('127.0.0.1', 80),
        local_bind_address: tuple = ('127.0.0.1', 8080)
    ) -> bool:
        """
        SSHトンネルを作成
        
        Args:
            ssh_host: SSHサーバーのホスト
            ssh_port: SSHポート
            ssh_user: SSHユーザー名
            ssh_password: SSHパスワード
            ssh_key_file: SSH秘密鍵ファイル
            remote_bind_address: リモートバインドアドレス
            local_bind_address: ローカルバインドアドレス
        
        Returns:
            成功したかどうか
        """
        if not SSH_TUNNEL_AVAILABLE:
            st.error("SSHトンネルにはsshtunnelが必要です: pip install sshtunnel")
            return False
        
        try:
            self.tunnel = SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                ssh_pkey=ssh_key_file,
                remote_bind_address=remote_bind_address,
                local_bind_address=local_bind_address
            )
            
            self.tunnel.start()
            return True
        
        except Exception as e:
            st.error(f"SSHトンネルの作成に失敗: {str(e)}")
            return False
    
    def close_tunnel(self):
        """SSHトンネルを閉じる"""
        if self.tunnel:
            try:
                self.tunnel.stop()
                self.tunnel = None
            except Exception as e:
                st.error(f"SSHトンネルのクローズに失敗: {str(e)}")
    
    def is_active(self) -> bool:
        """トンネルがアクティブか確認"""
        return self.tunnel is not None and self.tunnel.is_active


class SecureBrowser:
    """セキュアブラウジングクラス"""
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_secure_headers()
    
    def setup_secure_headers(self):
        """セキュアなヘッダーを設定"""
        if UA_AVAILABLE:
            ua = UserAgent()
            user_agent = ua.random
        else:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def secure_get(self, url: str, verify_ssl: bool = True, **kwargs) -> Optional[requests.Response]:
        """
        セキュアなGETリクエスト
        
        Args:
            url: リクエスト先URL
            verify_ssl: SSL証明書を検証するか
            **kwargs: requestsの追加パラメータ
        
        Returns:
            レスポンスオブジェクト
        """
        try:
            response = self.session.get(url, verify=verify_ssl, **kwargs)
            return response
        
        except requests.exceptions.SSLError:
            st.warning("SSL証明書の検証に失敗しました。")
            return None
        
        except Exception as e:
            st.error(f"リクエストに失敗: {str(e)}")
            return None
    
    def get_with_retry(self, url: str, max_retries: int = 3, **kwargs) -> Optional[requests.Response]:
        """
        リトライ機能付きGETリクエスト
        
        Args:
            url: リクエスト先URL
            max_retries: 最大リトライ回数
            **kwargs: requestsの追加パラメータ
        
        Returns:
            レスポンスオブジェクト
        """
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, **kwargs)
                if response.status_code == 200:
                    return response
            
            except Exception as e:
                if attempt == max_retries - 1:
                    st.error(f"最大リトライ回数に到達: {str(e)}")
                    return None
        
        return None


class VPNStatus:
    """VPN状態管理クラス"""
    
    @staticmethod
    def check_ip() -> Dict[str, str]:
        """現在のIPアドレスを確認"""
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            data = response.json()
            
            return {
                'ip': data.get('ip', 'Unknown'),
                'status': 'connected'
            }
        
        except Exception as e:
            return {
                'ip': 'Unknown',
                'status': 'error',
                'error': str(e)
            }
    
    @staticmethod
    def check_location() -> Dict[str, str]:
        """IPアドレスから位置情報を取得"""
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            data = response.json()
            
            return {
                'ip': data.get('ip', 'Unknown'),
                'country': data.get('country_name', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'region': data.get('region', 'Unknown')
            }
        
        except Exception as e:
            return {
                'error': str(e)
            }


def demo_vpn_manager():
    """VPNマネージャーのデモ"""
    st.title("🔐 VPN・プロキシマネージャー")
    
    tab1, tab2, tab3 = st.tabs(["プロキシ設定", "SSHトンネル", "接続状態"])
    
    with tab1:
        st.header("プロキシ設定")
        
        proxy_type = st.selectbox("プロキシタイプ", ["http", "https", "socks5"])
        proxy_url = st.text_input("プロキシURL", "localhost:8080")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("プロキシを設定"):
                proxy_manager = ProxyManager()
                if proxy_manager.set_proxy(proxy_url, proxy_type):
                    st.success("プロキシを設定しました")
        
        with col2:
            if st.button("接続テスト"):
                proxy_manager = ProxyManager()
                proxy_manager.set_proxy(proxy_url, proxy_type)
                
                with st.spinner("接続テスト中..."):
                    if proxy_manager.test_connection():
                        st.success("✓ 接続成功")
                    else:
                        st.error("✗ 接続失敗")
    
    with tab2:
        st.header("SSHトンネル")
        
        if not SSH_TUNNEL_AVAILABLE:
            st.warning("SSHトンネル機能を使用するには sshtunnel をインストールしてください")
            st.code("pip install sshtunnel")
        else:
            ssh_host = st.text_input("SSHホスト")
            ssh_port = st.number_input("SSHポート", value=22)
            ssh_user = st.text_input("SSHユーザー名")
            ssh_password = st.text_input("SSHパスワード", type="password")
            
            if st.button("トンネル作成"):
                tunnel_manager = SSHTunnelManager()
                if tunnel_manager.create_tunnel(
                    ssh_host=ssh_host,
                    ssh_port=ssh_port,
                    ssh_user=ssh_user,
                    ssh_password=ssh_password
                ):
                    st.success("SSHトンネルを作成しました")
                    st.session_state['ssh_tunnel'] = tunnel_manager
    
    with tab3:
        st.header("接続状態")
        
        if st.button("現在のIPを確認"):
            with st.spinner("確認中..."):
                ip_info = VPNStatus.check_ip()
                
                if ip_info['status'] == 'connected':
                    st.success(f"**現在のIPアドレス:** {ip_info['ip']}")
                else:
                    st.error("IPアドレスの取得に失敗しました")
        
        if st.button("位置情報を確認"):
            with st.spinner("確認中..."):
                location_info = VPNStatus.check_location()
                
                if 'error' not in location_info:
                    st.success("位置情報を取得しました")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**IP:** {location_info.get('ip', 'N/A')}")
                        st.write(f"**国:** {location_info.get('country', 'N/A')}")
                    
                    with col2:
                        st.write(f"**都市:** {location_info.get('city', 'N/A')}")
                        st.write(f"**地域:** {location_info.get('region', 'N/A')}")
                else:
                    st.error("位置情報の取得に失敗しました")


if __name__ == "__main__":
    demo_vpn_manager()

