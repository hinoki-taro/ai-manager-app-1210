# 🔑 APIキー設定ガイド

このガイドでは、アプリで使用するAPIキーの設定方法を説明します。

---

## 📋 必要なAPIキー

### **1. Google Gemini API キー**（必須）

**用途:**
- ✅ LLM（質問への回答生成）- 完全無料
- ✅ ベクターストア作成（オプション、Google Embeddings使用時）

**取得方法:**
1. Google AI Studio にアクセス:
   ```
   https://aistudio.google.com/app/apikey
   ```

2. **「Create API key」をクリック**

3. APIキーをコピー（例: `AIzaSy...`）

**無料枠:**
- 月間1,500リクエスト
- 質問回答は完全無料で使用可能

---

### **2. OpenAI API キー**（オプション）

**用途:**
- ✅ ベクターストア作成（OpenAI Embeddings使用時）
- ⚠️ 既に作成済みのベクターストアを読み込む場合に必要

**取得方法:**
1. OpenAI Platform にアクセス:
   ```
   https://platform.openai.com/api-keys
   ```

2. **アカウント作成**（まだの場合）
   - Googleアカウントで簡単登録可能
   - 支払い方法の設定が必要（クレジットカード）

3. **「Create new secret key」をクリック**

4. 名前を入力（例: `streamlit-app`）

5. APIキーをコピー（例: `sk-proj-...`）

**費用:**
- ベクターストア読み込み: 約$0.0001（0.01円）/回
- 初回のみ課金、その後は無料

---

## 🔧 ローカル環境でのAPIキー設定

### **方法1: `.env` ファイルを使用（推奨）**

1. **`.env` ファイルを開く**（プロジェクトルートにあります）

2. **以下の内容を確認/編集**:

```env
# Google Gemini API キー（必須）
GOOGLE_API_KEY=AIzaSyCVOryUeFaYf1n8Oun9wAh9RxGYD4MkKuY

# OpenAI API キー（オプション、ベクターストア読み込みに必要）
OPENAI_API_KEY=sk-proj-ここにあなたのAPIキーを貼り付け
```

3. **保存**

⚠️ **重要**: `.env` ファイルはGitHubにプッシュされません（機密情報保護のため）

---

## 🌐 Streamlit Cloud でのAPIキー設定

### **Settings → Secrets に設定**

1. **Streamlit Cloud にアクセス**:
   ```
   https://share.streamlit.io/
   ```

2. **デプロイしたアプリを選択**

3. **Settings（⚙️）→ Secrets をクリック**

4. **以下をコピー&ペースト**:

```toml
GOOGLE_API_KEY = "AIzaSyCVOryUeFaYf1n8Oun9wAh9RxGYD4MkKuY"
OPENAI_API_KEY = "your-openai-api-key-here"
SERPAPI_KEY = "your-serpapi-key-here"

[auth]
password = "mmi8686"
max_attempts = 5
lockout_duration = 1800
```

⚠️ **重要**: `your-openai-api-key-here` と `your-serpapi-key-here` を実際のAPIキーに置き換えてください。

⚠️ **チェックポイント**:
- [ ] `GOOGLE_API_KEY` が1行目
- [ ] `OPENAI_API_KEY` が2行目（実際のキーに置き換え）
- [ ] 空行がある
- [ ] `[auth]` セクションがある
- [ ] 引用符 `"` が正しく使われている

5. **「Save」をクリック**

6. **「Reboot app」で再起動**

---

## 📊 APIキーの使用状況

### **Google Gemini API**

**確認方法:**
```
https://aistudio.google.com/app/apikey
```

**使用量:**
- 質問への回答: 無料（月間1,500リクエスト）
- 埋め込み生成: 無料（月間1,500リクエスト）

---

### **OpenAI API**

**確認方法:**
```
https://platform.openai.com/usage
```

**使用量:**
- ベクターストア読み込み: 約$0.0001/回（初回のみ）

---

## 🔒 セキュリティのベストプラクティス

### **やるべきこと:**
- ✅ `.env` ファイルは `.gitignore` に含める（既に設定済み）
- ✅ APIキーを他人と共有しない
- ✅ 定期的にAPIキーをローテーション（3-6ヶ月ごと）
- ✅ 使用量を定期的に確認

### **やってはいけないこと:**
- ❌ APIキーをソースコードに直接書かない
- ❌ APIキーをGitHubにプッシュしない
- ❌ APIキーをメールやチャットで送信しない
- ❌ スクリーンショットにAPIキーを含めない

---

## 🆘 トラブルシューティング

### **エラー: "GOOGLE_API_KEY が設定されていません"**

**原因**: APIキーが正しく読み込まれていない

**対処法:**
1. `.env` ファイルが存在するか確認
2. `GOOGLE_API_KEY=` の後にスペースがないか確認
3. アプリを再起動

---

### **エラー: "Invalid API key"**

**原因**: APIキーが間違っている、または無効

**対処法:**
1. APIキーをコピーし直す
2. 前後にスペースがないか確認
3. 新しいAPIキーを作成

---

### **エラー: "API quota exceeded"**

**原因**: APIの使用量制限に達した

**対処法:**
1. **Google Gemini**: 翌日まで待つ（24時間でリセット）
2. **OpenAI**: 使用量ページで確認、必要に応じて課金

---

## 📞 サポート

**質問がある場合:**
- このガイドを参照
- `TROUBLESHOOTING.md` を確認
- 管理者に問い合わせ

---

*最終更新：2025年12月14日*  
*株式会社エムエムインターナショナル*

