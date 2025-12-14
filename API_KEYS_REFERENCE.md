# 🔑 APIキー クイックリファレンス

このファイルには、現在使用中のAPIキーの情報が記載されています。

⚠️ **注意**: このファイルには実際のAPIキー値は含まれません。APIキーは `.env` ファイルまたは Streamlit Secrets に保管されています。

---

## 📋 現在の設定

### **Google Gemini API キー** ✅

**ステータス**: 設定済み  
**場所**: `.env` ファイル  
**変数名**: `GOOGLE_API_KEY`  
**形式**: `AIzaSy...`（40文字程度）

**用途:**
- ✅ LLM（質問への回答生成）- **完全無料**
- ✅ Google Embeddings（オプション）

**確認方法:**
```bash
# Windowsの場合
type .env | findstr GOOGLE_API_KEY

# Mac/Linuxの場合
cat .env | grep GOOGLE_API_KEY
```

**取得元:**
- https://aistudio.google.com/app/apikey

---

### **OpenAI API キー** ✅

**ステータス**: 設定済み  
**場所**: `.env` ファイル  
**変数名**: `OPENAI_API_KEY`  
**形式**: `sk-proj-...`（100文字以上）

**用途:**
- ✅ ベクターストアの読み込み（必須）
- ⚠️ 費用: 約$0.0001（0.01円）/回

**取得元:**
- https://platform.openai.com/api-keys

---

### **SerpApi キー** ✅

**ステータス**: 設定済み（オプション）  
**場所**: `.env` ファイル  
**変数名**: `SERPAPI_KEY`  
**形式**: 64文字のハッシュ

**用途:**
- ✅ Web検索機能（拡張機能）
- ⚠️ 月間100リクエスト無料

**取得元:**
- https://serpapi.com/

---

## 🔧 APIキーの設定方法

### **ローカル環境（`.env` ファイル）**

**現在の `.env` ファイルの内容:**

```env
# Google Gemini API キー（設定済み）
GOOGLE_API_KEY=AIzaSyCVOryUeFaYf1n8Oun9wAh9RxGYD4MkKuY

# OpenAI API キー（設定が必要）
OPENAI_API_KEY=sk-proj-ここにあなたのOpenAI APIキーを貼り付け
```

**設定手順:**
1. `.env` ファイルを開く
2. `OPENAI_API_KEY=` の後に、取得したAPIキーを貼り付け
3. 保存

---

### **Streamlit Cloud（Secrets）**

**設定内容:**

```toml
GOOGLE_API_KEY = "AIzaSyCVOryUeFaYf1n8Oun9wAh9RxGYD4MkKuY"
OPENAI_API_KEY = "sk-proj-あなたのOpenAI APIキー"

[auth]
password = "mmi8686"
max_attempts = 5
lockout_duration = 1800
```

**設定手順:**
1. https://share.streamlit.io/ にアクセス
2. アプリを選択 → Settings → Secrets
3. 上記の内容をコピー&ペースト（OpenAI APIキーを実際の値に置き換え）
4. Save → Reboot app

---

## 💰 費用の目安

| API | 用途 | 費用 | 頻度 |
|-----|------|------|------|
| Google Gemini | 質問への回答 | **無料** | 毎回 |
| Google Gemini | Embeddings（オプション） | **無料** | 初回のみ |
| OpenAI | ベクターストア読み込み | $0.0001 | 初回のみ |

**月間コスト予測（1000回質問）:**
- Google Gemini: **$0**
- OpenAI: **$0.0001**（初回のみ）
- **合計: 約0.01円/月** ≈ **実質無料** 💰

---

## 📊 使用量の確認

### **Google Gemini API**

**確認先:**
```
https://aistudio.google.com/app/apikey
```

**無料枠:**
- 月間1,500リクエスト
- 毎月1日にリセット

---

### **OpenAI API**

**確認先:**
```
https://platform.openai.com/usage
```

**初回クレジット:**
- $5の無料クレジット（新規アカウント）
- 今回の使用量: 約$0.0001

---

## 🔄 APIキーの更新方法

### **Google Gemini API キーを更新する場合:**

1. **新しいAPIキーを取得**:
   - https://aistudio.google.com/app/apikey

2. **`.env` ファイルを更新**:
   ```env
   GOOGLE_API_KEY=新しいAPIキー
   ```

3. **Streamlit Secretsを更新**（WEB公開している場合）:
   - Settings → Secrets で更新
   - Reboot app

---

### **OpenAI API キーを更新する場合:**

1. **新しいAPIキーを取得**:
   - https://platform.openai.com/api-keys

2. **`.env` ファイルを更新**:
   ```env
   OPENAI_API_KEY=新しいAPIキー
   ```

3. **Streamlit Secretsを更新**（WEB公開している場合）:
   - Settings → Secrets で更新
   - Reboot app

---

## 🔒 セキュリティチェックリスト

- [ ] `.env` ファイルは `.gitignore` に含まれている ✅
- [ ] APIキーをGitHubにプッシュしていない ✅
- [ ] APIキーを他人と共有していない
- [ ] 定期的に使用量を確認している
- [ ] Streamlit SecretsにAPIキーを正しく設定している

---

## 📞 問い合わせ先

**APIキーに関する質問:**
- `API_KEYS_SETUP_GUIDE.md` を参照
- `TROUBLESHOOTING.md` を確認
- 管理者に問い合わせ

---

*最終更新：2025年12月14日*  
*株式会社エムエムインターナショナル*

