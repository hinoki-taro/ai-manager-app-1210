"""
OpenAI APIを使ってローカルでベクターストアを事前作成するスクリプト

使い方:
1. .envファイルにOPENAI_API_KEYを設定
2. このスクリプトを実行: python create_vectorstore_openai.py
3. vectorstore/フォルダが作成される
4. GitHubにプッシュする
"""

import os
from dotenv import load_dotenv
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

import constants as ct
from initialize import load_data_sources, adjust_string

# 環境変数の読み込み
load_dotenv()

def create_vectorstore():
    """ベクターストアをローカルに作成（OpenAI API使用）"""
    
    print("=" * 60)
    print("ベクターストア作成スクリプト (OpenAI API)")
    print("=" * 60)
    
    # ステップ1: データの読み込み
    print("\n🔄 データを読み込んでいます...")
    docs_all = load_data_sources()
    print(f"✓ {len(docs_all)}個のドキュメントを読み込みました")
    
    # ステップ2: テキストの正規化
    print("\n🔄 テキストを正規化しています...")
    for doc in docs_all:
        doc.page_content = adjust_string(doc.page_content)
        for key in doc.metadata:
            doc.metadata[key] = adjust_string(doc.metadata[key])
    print("✓ テキストの正規化が完了しました")
    
    # ステップ3: 埋め込みモデルの初期化
    print("\n🔄 埋め込みモデルを初期化しています...")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY が設定されていません。\n"
            ".envファイルに以下を設定してください:\n"
            'OPENAI_API_KEY="your-api-key-here"'
        )
    
    print(f"✓ APIキーを取得しました（先頭10文字: {openai_api_key[:10]}...）")
    
    # OpenAI Embeddingsを使用
    embeddings = OpenAIEmbeddings(
        model=ct.EMBEDDING_MODEL_OPENAI,
        openai_api_key=openai_api_key
    )
    print("✓ 埋め込みモデルの初期化が完了しました")
    
    # ステップ4: ドキュメントの分割
    print("\n🔄 ドキュメントを分割しています...")
    text_splitter = CharacterTextSplitter(
        chunk_size=ct.CHUNK_SIZE,
        chunk_overlap=ct.CHUNK_OVERLAP,
        separator="\n"
    )
    splitted_docs = text_splitter.split_documents(docs_all)
    print(f"✓ {len(splitted_docs)}個のチャンクに分割しました")
    
    # ステップ5: ベクターストアの作成と保存
    print("\n🔄 ベクターストアを作成しています（これには数分かかる場合があります）...")
    print("⚠️ この処理中にOpenAI APIのクォータを消費します（少額の費用）")
    
    # persist_directoryを指定してローカルに保存
    db = Chroma.from_documents(
        documents=splitted_docs,
        embedding=embeddings,
        persist_directory="./vectorstore"  # ローカルディレクトリに保存
    )
    
    print("✓ ベクターストアの作成が完了しました")
    print(f"✓ ベクターストアを保存しました: ./vectorstore/")
    
    print("\n" + "=" * 60)
    print("✅ 完了！")
    print("=" * 60)
    print("\n次のステップ:")
    print("1. vectorstore/ フォルダが作成されたことを確認")
    print("2. 以下のコマンドでGitHubにプッシュ:")
    print("   git add vectorstore/")
    print("   git add initialize.py")
    print("   git add create_vectorstore_openai.py")
    print('   git commit -m "Add pre-built vectorstore (OpenAI)"')
    print("   git push origin main")
    print("3. Streamlit Cloudでアプリを再起動")
    print("\n💰 コスト:")
    print(f"   - 216チャンク × OpenAI Embedding API")
    print(f"   - 推定コスト: 約$0.01-0.02（1-2円程度）")

if __name__ == "__main__":
    try:
        create_vectorstore()
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        print("\n詳細:")
        import traceback
        traceback.print_exc()



