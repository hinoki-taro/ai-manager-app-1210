# API切り替え詳細ガイド

Google GeminiとOpenAIを素早く切り替えるための詳細ガイドです。

---

## 🎯 クイックスタート

### OpenAIに切り替える（3ステップ）

```bash
# 1. ファイルをコピー
copy openai_version\utils_openai.py utils.py
copy openai_version\initialize_openai.py initialize.py

# 2. パッケージをインストール
pip install langchain-openai

# 3. APIキーを設定（.envファイルを編集）
# OPENAI_API_KEY=your_key_here

# 完了！アプリを起動
streamlit run main.py
```

### Geminiに戻す（2ステップ）

```bash
# 1. Gitから復元
git checkout utils.py initialize.py

# 2. APIキーを設定（.envファイルを編集）
# GOOGLE_API_KEY=your_key_here

# 完了！アプリを起動
streamlit run main.py
```

---

## 📋 切り替えバッチスクリプト

### OpenAIに切り替え

**`switch_to_openai.bat`** を作成：

```batch
@echo off
echo ========================================
echo OpenAI版に切り替えます
echo ========================================

echo.
echo [1/4] 現在のファイルをバックアップ中...
copy utils.py utils_gemini_backup.py
copy initialize.py initialize_gemini_backup.py

echo.
echo [2/4] OpenAI版のファイルをコピー中...
copy openai_version\utils_openai.py utils.py
copy openai_version\initialize_openai.py initialize.py

echo.
echo [3/4] パッケージをインストール中...
call env\Scripts\activate.bat
pip install langchain-openai --quiet

echo.
echo [4/4] 完了！
echo.
echo ========================================
echo 次のステップ:
echo 1. .envファイルを編集してOPENAI_API_KEYを設定
echo 2. streamlit run main.py でアプリを起動
echo ========================================

pause
```

### Geminiに切り替え

**`switch_to_gemini.bat`** を作成：

```batch
@echo off
echo ========================================
echo Gemini版に切り替えます
echo ========================================

echo.
echo [1/3] 現在のファイルをバックアップ中...
copy utils.py utils_openai_backup.py
copy initialize.py initialize_openai_backup.py

echo.
echo [2/3] Gemini版のファイルを復元中...
copy utils_gemini_backup.py utils.py
copy initialize_gemini_backup.py initialize.py

echo.
echo [3/3] 完了！
echo.
echo ========================================
echo 次のステップ:
echo 1. .envファイルを編集してGOOGLE_API_KEYを設定
echo 2. streamlit run main.py でアプリを起動
echo ========================================

pause
```

---

## 🔑 APIキー管理

### .envファイルの管理

両方のAPIキーを `.env` に記載しておくと便利です：

```env
# Google Gemini APIキー
GOOGLE_API_KEY=AIzaSyBlp0GgqOrY5VLVP703PKk-J1UKuDHuhKQ

# OpenAI APIキー
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# 認証設定
APP_PASSWORD=your_secure_password
```

### Streamlit Secrets（Web版）

Streamlit Community Cloudにデプロイする場合：

#### `.streamlit/secrets.toml`

```toml
# Google Gemini APIキー
GOOGLE_API_KEY = "AIzaSyBlp0GgqOrY5VLVP703PKk-J1UKuDHuhKQ"

# OpenAI APIキー
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxx"

# 認証設定
APP_PASSWORD = "your_secure_password"
```

---

## 📊 パフォーマンス比較

### 実測値（参考）

| 項目 | Google Gemini | OpenAI GPT-4o-mini |
|------|---------------|-------------------|
| **初回起動時間** | 約15秒 | 約10秒 |
| **質問への応答時間** | 2〜5秒 | 1〜3秒 |
| **埋め込み処理** | 遅い（無料枠制限） | 速い |
| **回答の質** | 良好 | 非常に良好 |
| **日本語対応** | 良好 | 非常に良好 |
| **コスト（月1000質問）** | 無料 | 約$5〜$10 |

---

## 🔍 差分の確認

### 主な違い

#### `utils.py` vs `utils_openai.py`

```python
# Google Gemini版
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=ct.MODEL, temperature=ct.TEMPERATURE)

# OpenAI版
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model=ct.MODEL_OPENAI, temperature=ct.TEMPERATURE)
```

#### `initialize.py` vs `initialize_openai.py`

```python
# Google Gemini版
from langchain_google_genai import GoogleGenerativeAIEmbeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# OpenAI版
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
```

---

## 🧪 テスト方法

### OpenAI版のテスト

```bash
# 1. OpenAIに切り替え
copy openai_version\utils_openai.py utils.py
copy openai_version\initialize_openai.py initialize.py

# 2. アプリを起動
streamlit run main.py

# 3. テスト質問
「JINNYの導入台数は？」
「会社の設立年は？」
「清掃3.0とは何ですか？」

# 4. ログを確認
cat logs\langchain_log.json
```

### Gemini版のテスト

```bash
# 1. Geminiに戻す
git checkout utils.py initialize.py

# 2. アプリを起動
streamlit run main.py

# 3. 同じテスト質問で比較
```

---

## 🛡️ セキュリティ

### APIキーの保護

#### `.gitignore` に追加済み
```
.env
.streamlit/secrets.toml
utils_*_backup.py
initialize_*_backup.py
```

#### APIキーの定期的なローテーション
- **推奨頻度:** 3ヶ月ごと
- **OpenAI:** https://platform.openai.com/api-keys
- **Google:** https://console.cloud.google.com/apis/credentials

---

## 💡 ベストプラクティス

### 開発フロー

```
開発・テスト
    ↓
Google Gemini（無料）
    ↓
テスト完了
    ↓
本番デプロイ
    ↓
OpenAI（有料・高品質）
```

### コスト管理

#### OpenAIの使用量監視
```bash
# 使用量を確認
# https://platform.openai.com/usage

# 月間上限を設定
# https://platform.openai.com/account/limits
# 推奨: $20〜$50/月
```

#### Geminiの使用量監視
```bash
# 使用量を確認
# https://ai.google.dev/gemini-api/docs/rate-limits

# 無料枠:
# - 1日1,500リクエスト
# - 月間150万トークン
```

---

## 📈 今後の拡張

### 動的な切り替え機能

将来的に、アプリ内でAPIを切り替えられるようにする案：

```python
# constants.py
API_PROVIDER = os.getenv("API_PROVIDER", "gemini")  # "gemini" or "openai"

# utils.py
if ct.API_PROVIDER == "openai":
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model=ct.MODEL_OPENAI, temperature=ct.TEMPERATURE)
else:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model=ct.MODEL, temperature=ct.TEMPERATURE)
```

### フォールバック機能

片方のAPIがエラーの場合、もう片方に自動で切り替える：

```python
try:
    # OpenAIで試行
    llm = ChatOpenAI(...)
    response = llm.invoke(...)
except Exception as e:
    # Geminiにフォールバック
    llm = ChatGoogleGenerativeAI(...)
    response = llm.invoke(...)
```

---

## 📞 サポート

- **メール:** ai-support@mm-international.co.jp
- **関連ドキュメント:**
  - `README_OPENAI.md` - OpenAI版の概要
  - `LANGCHAIN_GUIDE.md` - LangChain実装ガイド

---

*最終更新：2025年12月13日*  
*株式会社エムエムインターナショナル*

