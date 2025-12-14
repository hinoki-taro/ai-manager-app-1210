"""
アバター・ロゴ管理モジュール
会社ロゴと管理部長アバターの表示とアニメーション機能を提供します。
また、UI強化のためのアイコン、背景、イラスト機能も統合しています。

使用方法:
    import avatar_manager
    avatar_manager.show_company_logo()
    avatar_manager.show_manager_avatar(talking=True)
    avatar_manager.show_icon("search", size=48)
    avatar_manager.show_message_success("成功しました！")
"""

import streamlit as st
import base64
from pathlib import Path


class LogoManager:
    """ロゴ管理クラス"""
    
    LOGO_PATH = "assets/images/company_logo.svg"
    LOGO_PLACEHOLDER_SVG = """
    <svg width="200" height="80" xmlns="http://www.w3.org/2000/svg">
        <rect width="200" height="80" fill="#1E3A8A" rx="10"/>
        <text x="100" y="35" font-family="Arial, sans-serif" font-size="24" 
              font-weight="bold" fill="white" text-anchor="middle">MM</text>
        <text x="100" y="55" font-family="Arial, sans-serif" font-size="12" 
              fill="#93C5FD" text-anchor="middle">International</text>
    </svg>
    """
    
    @staticmethod
    def show_logo(width: int = 200, use_column: bool = False):
        """
        会社ロゴを表示
        
        Args:
            width: ロゴの幅（ピクセル）
            use_column: カラムレイアウトを使用するか
        """
        logo_path = Path(LogoManager.LOGO_PATH)
        
        if logo_path.exists():
            # 実際のロゴファイルが存在する場合
            if use_column:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(str(logo_path), width=width)
            else:
                st.image(str(logo_path), width=width)
        else:
            # プレースホルダーSVGを表示
            if use_column:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(
                        f'<div style="text-align: center;">{LogoManager.LOGO_PLACEHOLDER_SVG}</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(LogoManager.LOGO_PLACEHOLDER_SVG, unsafe_allow_html=True)
            
            # ロゴ配置の案内
            with st.expander("ℹ️ ロゴの配置方法"):
                st.info(f"""
                **会社ロゴを表示するには:**
                
                1. 会社のロゴ画像（PNG推奨）を用意
                2. `{LogoManager.LOGO_PATH}` に配置
                3. アプリを再起動
                
                **推奨サイズ:** 幅200-400px、透過PNG
                """)


class AvatarManager:
    """アバター管理クラス"""
    
    AVATAR_PATH = "assets/images/ai_manager_avatar.png"
    
    # かわいい管理部長アバター（40代男性）のSVG
    AVATAR_SVG = """
    <svg width="120" height="120" xmlns="http://www.w3.org/2000/svg">
        <!-- 背景円 -->
        <circle cx="60" cy="60" r="58" fill="#E0F2FE" stroke="#0EA5E9" stroke-width="2"/>
        
        <!-- 顔 -->
        <ellipse cx="60" cy="60" rx="40" ry="45" fill="#FFE4C4"/>
        
        <!-- 髪の毛（短髪、40代らしく少し薄め） -->
        <path d="M 25 40 Q 20 30, 30 25 Q 40 20, 50 22 Q 60 18, 70 22 Q 80 20, 90 25 Q 100 30, 95 40" 
              fill="#4A4A4A" opacity="0.8"/>
        
        <!-- 眉毛 -->
        <path d="M 35 45 Q 40 43, 45 45" stroke="#4A4A4A" stroke-width="2" fill="none"/>
        <path d="M 75 45 Q 80 43, 85 45" stroke="#4A4A4A" stroke-width="2" fill="none"/>
        
        <!-- 目 -->
        <ellipse cx="40" cy="52" rx="4" ry="6" fill="#2C3E50"/>
        <ellipse cx="80" cy="52" rx="4" ry="6" fill="#2C3E50"/>
        
        <!-- 目の輝き -->
        <circle cx="41" cy="50" r="1.5" fill="white"/>
        <circle cx="81" cy="50" r="1.5" fill="white"/>
        
        <!-- 鼻 -->
        <path d="M 60 58 Q 58 63, 60 65" stroke="#D4A574" stroke-width="2" fill="none"/>
        
        <!-- 口（デフォルト状態、笑顔） -->
        <g id="mouth-default">
            <path d="M 45 72 Q 60 78, 75 72" stroke="#D4787B" stroke-width="2.5" fill="none" stroke-linecap="round"/>
        </g>
        
        <!-- ほっぺ -->
        <circle cx="35" cy="65" r="5" fill="#FFB6C1" opacity="0.4"/>
        <circle cx="85" cy="65" r="5" fill="#FFB6C1" opacity="0.4"/>
        
        <!-- メガネ（知的な印象） -->
        <g stroke="#4A4A4A" stroke-width="1.5" fill="none">
            <circle cx="40" cy="52" r="8"/>
            <circle cx="80" cy="52" r="8"/>
            <path d="M 48 52 L 72 52"/>
        </g>
        
        <!-- スーツの襟 -->
        <path d="M 30 100 L 40 110 L 60 105 L 80 110 L 90 100" fill="#1E3A8A"/>
        <rect x="55" y="105" width="10" height="15" fill="#93C5FD"/>
    </svg>
    """
    
    @staticmethod
    def show_avatar(talking: bool = False, size: int = 120):
        """
        管理部長アバターを表示
        
        Args:
            talking: 口を動かすアニメーションを有効にするか
            size: アバターのサイズ（ピクセル）
        """
        avatar_path = Path(AvatarManager.AVATAR_PATH)
        
        if avatar_path.exists():
            # 実際のアバター画像が存在する場合
            if talking:
                # CSSアニメーション付きで表示
                st.markdown(
                    f"""
                    <div class="avatar-container">
                        <img src="data:image/png;base64,{AvatarManager._get_image_base64(avatar_path)}" 
                             class="avatar-talking" style="width: {size}px; height: {size}px;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.image(str(avatar_path), width=size)
        else:
            # SVGアバターを表示
            if talking:
                # 口が動くアニメーション付きSVG
                animated_svg = AvatarManager._create_animated_avatar()
                st.markdown(
                    f'<div style="text-align: center;">{animated_svg}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div style="text-align: center;">{AvatarManager.AVATAR_SVG}</div>',
                    unsafe_allow_html=True
                )
            
            # アバター配置の案内
            with st.expander("ℹ️ アバター画像の配置方法"):
                st.info(f"""
                **カスタムアバターを使用するには:**
                
                1. 管理部長の写真を用意
                2. 画像編集ソフトで可愛くアレンジ（推奨ツール：Canva、Adobe Express）
                3. `{AvatarManager.AVATAR_PATH}` に配置
                4. アプリを再起動
                
                **推奨サイズ:** 120x120px、透過PNG
                
                **または:**
                - AI画像生成ツールで作成（Stable Diffusion, Midjourney等）
                - プロンプト例: "cute cartoon business manager, 40s male, glasses, suit, friendly smile, flat design"
                """)
    
    @staticmethod
    def _create_animated_avatar() -> str:
        """口が動くアニメーション付きアバターSVGを生成"""
        return """
        <svg width="120" height="120" xmlns="http://www.w3.org/2000/svg">
            <style>
                @keyframes mouth-talk {
                    0%, 100% { d: path("M 45 72 Q 60 78, 75 72"); }
                    25% { d: path("M 45 74 Q 60 77, 75 74"); }
                    50% { d: path("M 47 73 Q 60 76, 73 73"); }
                    75% { d: path("M 45 74 Q 60 77, 75 74"); }
                }
                .mouth-animated {
                    animation: mouth-talk 0.8s ease-in-out infinite;
                }
            </style>
            
            <!-- 背景円 -->
            <circle cx="60" cy="60" r="58" fill="#E0F2FE" stroke="#0EA5E9" stroke-width="2"/>
            
            <!-- 顔 -->
            <ellipse cx="60" cy="60" rx="40" ry="45" fill="#FFE4C4"/>
            
            <!-- 髪の毛 -->
            <path d="M 25 40 Q 20 30, 30 25 Q 40 20, 50 22 Q 60 18, 70 22 Q 80 20, 90 25 Q 100 30, 95 40" 
                  fill="#4A4A4A" opacity="0.8"/>
            
            <!-- 眉毛 -->
            <path d="M 35 45 Q 40 43, 45 45" stroke="#4A4A4A" stroke-width="2" fill="none"/>
            <path d="M 75 45 Q 80 43, 85 45" stroke="#4A4A4A" stroke-width="2" fill="none"/>
            
            <!-- 目 -->
            <ellipse cx="40" cy="52" rx="4" ry="6" fill="#2C3E50"/>
            <ellipse cx="80" cy="52" rx="4" ry="6" fill="#2C3E50"/>
            
            <!-- 目の輝き -->
            <circle cx="41" cy="50" r="1.5" fill="white"/>
            <circle cx="81" cy="50" r="1.5" fill="white"/>
            
            <!-- 鼻 -->
            <path d="M 60 58 Q 58 63, 60 65" stroke="#D4A574" stroke-width="2" fill="none"/>
            
            <!-- 口（アニメーション） -->
            <path class="mouth-animated" d="M 45 72 Q 60 78, 75 72" 
                  stroke="#D4787B" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            
            <!-- ほっぺ -->
            <circle cx="35" cy="65" r="5" fill="#FFB6C1" opacity="0.4"/>
            <circle cx="85" cy="65" r="5" fill="#FFB6C1" opacity="0.4"/>
            
            <!-- メガネ -->
            <g stroke="#4A4A4A" stroke-width="1.5" fill="none">
                <circle cx="40" cy="52" r="8"/>
                <circle cx="80" cy="52" r="8"/>
                <path d="M 48 52 L 72 52"/>
            </g>
            
            <!-- スーツの襟 -->
            <path d="M 30 100 L 40 110 L 60 105 L 80 110 L 90 100" fill="#1E3A8A"/>
            <rect x="55" y="105" width="10" height="15" fill="#93C5FD"/>
        </svg>
        """
    
    @staticmethod
    def _get_image_base64(image_path: Path) -> str:
        """画像をBase64エンコード"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()


def apply_avatar_styles():
    """
    アバターアニメーション用のCSSスタイルを適用
    main.pyから呼び出す
    """
    st.markdown(
        """
        <style>
        /* アバターコンテナ */
        .avatar-container {
            text-align: center;
            margin: 10px 0;
        }
        
        /* 話しているアニメーション（強化版） */
        .avatar-talking {
            animation: avatar-bounce 1.2s ease-in-out infinite;
            border-radius: 50%;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        }
        
        .avatar-talking:hover {
            transform: scale(1.05);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
        }
        
        @keyframes avatar-bounce {
            0%, 100% { 
                transform: translateY(0px) scale(1) rotate(0deg); 
            }
            25% { 
                transform: translateY(-4px) scale(1.03) rotate(-1deg); 
            }
            50% { 
                transform: translateY(0px) scale(1) rotate(0deg); 
            }
            75% { 
                transform: translateY(-4px) scale(1.03) rotate(1deg); 
            }
        }
        
        /* ロゴのホバー効果 */
        .logo-hover {
            transition: transform 0.3s ease;
        }
        
        .logo-hover:hover {
            transform: scale(1.05);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def show_welcome_screen():
    """
    ウェルカムスクリーン（ロゴ + アバター）を表示
    """
    # ロゴ表示
    st.markdown('<div class="logo-hover">', unsafe_allow_html=True)
    LogoManager.show_logo(width=250, use_column=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # タイトル
    st.markdown(
        """
        <h1 style='text-align: center; color: #1E3A8A;'>
            社内情報検索AI
        </h1>
        <h3 style='text-align: center; color: #64748B;'>
            AI管理部長がお答えします
        </h3>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # アバター表示（中央配置、大きめサイズ）
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        AvatarManager.show_avatar(talking=True, size=250)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ウェルカムメッセージ
    st.info("""
    社内情報について何でもお尋ねください。
    """)


def show_sidebar_branding():
    """
    サイドバーにロゴとアバターを表示
    """
    with st.sidebar:
        # ロゴ（小さめ）
        LogoManager.show_logo(width=150, use_column=False)
        
        st.markdown("---")
        
        # アバター（中サイズ、中央配置、動くアニメーション）
        col1, col2, col3 = st.columns([0.5, 2, 0.5])
        with col2:
            AvatarManager.show_avatar(talking=True, size=120)
        
        st.markdown(
            """
            <p style='text-align: center; font-size: 12px; color: #64748B;'>
                AI管理部長
            </p>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")


def show_chat_avatar(message_content: str, is_user: bool = False):
    """
    チャット内でアバターを表示
    
    Args:
        message_content: メッセージ内容
        is_user: ユーザーのメッセージか
    """
    if is_user:
        # ユーザーアイコン
        st.markdown(
            """
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="width: 40px; height: 40px; border-radius: 50%; 
                            background: #E0F2FE; display: flex; align-items: center; 
                            justify-content: center; margin-right: 10px;">
                    <span style="font-size: 20px;">👤</span>
                </div>
                <div style="flex: 1; background: #F1F5F9; padding: 10px; 
                            border-radius: 10px;">
                    {message}
                </div>
            </div>
            """.format(message=message_content),
            unsafe_allow_html=True
        )
    else:
        # AI管理部長アイコン
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="margin-right: 10px;">
                    {AvatarManager.AVATAR_SVG.replace('width="120"', 'width="40"').replace('height="120"', 'height="40"')}
                </div>
                <div style="flex: 1; background: #E0F2FE; padding: 10px; 
                            border-radius: 10px;">
                    {message_content}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def demo_avatar_showcase():
    """アバターとロゴのデモ"""
    st.title("🎨 ロゴ＆アバター デモ")
    
    tab1, tab2, tab3 = st.tabs(["ウェルカム画面", "アバターギャラリー", "チャット例"])
    
    with tab1:
        show_welcome_screen()
    
    with tab2:
        st.header("アバターバリエーション")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("通常表示")
            AvatarManager.show_avatar(talking=False, size=120)
        
        with col2:
            st.subheader("話している（アニメーション）")
            AvatarManager.show_avatar(talking=True, size=120)
        
        st.markdown("---")
        
        st.subheader("サイズバリエーション")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("小（80px）")
            AvatarManager.show_avatar(talking=False, size=80)
        
        with col2:
            st.write("中（120px）")
            AvatarManager.show_avatar(talking=False, size=120)
        
        with col3:
            st.write("大（150px）")
            AvatarManager.show_avatar(talking=False, size=150)
    
    with tab3:
        st.header("チャット例")
        
        show_chat_avatar("JINNYの導入台数を教えてください", is_user=True)
        show_chat_avatar("JINNYは1,000台以上導入されています！", is_user=False)
        show_chat_avatar("会社の設立年はいつですか？", is_user=True)
        show_chat_avatar("2004年に設立されました。", is_user=False)


# ============================================================
# UI強化機能（アイコン・背景・イラスト）
# ============================================================

class IconManager:
    """アイコン管理クラス"""
    
    ICONS_DIR = Path("assets/images/icons")
    
    @staticmethod
    def show_icon(icon_type: str, size: int = 48):
        """
        アイコンを表示
        
        Args:
            icon_type: アイコンの種類 (search/document/inquiry/success/warning/error/loading)
            size: アイコンのサイズ（ピクセル）
        """
        icon_files = {
            "search": "search_icon.svg",
            "document": "document_icon.svg",
            "inquiry": "inquiry_icon.svg",
            "success": "success_icon.svg",
            "warning": "warning_icon.svg",
            "error": "error_icon.svg",
            "loading": "loading_icon.svg",
        }
        
        icon_file = icon_files.get(icon_type)
        if icon_file:
            icon_path = IconManager.ICONS_DIR / icon_file
            if icon_path.exists():
                st.image(str(icon_path), width=size)
                return
        
        # フォールバック：絵文字
        emoji_map = {
            "search": "🔍",
            "document": "📄",
            "inquiry": "💬",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "loading": "⏳",
        }
        st.markdown(f"<span style='font-size: {size}px;'>{emoji_map.get(icon_type, '❓')}</span>", 
                   unsafe_allow_html=True)


class MessageBox:
    """メッセージボックス（アイコン付き）"""
    
    @staticmethod
    def success(message: str):
        """成功メッセージ"""
        col1, col2 = st.columns([1, 20])
        with col1:
            IconManager.show_icon("success", size=24)
        with col2:
            st.success(message, icon="✅")
    
    @staticmethod
    def info(message: str):
        """情報メッセージ"""
        col1, col2 = st.columns([1, 20])
        with col1:
            IconManager.show_icon("document", size=24)
        with col2:
            st.info(message, icon="ℹ️")
    
    @staticmethod
    def warning(message: str):
        """警告メッセージ"""
        col1, col2 = st.columns([1, 20])
        with col1:
            IconManager.show_icon("warning", size=24)
        with col2:
            st.warning(message, icon="⚠️")
    
    @staticmethod
    def error(message: str):
        """エラーメッセージ"""
        col1, col2 = st.columns([1, 20])
        with col1:
            IconManager.show_icon("error", size=24)
        with col2:
            st.error(message, icon="❌")


class IllustrationManager:
    """イラスト管理クラス"""
    
    DECORATIONS_DIR = Path("assets/images/decorations")
    
    @staticmethod
    def show_empty_state(message: str = "データがありません", size: int = 200):
        """
        空状態を表示
        
        Args:
            message: メッセージ
            size: イラストのサイズ
        """
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            empty_state_path = IllustrationManager.DECORATIONS_DIR / "empty_state.svg"
            if empty_state_path.exists():
                st.image(str(empty_state_path), width=size)
            
            st.markdown(
                f"""
                <p style="text-align: center; color: #64748B; font-size: 18px; font-weight: 500;">
                    {message}
                </p>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# 便利関数（グローバル）
# ============================================================

def show_icon(icon_type: str, size: int = 48):
    """アイコンを表示（グローバル関数）"""
    IconManager.show_icon(icon_type, size)


def show_message_success(message: str):
    """成功メッセージを表示（グローバル関数）"""
    MessageBox.success(message)


def show_message_info(message: str):
    """情報メッセージを表示（グローバル関数）"""
    MessageBox.info(message)


def show_message_warning(message: str):
    """警告メッセージを表示（グローバル関数）"""
    MessageBox.warning(message)


def show_message_error(message: str):
    """エラーメッセージを表示（グローバル関数）"""
    MessageBox.error(message)


def show_empty_state(message: str = "データがありません"):
    """空状態を表示（グローバル関数）"""
    IllustrationManager.show_empty_state(message)


if __name__ == "__main__":
    apply_avatar_styles()
    demo_avatar_showcase()

