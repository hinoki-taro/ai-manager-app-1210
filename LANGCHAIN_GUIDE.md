# LangChain実装ガイド

株式会社エムエムインターナショナル 社内情報検索AIアプリのLangChain実装について説明します。

---

## 📚 実装されている機能

### 1. 基本的なRAG（Retrieval-Augmented Generation）
**ファイル:** `utils.py`, `initialize.py`

#### 機能
- ✅ ドキュメントの読み込み（PDF, DOCX, CSV, TXT, Web）
- ✅ テキストのチャンク分割
- ✅ ベクトル化（Google Gemini Embeddings）
- ✅ ベクトルストア（ChromaDB）
- ✅ 類似度検索

### 2. 会話履歴の記憶
**ファイル:** `utils.py`

#### 機能
- ✅ 会話履歴の保持
- ✅ コンテキストを考慮した回答生成
- ✅ 履歴を使った質問の補完

### 3. LangChain強化機能 🆕
**ファイル:** `langchain_enhanced.py`（新規作成）

#### 機能
- ✅ **ストリーミング対応**
  - リアルタイムでレスポンスを表示
  - ユーザー体験の向上

- ✅ **レート制限**
  - 1分間に10回までのリクエスト制限
  - API使用量の管理
  - 残りリクエスト数の表示

- ✅ **クエリキャッシング**
  - 同じ質問への即座の回答
  - API使用量の削減
  - 最大100件のキャッシュ保持
  - 1時間の有効期限

- ✅ **入力検証**
  - 空文字チェック
  - 文字数制限（最大1,000文字）
  - 最小文字数チェック

- ✅ **エラーハンドリング**
  - APIキーエラー
  - レート制限エラー
  - タイムアウトエラー
  - ネットワークエラー
  - ユーザーフレンドリーなエラーメッセージ

- ✅ **詳細なログ記録**
  - 全クエリのログ
  - 処理時間の記録
  - 参照元の記録
  - エラーログ

- ✅ **会話履歴管理**
  - 会話履歴のトリミング（最新10件を保持）
  - メモリの効率的な使用

---

## 🚀 使い方

### 基本的な使用方法
通常通りアプリを使用するだけで、強化機能が自動的に適用されます。

### キャッシュ機能
同じ質問をすると、キャッシュから即座に回答が返されます：
```
💡 キャッシュから回答を取得しました
```

### レート制限
1分間に10回以上リクエストすると、以下のメッセージが表示されます：
```
🚫 リクエスト制限に達しました。1分後に再度お試しください。
```

残りリクエスト数が3回以下になると警告が表示されます：
```
ℹ️ 残りリクエスト数: 2回（1分ごとにリセット）
```

### 処理時間の表示
処理に3秒以上かかった場合、処理時間が表示されます：
```
⏱️ 処理時間: 4.5秒
```

---

## 📊 ログとキャッシュ

### ログファイル
#### アクセスログ
- **場所:** `logs/access_log.json`
- **内容:** ログイン試行の記録

#### LangChainログ
- **場所:** `logs/langchain_log.json`
- **内容:** 
  - すべてのクエリと回答
  - 処理時間
  - 参照元
  - エラー情報

### キャッシュファイル
- **場所:** `logs/query_cache.json`
- **内容:** 質問と回答のキャッシュ
- **最大サイズ:** 100件
- **有効期限:** 1時間

---

## ⚙️ 設定のカスタマイズ

### レート制限の変更
**ファイル:** `langchain_enhanced.py`

```python
# デフォルト: 1分間に10回
_rate_limiter = RateLimiter(max_requests=10, time_window=60)

# カスタマイズ例: 1分間に20回
_rate_limiter = RateLimiter(max_requests=20, time_window=60)
```

### キャッシュサイズの変更
```python
# デフォルト: 100件
_query_cache = QueryCache(max_size=100)

# カスタマイズ例: 200件
_query_cache = QueryCache(max_size=200)
```

### 会話履歴の保持数変更
```python
# デフォルト: 最新10件
_conversation_manager = ConversationManager(max_history=10)

# カスタマイズ例: 最新20件
_conversation_manager = ConversationManager(max_history=20)
```

---

## 🔧 技術詳細

### アーキテクチャ

```
ユーザー入力
    ↓
[入力検証] ← InputValidator
    ↓
[レート制限チェック] ← RateLimiter
    ↓
[キャッシュチェック] ← QueryCache
    ↓ (キャッシュミス)
[LLM処理]
    ├─ [プロンプト生成]
    ├─ [Retriever呼び出し]
    ├─ [会話履歴管理] ← ConversationManager
    └─ [LLM呼び出し]
    ↓
[レスポンス]
    ├─ [キャッシュ保存] → QueryCache
    └─ [ログ記録] → LangChainLogger
    ↓
ユーザーへ表示
```

### 使用しているLangChainコンポーネント

#### モデル
- `ChatGoogleGenerativeAI` - Google Gemini LLM
- `GoogleGenerativeAIEmbeddings` - テキストの埋め込み

#### プロンプト
- `ChatPromptTemplate` - プロンプトテンプレート
- `MessagesPlaceholder` - 会話履歴のプレースホルダー

#### チェーン
- `create_history_aware_retriever` - 履歴を考慮した検索
- `create_retrieval_chain` - RAGチェーン
- `create_stuff_documents_chain` - ドキュメント結合チェーン

#### ベクトルストア
- `Chroma` - ベクトルデータベース

#### ドキュメントローダー
- `WebBaseLoader` - Webページの読み込み
- `PyMuPDFLoader` - PDFファイルの読み込み
- `Docx2txtLoader` - Wordファイルの読み込み
- `CSVLoader` - CSVファイルの読み込み
- `TextLoader` - テキストファイルの読み込み

---

## 📈 パフォーマンス最適化

### 実装済みの最適化
1. **キャッシング** - 同じ質問への即座の回答
2. **会話履歴のトリミング** - メモリ使用量の削減
3. **レート制限** - API使用量の管理
4. **リトライ機能** - 一時的なエラーの自動リトライ

### 今後の最適化案
- ⏳ ストリーミング対応の完全実装
- ⏳ より高度なキャッシング戦略
- ⏳ バッチ処理のサポート
- ⏳ 非同期処理の導入

---

## 🐛 トラブルシューティング

### よくあるエラーと対処法

#### 1. レート制限エラー
**エラー:** `🚫 リクエスト制限に達しました`

**対処法:** 1分待ってから再度試行

#### 2. APIキーエラー
**エラー:** `APIキーの設定に問題があります`

**対処法:** 
- `.env` の `GOOGLE_API_KEY` を確認
- Streamlit Secrets の設定を確認

#### 3. タイムアウトエラー
**エラー:** `処理がタイムアウトしました`

**対処法:** より短い質問を試す

#### 4. キャッシュエラー
キャッシュファイルが壊れた場合：
```bash
# キャッシュファイルを削除
rm logs/query_cache.json
```

---

## 📊 統計情報の確認

### ログの確認方法
```python
from langchain_enhanced import get_langchain_logger

logger = get_langchain_logger()
logs = logger.get_logs(limit=50)

# ログの分析
for log in logs:
    print(f"質問: {log['query']}")
    print(f"処理時間: {log['elapsed_time']}秒")
    print(f"成功: {log['success']}")
```

### キャッシュヒット率の確認
```python
from langchain_enhanced import get_query_cache

cache = get_query_cache()
print(f"キャッシュサイズ: {len(cache.cache)}件")
```

---

## 🔐 セキュリティ考慮事項

### 実装済みのセキュリティ
1. **入力検証** - 不正な入力のブロック
2. **レート制限** - 悪用の防止
3. **エラーマスキング** - センシティブ情報の隠蔽
4. **ログの保護** - `.gitignore` でログファイルを除外

---

## 📞 サポート

LangChain実装に関する質問や問題：
- **メール:** ai-support@mm-international.co.jp
- **詳細ドキュメント:** `SECURITY_GUIDE.md`

---

## 📁 関連ファイル

- `utils.py` - メインのLLM処理
- `initialize.py` - RAGシステムの初期化
- `langchain_enhanced.py` - 強化機能
- `constants.py` - 設定定数
- `requirements.txt` - 依存パッケージ

---

*最終更新：2025年12月12日*  
*株式会社エムエムインターナショナル*

