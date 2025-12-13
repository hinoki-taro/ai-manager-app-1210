"""
フィードバック機能モジュール
ユーザーからのフィードバックを収集します。
"""

import streamlit as st
import os
from datetime import datetime
import json


def display_feedback_form():
    """
    フィードバックフォームをサイドバーに表示します。
    """
    with st.sidebar:
        st.markdown("---")
        with st.expander("💬 フィードバック", expanded=False):
            st.markdown("""
ご意見・ご要望をお聞かせください。
アプリの改善に役立てます。
            """)
            
            with st.form("feedback_form", clear_on_submit=True):
                # フィードバックのタイプ
                feedback_type = st.selectbox(
                    "種類",
                    [
                        "💡 機能改善の提案",
                        "🐛 バグ・不具合の報告",
                        "❓ 質問・使い方",
                        "👍 良かった点",
                        "👎 改善してほしい点",
                        "📝 その他"
                    ]
                )
                
                # フィードバック内容
                feedback_content = st.text_area(
                    "内容",
                    placeholder="詳しく教えてください...",
                    height=100
                )
                
                # メールアドレス（オプション）
                email = st.text_input(
                    "メールアドレス（任意）",
                    placeholder="返信が必要な場合のみ",
                    help="返信が必要な場合はメールアドレスを入力してください"
                )
                
                # 送信ボタン
                submitted = st.form_submit_button("送信", use_container_width=True)
                
                if submitted:
                    if feedback_content.strip():
                        # フィードバックを保存
                        success = save_feedback(
                            feedback_type,
                            feedback_content,
                            email
                        )
                        
                        if success:
                            st.success("✅ フィードバックを送信しました！\nご協力ありがとうございます。")
                        else:
                            st.warning("""
⚠️ 保存に失敗しました。
以下の方法でお送りください：
- 社内チャット: #ai-search-support
- メール: ai-support@mm-international.co.jp
                            """)
                    else:
                        st.error("内容を入力してください。")


def save_feedback(feedback_type: str, content: str, email: str = "") -> bool:
    """
    フィードバックをファイルに保存します。
    
    Args:
        feedback_type: フィードバックのタイプ
        content: フィードバック内容
        email: メールアドレス（オプション）
        
    Returns:
        bool: 保存成功の場合True
    """
    try:
        # フィードバックディレクトリの作成
        feedback_dir = "feedback"
        os.makedirs(feedback_dir, exist_ok=True)
        
        # フィードバックデータ
        feedback_data = {
            "timestamp": datetime.now().isoformat(),
            "type": feedback_type,
            "content": content,
            "email": email,
            "session_id": st.session_state.get("session_id", "unknown")
        }
        
        # ファイル名（タイムスタンプベース）
        filename = f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(feedback_dir, filename)
        
        # JSON形式で保存
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(feedback_data, f, ensure_ascii=False, indent=2)
        
        return True
        
    except Exception as e:
        print(f"フィードバック保存エラー: {e}")
        return False


def display_quick_feedback():
    """
    回答後のクイックフィードバック（役に立った/立たなかった）
    """
    # セッション状態の初期化
    if "show_quick_feedback" not in st.session_state:
        st.session_state.show_quick_feedback = False
    
    if st.session_state.show_quick_feedback:
        st.markdown("---")
        st.markdown("**この回答は役に立ちましたか？**")
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            if st.button("👍 はい", key="feedback_yes", use_container_width=True):
                save_quick_feedback("helpful")
                st.success("フィードバックありがとうございます！")
                st.session_state.show_quick_feedback = False
        
        with col2:
            if st.button("👎 いいえ", key="feedback_no", use_container_width=True):
                save_quick_feedback("not_helpful")
                st.info("フィードバックありがとうございます。改善に努めます。")
                st.session_state.show_quick_feedback = False


def save_quick_feedback(feedback: str):
    """
    クイックフィードバックを保存
    
    Args:
        feedback: "helpful" または "not_helpful"
    """
    try:
        feedback_dir = "feedback"
        os.makedirs(feedback_dir, exist_ok=True)
        
        # 統計ファイルに追記
        stats_file = os.path.join(feedback_dir, "quick_feedback_stats.json")
        
        # 既存の統計を読み込み
        if os.path.exists(stats_file):
            with open(stats_file, "r", encoding="utf-8") as f:
                stats = json.load(f)
        else:
            stats = {"helpful": 0, "not_helpful": 0}
        
        # カウントを更新
        stats[feedback] = stats.get(feedback, 0) + 1
        
        # 保存
        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"クイックフィードバック保存エラー: {e}")


def get_feedback_stats() -> dict:
    """
    フィードバック統計を取得（管理者向け）
    
    Returns:
        dict: 統計情報
    """
    try:
        stats_file = "feedback/quick_feedback_stats.json"
        if os.path.exists(stats_file):
            with open(stats_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"helpful": 0, "not_helpful": 0}
    except:
        return {"helpful": 0, "not_helpful": 0}


def display_feedback_stats():
    """
    フィードバック統計を表示（管理者向け）
    """
    stats = get_feedback_stats()
    total = stats["helpful"] + stats["not_helpful"]
    
    if total > 0:
        helpful_rate = (stats["helpful"] / total) * 100
        
        st.markdown("### 📊 フィードバック統計")
        st.metric("役に立った", f"{stats['helpful']}件")
        st.metric("改善が必要", f"{stats['not_helpful']}件")
        st.metric("満足度", f"{helpful_rate:.1f}%")
    else:
        st.info("まだフィードバックがありません。")


# 使用例
if __name__ == "__main__":
    st.set_page_config(page_title="フィードバック機能テスト")
    
    st.title("フィードバック機能テスト")
    
    # フィードバックフォーム
    display_feedback_form()
    
    # クイックフィードバック
    st.session_state.show_quick_feedback = True
    display_quick_feedback()
    
    # 統計表示
    st.markdown("---")
    display_feedback_stats()

