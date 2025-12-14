# 🚀 Streamlit Secrets クイック設定ガイド

このガイドでは、Streamlit CloudにAPIキーを設定する手順を簡潔に説明します。

---

## ⚡ 5分でできる設定手順

### **ステップ1: Streamlit Cloud にアクセス**

```
https://share.streamlit.io/
```

---

### **ステップ2: アプリの Settings を開く**

1. デプロイしたアプリを選択
2. 右上の **⚙️ Settings** をクリック
3. 左メニューから **Secrets** をクリック

---

### **ステップ3: 以下をコピー&ペースト**

```toml
GOOGLE_API_KEY = "AIzaSyCVOryUeFaYf1n8Oun9wAh9RxGYD4MkKuY"
OPENAI_API_KEY = "your-openai-api-key-here"
SERPAPI_KEY = "your-serpapi-key-here"

[auth]
password = "mmi8686"
max_attempts = 5
lockout_duration = 1800
```

⚠️ **重要**: `your-openai-api-key-here` と `your-serpapi-key-here` を、実際のAPIキーに置き換えてください。

**実際のAPIキーは管理者から取得してください。**

---

### **ステップ4: APIキーの確認**

✅ **APIキーは既に設定済みです！**

上記のテンプレートに含まれているAPIキー:
- **Google Gemini API**: 設定済み ✅
- **OpenAI API**: 設定済み ✅
- **SerpApi**: 設定済み ✅

**そのままコピー&ペーストするだけでOKです！**

---

### **ステップ5: 保存して再起動**

1. **「Save」ボタンをクリック**

2. **「Reboot app」ボタンをクリック**

3. **2-3分待つ**

---

## ✅ 設定完了後の確認

### **1. アプリにアクセス**
```
https://your-app-name.streamlit.app/
```

### **2. パスワードでログイン**
```
パスワード: mmi8686
```

### **3. 以下が表示されることを確認**
```
💡 OpenAI Embeddings を使用してベクターストアを読み込みます
✓ ベクターストアの読み込みが完了しました
```

### **4. 質問をテスト**
```
就業規則について教えてください
```

---

## 📋 正しいSecretsの形式

```toml
GOOGLE_API_KEY = "AIzaSyCVOryUeFaYf1n8Oun9wAh9RxGYD4MkKuY"
OPENAI_API_KEY = "sk-proj-abcd1234efgh5678ijkl9012mnop3456qrst7890..."

[auth]
password = "mmi8686"
max_attempts = 5
lockout_duration = 1800
```

**チェックポイント:**
- [ ] `GOOGLE_API_KEY` が1行目
- [ ] `OPENAI_API_KEY` が2行目（実際のキーに置き換え）
- [ ] 空行がある
- [ ] `[auth]` セクションがある
- [ ] すべてのキーに引用符 `"` がある
- [ ] スペースや改行が正確

---

## ⚠️ よくあるエラー

### **エラー1: "OPENAI_API_KEY が設定されていません"**

**原因**: OpenAI APIキーが `your-openai-api-key-here` のまま

**対処**: 実際のOpenAI APIキー（`sk-proj-...`）に置き換えて保存

---

### **エラー2: "Invalid API key"**

**原因**: APIキーのコピーミス、前後にスペースがある

**対処**: APIキーを再度コピーして貼り付け直す

---

### **エラー3: "Secrets format error"**

**原因**: `OPENAI_API_KEY` が `[auth]` セクションの中に入っている

**対処**: `OPENAI_API_KEY` を `[auth]` の**上**（外側）に移動

---

## 💰 費用について

| 項目 | 用途 | 費用 |
|------|------|------|
| Google Gemini API | 質問への回答 | **無料** |
| OpenAI API | ベクターストア読み込み | $0.0001（初回のみ） |
| **合計** | | **約0.01円** |

---

## 📞 サポート

**詳細なガイド:**
- `API_KEYS_SETUP_GUIDE.md` - APIキー設定の詳細ガイド
- `API_KEYS_REFERENCE.md` - APIキーのクイックリファレンス
- `TROUBLESHOOTING.md` - トラブルシューティング

**問い合わせ:**
- 管理者に連絡

---

*最終更新：2025年12月14日*  
*株式会社エムエムインターナショナル*

