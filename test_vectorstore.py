"""
ベクターストアのテストスクリプト
JINNYの情報が正しく検索できるか確認します
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 環境変数の読み込み
load_dotenv()

# OpenAI APIキーの取得
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("[ERROR] OPENAI_API_KEY が設定されていません")
    exit(1)

print("=" * 60)
print("ベクターストア検索テスト")
print("=" * 60)

# 埋め込みモデルの初期化
print("\n[1] 埋め込みモデルを初期化しています...")
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=openai_api_key
)
print("[OK] 埋め込みモデルの初期化完了")

# ベクターストアの読み込み
vectorstore_path = "./vectorstore"
print(f"\n[2] ベクターストアを読み込んでいます: {vectorstore_path}")

if not Path(vectorstore_path).exists():
    print(f"[ERROR] ベクターストアが見つかりません: {vectorstore_path}")
    exit(1)

db = Chroma(
    persist_directory=vectorstore_path,
    embedding_function=embeddings
)
print("[OK] ベクターストアの読み込み完了")

# ドキュメント数の確認
print("\n[3] ベクターストアの内容を確認しています...")
try:
    collection = db._collection
    doc_count = collection.count()
    print(f"[OK] ドキュメント数: {doc_count}件")
    
    if doc_count == 0:
        print("[ERROR] ベクターストアが空です！")
        exit(1)
except Exception as e:
    print(f"[WARNING] ドキュメント数の確認に失敗: {e}")

# JINNYで検索
print("\n[4] 'JINNY' で検索しています...")
query = "JINNY"
results = db.similarity_search(query, k=5)

print(f"\n検索結果: {len(results)}件")
print("=" * 60)

if len(results) == 0:
    print("[ERROR] 検索結果が0件です！")
    print("\n考えられる原因:")
    print("1. ベクターストアに情報が含まれていない")
    print("2. 埋め込みモデルの不一致")
    print("3. ベクターストアの破損")
else:
    for i, doc in enumerate(results, 1):
        print(f"\n【結果 {i}】")
        print(f"ソース: {doc.metadata.get('source', 'N/A')}")
        print(f"内容（最初の200文字）:")
        print(doc.page_content[:200])
        print("-" * 60)

# 日本語での検索
print("\n[5] 'JINNYについて教えてください' で検索しています...")
query_jp = "JINNYについて教えてください"
results_jp = db.similarity_search(query_jp, k=5)

print(f"\n検索結果: {len(results_jp)}件")
print("=" * 60)

if len(results_jp) > 0:
    for i, doc in enumerate(results_jp, 1):
        print(f"\n【結果 {i}】")
        print(f"ソース: {doc.metadata.get('source', 'N/A')}")
        print(f"内容（最初の200文字）:")
        print(doc.page_content[:200])
        print("-" * 60)
else:
    print("[ERROR] 日本語検索でも結果が0件です！")

print("\n" + "=" * 60)
print("テスト完了")
print("=" * 60)

