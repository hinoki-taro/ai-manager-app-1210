# 完全無料運用への移行 - 完了サマリー

株式会社エムエムインターナショナル 社内情報検索AIアプリ

---

## ✅ 完了した準備

### 1. 自動切り替え機能
- ✅ `initialize.py` を修正
- ✅ OpenAI EmbeddingsとGoogle Gemini Embeddingsの両方に対応
- ✅ APIキーの設定に応じて自動的に切り替え

### 2. 無料版への移行スクリプト
- ✅ `switch_to_free.bat` を作成
- ✅ Google Gemini APIでベクターストアを再作成できる
- ✅ 完全無料で運用可能

### 3. ドキュメント
- ✅ `FREE_TIER_MIGRATION_GUIDE.md` を作成
- ✅ `FUTURE_OPERATION_GUIDE.md` を作成
- ✅ 詳細な移行手順と運用方針を記載

---

## 🎯 今後の流れ

### 今回（2025年12月13日）- 動作確認

#### 1. OpenAI APIでベクターストアを作成
```
install_langchain_openai.bat をダブルクリック
↓
.env に OPENAI_API_KEY を設定
↓
create_vectorstore_openai.bat をダブルクリック
↓
約3-5分待つ（約1-2円）
```

#### 2. GitHubにプッシュ
```bash
git add .
git commit -m "Add OpenAI vectorstore and free tier migration tools"
git push origin main
```

#### 3. Streamlit CloudでSecretsを設定
```toml
OPENAI_API_KEY = "sk-proj-..."
GOOGLE_API_KEY = "AIzaSy..."

[auth]
password = "mmi8686"
session_timeout_minutes = 60
max_login_attempts = 5
```

#### 4. アプリを再起動して動作確認

---

### 明日以降（2025年12月14日以降）- 完全無料化

#### 1. .envを更新
```
# OPENAI_API_KEY を削除またはコメントアウト
# OPENAI_API_KEY=sk-proj-...

GOOGLE_API_KEY=AIzaSyBlp0GgqOrY5VLVP703PKk-J1UKuDHuhKQ
```

#### 2. ベクターストアを再作成
```
switch_to_free.bat をダブルクリック
↓
約5-10分待つ（完全無料）
```

#### 3. GitHubにプッシュ
```bash
git add vectorstore/
git commit -m "Switch to free tier (Google Gemini Embeddings)"
git push origin main
```

#### 4. Streamlit CloudでSecretsを更新
```toml
# OPENAI_API_KEY を削除
GOOGLE_API_KEY = "AIzaSy..."

[auth]
password = "mmi8686"
session_timeout_minutes = 60
max_login_attempts = 5
```

#### 5. アプリを再起動
- 完全無料で動作！

---

## 🔄 自動切り替えの仕組み

### どちらのAPIキーが設定されているかで自動判断

#### パターン1: OpenAI API使用（有料）
```toml
# Streamlit Secrets
OPENAI_API_KEY = "sk-proj-..."
GOOGLE_API_KEY = "AIzaSy..."  # LLM用
```

**動作:**
- ✅ ベクターストア読み込み: OpenAI Embeddings
- ✅ LLM（チャット）: Google Gemini API
- 💰 コスト: 約360円/年

---

#### パターン2: Google Gemini API使用（無料）
```toml
# Streamlit Secrets
GOOGLE_API_KEY = "AIzaSy..."  # 埋め込み & LLM両方
```

**動作:**
- ✅ ベクターストア読み込み: Google Gemini Embeddings
- ✅ LLM（チャット）: Google Gemini API
- 💰 コスト: 完全無料

---

## 💡 自動切り替えのロジック

`initialize.py` の処理フロー：

```python
# APIキーを確認
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

# どちらを使うか決定
if openai_api_key:
    # OpenAI Embeddings を使用
    embeddings = OpenAIEmbeddings(...)
elif google_api_key:
    # Google Gemini Embeddings を使用（完全無料）
    embeddings = GoogleGenerativeAIEmbeddings(...)
else:
    # エラー
    raise ValueError("APIキーが設定されていません")
```

---

## 📊 コスト比較

### パターン1: OpenAI API（今回）
| 項目 | コスト |
|------|--------|
| ベクターストア作成 | 約1-2円（一度だけ） |
| クエリの埋め込み | 約0.01円/質問 |
| LLM（チャット） | 無料 |
| **月間コスト** | **約30円** |
| **年間コスト** | **約360円** |

### パターン2: Google Gemini API（明日以降）
| 項目 | コスト |
|------|--------|
| ベクターストア作成 | 無料 |
| クエリの埋め込み | 無料 |
| LLM（チャット） | 無料 |
| **月間コスト** | **完全無料** |
| **年間コスト** | **完全無料** |

---

## 🎯 推奨する運用方針

### 【推奨】完全無料運用

1. **今回:** OpenAI APIで動作確認（約1-2円）
2. **明日:** Google Gemini APIに切り替え（無料）
3. **以降:** 完全無料で運用

### データ更新時（月1回程度）
1. ローカルで `data/` フォルダを更新
2. `switch_to_free.bat` を実行（無料）
3. GitHubにプッシュ
4. Streamlit Cloudで自動デプロイ

### 日常運用（社員）
- 完全無料
- 毎日1500質問まで無料
- 何も気にせず使える

---

## ⚠️ 注意事項

### Google Gemini APIの無料枠について

#### 使えるもの
- ✅ **LLM（チャット）:** 毎日1500リクエスト
- ✅ **埋め込みAPI:** 少ない（月1回のデータ更新なら問題なし）

#### 制限
- 一度に大量の埋め込みを行うと、クォータを超過する可能性
- 24時間でリセットされる

### 実行タイミング
- **`switch_to_free.bat` は24時間経過後に実行**
- 早く実行すると、クォータエラーが発生

---

## 📞 サポート

### 内部サポート
- **メール:** ai-support@mm-international.co.jp

### ドキュメント
- **移行手順:** `FREE_TIER_MIGRATION_GUIDE.md`
- **運用方針:** `FUTURE_OPERATION_GUIDE.md`
- **ベクターストア作成:** `VECTORSTORE_SETUP_GUIDE.md`

---

## 📁 作成したファイル

### スクリプト
- ✅ `create_vectorstore_openai.py` - OpenAI APIでベクターストア作成
- ✅ `create_vectorstore_openai.bat` - 上記のバッチファイル
- ✅ `switch_to_free.bat` - 無料版への切り替えスクリプト
- ✅ `install_langchain_openai.bat` - 必要なパッケージをインストール

### ドキュメント
- ✅ `FREE_TIER_MIGRATION_GUIDE.md` - 無料版への移行ガイド
- ✅ `FUTURE_OPERATION_GUIDE.md` - 今後の運用ガイド
- ✅ `COMPLETE_FREE_SETUP_SUMMARY.md` - このドキュメント

### 修正したファイル
- ✅ `initialize.py` - 自動切り替え機能を追加
- ✅ `constants.py` - 埋め込みモデルの定義を追加
- ✅ `requirements.txt` - langchain-openai を追加

---

## 🚀 次のステップ

### 今すぐやること

1. **`install_langchain_openai.bat` をダブルクリック**
2. **`.env` に OPENAI_API_KEY を設定**
3. **`create_vectorstore_openai.bat` をダブルクリック**
4. **GitHubにプッシュ**
5. **Streamlit Cloudで動作確認**

### 明日やること

1. **`.env` を GOOGLE_API_KEY に変更**
2. **`switch_to_free.bat` をダブルクリック**
3. **GitHubにプッシュ**
4. **完全無料化達成！**

---

**作成日:** 2025年12月13日  
**対象:** 株式会社エムエムインターナショナル  
**アプリ名:** mmi-ai-manager  
**バージョン:** 1.0

---

**すべての準備が完了しました！今すぐ動作確認を始めてください！** 🎉



