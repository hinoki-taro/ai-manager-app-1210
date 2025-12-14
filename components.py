"""
このファイルは、画面表示に特化した関数定義のファイルです。
"""

############################################################
# ライブラリの読み込み
############################################################
import streamlit as st
import utils
import constants as ct
import avatar_manager


############################################################
# 関数定義
############################################################

def display_app_title():
    """
    タイトル表示（カスタムスタイル適用）
    """
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem; padding: 1.5rem; 
                background: linear-gradient(135deg, #E0F2FE 0%, #FFFFFF 100%);
                border-radius: 12px; box-shadow: 0 2px 8px rgba(30, 58, 138, 0.1);">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
        <div style="font-size: 1.75rem; font-weight: 700; color: #1E3A8A; line-height: 1.4;">
            {ct.APP_NAME}
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_select_mode():
    """
    回答モードのラジオボタンを表示（カスタムスタイル適用）
    """
    # サイドバーに回答モードを選択する用のラジオボタンを表示
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E3A8A 0%, #0EA5E9 100%); 
                    color: white; padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem;
                    text-align: center; font-weight: 600;">
            🎯 利用目的
        </div>
        """, unsafe_allow_html=True)
        
        # デフォルト値を取得（session_stateに値があればそれを使用）
        default_index = 1  # 「社内問い合わせ」をデフォルトに
        if "mode" in st.session_state:
            # 既存のmodeから適切なindexを計算
            if st.session_state.mode == ct.ANSWER_MODE_1:
                default_index = 0
            elif st.session_state.mode == ct.ANSWER_MODE_2:
                default_index = 1
        
        st.session_state.mode = st.radio(
            label="利用目的を選択してください",
            options=[ct.ANSWER_MODE_1, ct.ANSWER_MODE_2],
            index=default_index,
            label_visibility="collapsed"
        )


def display_help_section():
    """
    ヘルプセクションの表示
    """
    with st.sidebar:
        st.markdown("---")
        with st.expander("📚 ヘルプ・使い方", expanded=False):
            # 検索アイコンを表示
            col1, col2 = st.columns([1, 5])
            with col1:
                avatar_manager.show_icon("inquiry", size=40)
            with col2:
                st.markdown("#### クイックガイド")
            
            st.markdown("""
**質問のコツ:**
- ✅ 具体的に聞く
- ✅ 1つずつ質問
- ✅ キーワードを含める

**質問例:**
```
「有給休暇の申請方法は？」
「経費精算の期限はいつ？」
「会議室の予約方法を教えて」
```

**困ったときは:**
- 🔄 履歴をクリア
- 🔀 モードを切り替え
- 📝 質問を変えてみる

**サポート:**
#ai-search-support
            """)
            
            # ドキュメントへのリンク
            st.markdown("---")
            st.markdown("""
**📖 詳細ガイド:**
- [利用ガイド](USER_GUIDE.md)
- [よくある質問](FAQ.md)
- [トラブル対処](TROUBLESHOOTING.md)
            """)


def display_initial_ai_message():
    """
    AIメッセージの初期表示
    """
    # サイドバーに機能説明を表示
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 使い方")
        st.markdown("こんにちは。私は社内文書の情報をもとに回答する生成AIチャットボットです。上記で利用目的を選択し、画面下部のチャット欄からメッセージを送信してください。")

        # 「社内文書検索」の機能説明
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E0F2FE 0%, #FFFFFF 100%); 
                    padding: 1rem; border-radius: 8px; border-left: 4px solid #0EA5E9; margin-bottom: 1rem;">
            <strong style="color: #1E3A8A;">📄 社内文書検索</strong>
        </div>
        """, unsafe_allow_html=True)
        st.info("入力内容と関連性が高い社内文書のありかを検索できます。", icon="🔍")
        # 「st.code()」を使うとコードブロックの装飾で表示される
        # 「wrap_lines=True」で折り返し設定、「language=None」で非装飾とする
        st.code("【入力例】\n社員の育成方針に関するMTGの議事録", wrap_lines=True, language=None)

        # 「社内問い合わせ」の機能説明
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E0F2FE 0%, #FFFFFF 100%); 
                    padding: 1rem; border-radius: 8px; border-left: 4px solid #0EA5E9; margin-bottom: 1rem;">
            <strong style="color: #1E3A8A;">💬 社内問い合わせ</strong>
        </div>
        """, unsafe_allow_html=True)
        st.info("質問・要望に対して、社内文書の情報をもとに回答を得られます。", icon="🤖")
        st.code("【入力例】\n人事部に所属している従業員情報を一覧化して", wrap_lines=True, language=None)


def display_conversation_log():
    """
    会話ログの一覧表示
    """
    # 会話ログのループ処理
    for message in st.session_state.messages:
        # 「message」辞書の中の「role」キーには「user」か「assistant」が入っている
        # アバターを設定（ユーザーは絵文字、AIは画像）
        avatar = "👤" if message["role"] == "user" else avatar_manager.AvatarManager.AVATAR_PATH
        with st.chat_message(message["role"], avatar=avatar):

            # ユーザー入力値の場合、そのままテキストを表示するだけ
            if message["role"] == "user":
                st.markdown(message["content"])
            
            # LLMからの回答の場合
            else:
                # 「社内文書検索」の場合、テキストの種類に応じて表示形式を分岐処理
                if message["content"]["mode"] == ct.ANSWER_MODE_1:
                    
                    # ファイルのありかの情報が取得できた場合（通常時）の表示処理
                    if not "no_file_path_flg" in message["content"]:
                        # ==========================================
                        # ユーザー入力値と最も関連性が高いメインドキュメントのありかを表示
                        # ==========================================
                        # 補足文の表示
                        st.markdown(message["content"]["main_message"])

                        # 参照元のありかに応じて、適したアイコンを取得
                        icon = utils.get_source_icon(message['content']['main_file_path'])
                        # 参照元ドキュメントのページ番号が取得できた場合にのみ、ページ番号を表示
                        if "main_page_number" in message["content"]:
                            st.success(f"{message['content']['main_file_path']} (ページ: {message['content']['main_page_number'] + 1})", icon=icon)
                        else:
                            st.success(f"{message['content']['main_file_path']}", icon=icon)
                        
                        # ==========================================
                        # ユーザー入力値と関連性が高いサブドキュメントのありかを表示
                        # ==========================================
                        if "sub_message" in message["content"]:
                            # 補足メッセージの表示
                            st.markdown(message["content"]["sub_message"])

                            # サブドキュメントのありかを一覧表示
                            for sub_choice in message["content"]["sub_choices"]:
                                # 参照元のありかに応じて、適したアイコンを取得
                                icon = utils.get_source_icon(sub_choice['source'])
                                # 参照元ドキュメントのページ番号が取得できた場合にのみ、ページ番号を表示
                                if "page_number" in sub_choice:
                                    st.info(f"{sub_choice['source']} (ページ: {sub_choice['page_number'] + 1})", icon=icon)
                                else:
                                    st.info(f"{sub_choice['source']}", icon=icon)
                    # ファイルのありかの情報が取得できなかった場合、LLMからの回答のみ表示
                    else:
                        st.markdown(message["content"]["answer"])
                
                # 「社内問い合わせ」の場合の表示処理
                else:
                    # LLMからの回答を表示
                    st.markdown(message["content"]["answer"])

                    # 参照元のありかを一覧表示
                    if "file_info_list" in message["content"]:
                        # 区切り線の表示
                        st.divider()
                        # 「情報源」の文字を太字で表示
                        st.markdown(f"##### {message['content']['message']}")
                        # ドキュメントのありかを一覧表示
                        for file_info in message["content"]["file_info_list"]:
                            # 参照元のありかに応じて、適したアイコンを取得
                            icon = utils.get_source_icon(file_info)
                            st.info(file_info, icon=icon)


def display_search_llm_response(llm_response):
    """
    「社内文書検索」モードにおけるLLMレスポンスを表示

    Args:
        llm_response: LLMからの回答

    Returns:
        LLMからの回答を画面表示用に整形した辞書データ
    """
    # LLMからのレスポンスに参照元情報が入っており、かつ「該当資料なし」が回答として返された場合
    if llm_response["context"] and llm_response["answer"] != ct.NO_DOC_MATCH_ANSWER:
        
        # 成功アイコンを表示
        col1, col2 = st.columns([1, 20])
        with col1:
            avatar_manager.show_icon("success", size=32)

        # ==========================================
        # ユーザー入力値と最も関連性が高いメインドキュメントのありかを表示
        # ==========================================
        # LLMからのレスポンス（辞書）の「context」属性の中の「0」に、最も関連性が高いドキュメント情報が入っている
        main_file_path = llm_response["context"][0].metadata["source"]

        # 補足メッセージの表示
        main_message = "入力内容に関する情報は、以下のファイルに含まれている可能性があります。"
        st.markdown(main_message)
        
        # ファイル形式のラベルを取得
        file_type = utils.get_file_type_label(main_file_path)
        
        # 参照元のありかに応じて、適したアイコンを取得
        icon = utils.get_source_icon(main_file_path)
        # ページ番号が取得できた場合のみ、ページ番号を表示（ドキュメントによっては取得できない場合がある）
        if "page" in llm_response["context"][0].metadata:
            # ページ番号を取得
            main_page_number = llm_response["context"][0].metadata["page"]
            # 「ファイル形式」「メインドキュメントのファイルパス」と「ページ番号」を表示
            st.success(f"**[{file_type}]** {main_file_path} (ページ: {main_page_number + 1})", icon=icon)
        else:
            # 「ファイル形式」「メインドキュメントのファイルパス」を表示
            st.success(f"**[{file_type}]** {main_file_path}", icon=icon)

        # ==========================================
        # ユーザー入力値と関連性が高いサブドキュメントのありかを表示
        # ==========================================
        # メインドキュメント以外で、関連性が高いサブドキュメントを格納する用のリストを用意
        sub_choices = []
        # 重複チェック用のリストを用意
        duplicate_check_list = []

        # ドキュメントが2件以上検索できた場合（サブドキュメントが存在する場合）のみ、サブドキュメントのありかを一覧表示
        # 「source_documents」内のリストの2番目以降をスライスで参照（2番目以降がなければfor文内の処理は実行されない）
        for document in llm_response["context"][1:]:
            # ドキュメントのファイルパスを取得
            sub_file_path = document.metadata["source"]

            # メインドキュメントのファイルパスと重複している場合、処理をスキップ（表示しない）
            if sub_file_path == main_file_path:
                continue
            
            # 同じファイル内の異なる箇所を参照した場合、2件目以降のファイルパスに重複が発生する可能性があるため、重複を除去
            if sub_file_path in duplicate_check_list:
                continue

            # 重複チェック用のリストにファイルパスを順次追加
            duplicate_check_list.append(sub_file_path)
            
            # ページ番号が取得できない場合のための分岐処理
            if "page" in document.metadata:
                # ページ番号を取得
                sub_page_number = document.metadata["page"]
                # 「サブドキュメントのファイルパス」と「ページ番号」の辞書を作成
                sub_choice = {"source": sub_file_path, "page_number": sub_page_number}
            else:
                # 「サブドキュメントのファイルパス」の辞書を作成
                sub_choice = {"source": sub_file_path}
            
            # 後ほど一覧表示するため、サブドキュメントに関する情報を順次リストに追加
            sub_choices.append(sub_choice)
        
        # サブドキュメントが存在する場合のみの処理
        if sub_choices:
            # 補足メッセージの表示
            sub_message = "その他、ファイルありかの候補を提示します。"
            st.markdown(sub_message)

            # サブドキュメントに対してのループ処理
            for sub_choice in sub_choices:
                # ファイル形式のラベルを取得
                file_type = utils.get_file_type_label(sub_choice['source'])
                # 参照元のありかに応じて、適したアイコンを取得
                icon = utils.get_source_icon(sub_choice['source'])
                # ページ番号が取得できない場合のための分岐処理
                if "page_number" in sub_choice:
                    # 「ファイル形式」「サブドキュメントのファイルパス」と「ページ番号」を表示
                    st.info(f"**[{file_type}]** {sub_choice['source']} (ページ: {sub_choice['page_number'] + 1})", icon=icon)
                else:
                    # 「ファイル形式」「サブドキュメントのファイルパス」を表示
                    st.info(f"**[{file_type}]** {sub_choice['source']}", icon=icon)
        
        # 表示用の会話ログに格納するためのデータを用意
        # - 「mode」: モード（「社内文書検索」or「社内問い合わせ」）
        # - 「main_message」: メインドキュメントの補足メッセージ
        # - 「main_file_path」: メインドキュメントのファイルパス
        # - 「main_page_number」: メインドキュメントのページ番号
        # - 「sub_message」: サブドキュメントの補足メッセージ
        # - 「sub_choices」: サブドキュメントの情報リスト
        content = {}
        content["mode"] = ct.ANSWER_MODE_1
        content["main_message"] = main_message
        content["main_file_path"] = main_file_path
        # メインドキュメントのページ番号は、取得できた場合にのみ追加
        if "page" in llm_response["context"][0].metadata:
            content["main_page_number"] = main_page_number
        # サブドキュメントの情報は、取得できた場合にのみ追加
        if sub_choices:
            content["sub_message"] = sub_message
            content["sub_choices"] = sub_choices
    
    # LLMからのレスポンスに、ユーザー入力値と関連性の高いドキュメント情報が入って「いない」場合
    else:
        # 空状態のイラストを表示
        avatar_manager.show_empty_state("入力内容と関連する社内文書が見つかりませんでした")
        
        # 関連ドキュメントが取得できなかった場合のメッセージ表示
        st.info("入力内容を変更してみてください。", icon="💡")

        # 表示用の会話ログに格納するためのデータを用意
        # - 「mode」: モード（「社内文書検索」or「社内問い合わせ」）
        # - 「answer」: LLMからの回答
        # - 「no_file_path_flg」: ファイルパスが取得できなかったことを示すフラグ（画面を再描画時の分岐に使用）
        content = {}
        content["mode"] = ct.ANSWER_MODE_1
        content["answer"] = ct.NO_DOC_MATCH_MESSAGE
        content["no_file_path_flg"] = True
    
    return content


def display_contact_llm_response(llm_response):
    """
    「社内問い合わせ」モードにおけるLLMレスポンスを表示

    Args:
        llm_response: LLMからの回答

    Returns:
        LLMからの回答を画面表示用に整形した辞書データ
    """
    # LLMからの回答を表示
    st.markdown(llm_response["answer"])

    # ユーザーの質問・要望に適切な回答を行うための情報が、社内文書のデータベースに存在しなかった場合
    if llm_response["answer"] != ct.INQUIRY_NO_MATCH_ANSWER:
        # 区切り線を表示
        st.divider()

        # 補足メッセージを表示
        message = "情報源"
        st.markdown(f"##### {message}")

        # 参照元のファイルパスの一覧を格納するためのリストを用意
        file_path_list = []
        file_info_list = []

        # LLMが回答生成の参照元として使ったドキュメントの一覧が「context」内のリストの中に入っているため、ループ処理
        for document in llm_response["context"]:
            # ファイルパスを取得
            file_path = document.metadata["source"]
            # ファイルパスの重複は除去
            if file_path in file_path_list:
                continue

            # ファイル形式のラベルを取得
            file_type = utils.get_file_type_label(file_path)
            
            # ページ番号が取得できた場合のみ、ページ番号を表示（ドキュメントによっては取得できない場合がある）
            if "page" in document.metadata:
                # ページ番号を取得
                page_number = document.metadata["page"]
                # 「ファイル形式」「ファイルパス」と「ページ番号」
                file_info = f"**[{file_type}]** {file_path} (ページ: {page_number + 1})"
            else:
                # 「ファイル形式」「ファイルパス」のみ
                file_info = f"**[{file_type}]** {file_path}"

            # 参照元のありかに応じて、適したアイコンを取得
            icon = utils.get_source_icon(file_path)
            # ファイル情報を表示
            st.info(file_info, icon=icon)

            # 重複チェック用に、ファイルパスをリストに順次追加
            file_path_list.append(file_path)
            # ファイル情報をリストに順次追加
            file_info_list.append(file_info)

    # 表示用の会話ログに格納するためのデータを用意
    # - 「mode」: モード（「社内文書検索」or「社内問い合わせ」）
    # - 「answer」: LLMからの回答
    # - 「message」: 補足メッセージ
    # - 「file_path_list」: ファイルパスの一覧リスト
    content = {}
    content["mode"] = ct.ANSWER_MODE_2
    content["answer"] = llm_response["answer"]
    # 参照元のドキュメントが取得できた場合のみ
    if llm_response["answer"] != ct.INQUIRY_NO_MATCH_ANSWER:
        content["message"] = message
        content["file_info_list"] = file_info_list

    return content