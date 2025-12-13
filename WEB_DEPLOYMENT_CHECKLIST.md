# ✅ WEB公開 最終チェックリスト

## 🚀 公開準備状況

このチェックリストを使って、WEB公開の準備が整っているか確認してください。

---

## ステップ1: セキュリティ確認 🔒

### 機密情報の保護

- [ ] `.gitignore` に以下が含まれている:
  - [ ] `.env`
  - [ ] `.streamlit/secrets.toml`
  - [ ] `data/`
  - [ ] `logs/`

- [ ] 以下のファイルが作成されている:
  - [ ] `env_template.txt`（APIキーなし）
  - [ ] `.streamlit/secrets.toml.template`（APIキーなし）

- [ ] コード内にAPIキーが直接記述されていない

**確認コマンド**:
```bash
# 機密情報がGitに含まれていないか確認
git status
git log --all --oneline -- .env
git log --all --oneline -- data/
```

---

## ステップ2: ファイル構成確認 📁

### 必須ファイルの存在確認

- [ ] `main.py` ✅
- [ ] `auth.py` ✅（NEW: 認証機能）
- [ ] `initialize.py` ✅
- [ ] `utils.py` ✅
- [ ] `constants.py` ✅
- [ ] `components.py` ✅
- [ ] `requirements.txt` ✅
- [ ] `.gitignore` ✅
- [ ] `.streamlit/config.toml` ✅
- [ ] `.streamlit/secrets.toml.template` ✅

### ドキュメントの確認

- [ ] `DEPLOYMENT_GUIDE.md` ✅（詳細デプロイ手順）
- [ ] `SECURITY_CHECKLIST.md` ✅（セキュリティ確認）
- [ ] `README_WEB_DEPLOYMENT.md` ✅（公開版README）
- [ ] `明日の朝の起動手順.txt` ✅（ローカル起動手順）

---

## ステップ3: コード確認 💻

### Google Gemini API 設定

- [ ] `initialize.py` が `GoogleGenerativeAIEmbeddings` を使用 ✅
- [ ] `utils.py` が `ChatGoogleGenerativeAI` を使用 ✅
- [ ] `constants.py` で `MODEL = "gemini-1.5-flash"` ✅

### 認証機能の統合

- [ ] `main.py` に `import auth` が追加されている ✅
- [ ] `main.py` の初期化前に `auth.check_password()` を呼び出している ✅
- [ ] `auth.add_logout_button()` でログアウトボタンを表示 ✅

**確認方法**:
```python
# main.py の該当箇所を確認
# ############################################################
# # 3. 認証チェック
# ############################################################
# if not auth.check_password():
#     st.stop()
```

---

## ステップ4: ローカル動作確認 🖥️

### 起動テスト

```bash
# 1. 環境変数を設定
copy env_template.txt .env
# .env にAPIキーを記入

# 2. アプリを起動
streamlit run main.py

# 3. ブラウザで http://localhost:8501 にアクセス
```

### 機能テスト

- [ ] アプリが正常に起動する
- [ ] 認証画面が表示される（パスワード設定時）
- [ ] ログイン後、メイン画面が表示される
- [ ] 「社内文書検索」モードで検索できる
- [ ] 「社内問い合わせ」モードで質問できる
- [ ] ログアウトボタンが機能する

---

## ステップ5: GitHub準備 🐙

### リポジトリ作成

```bash
# 1. GitHubで新しいリポジトリを作成
#    - Repository name: internal-ai-search-app
#    - Visibility: Private ⚠️ 必ずPrivateを選択

# 2. ローカルでGit初期化
cd "C:\Users\mtokyo081\Desktop\cursor\社内情報特化型生成AI検索アプリ"
git init
git add .
git commit -m "Initial commit: Internal AI Search App"

# 3. GitHubにプッシュ
git remote add origin https://github.com/あなたのユーザー名/internal-ai-search-app.git
git branch -M main
git push -u origin main
```

### リポジトリ設定

- [ ] リポジトリが **Private** に設定されている ⚠️
- [ ] README.md が適切に表示される
- [ ] `.gitignore` が機能している（`data/`, `.env` が除外されている）

---

## ステップ6: Streamlit Cloud デプロイ ☁️

### デプロイ手順

1. **Streamlit Cloudにアクセス**
   - https://share.streamlit.io/
   - GitHubアカウントでログイン

2. **新しいアプリを作成**
   - [ ] 「New app」をクリック
   - [ ] リポジトリを選択: `あなたのユーザー名/internal-ai-search-app`
   - [ ] Branch: `main`
   - [ ] Main file path: `main.py`
   - [ ] 「Deploy!」をクリック

3. **Secrets を設定**
   - [ ] Settings → Secrets に移動
   - [ ] 以下をコピー＆ペースト:
     ```toml
     GOOGLE_API_KEY = "AIzaSyBlp0GgqOrY5VLVP703PKk-J1UKuDHuhKQ"
     
     # パスワード認証を有効にする場合（オプション）
     [auth]
     password = "your_secure_password_here"
     ```
   - [ ] 「Save」をクリック

4. **アクセス制限を設定**（推奨）
   - [ ] Settings → Sharing
   - [ ] 社内ドメイン制限 or 招待制を設定

---

## ステップ7: 本番環境テスト 🧪

### デプロイ後の確認

- [ ] アプリが正常に起動する
- [ ] APIキーが正しく読み込まれている
- [ ] 認証機能が動作する（設定している場合）
- [ ] データファイルが読み込まれる（配置している場合）
- [ ] 質問に対して正しい回答が返される

### エラー対応

エラーが出た場合：

1. **ログを確認**
   - Streamlit Cloud → Settings → Logs

2. **よくあるエラー**
   - `GOOGLE_API_KEY not found`: Secrets を再確認
   - `ModuleNotFoundError`: requirements.txt を確認
   - `初期化処理に失敗`: データファイルを確認

---

## ステップ8: アクセス制御 🔐

### オプションA: Streamlit Cloud のドメイン制限

```
Settings → Sharing
→ Restrict to specific email domains
→ @mm-international.co.jp を追加
```

### オプションB: パスワード認証

```toml
# Secrets に追加
[auth]
password = "YourSecurePassword123!"
```

### オプションC: 招待制

```
Settings → Sharing
→ Invite viewers
→ 社員のメールアドレスを追加
```

**推奨**: **オプションA + オプションB** の組み合わせ

---

## ステップ9: 社内共有 📢

### 共有情報の準備

- [ ] アプリのURL: `https://internal-ai-search-app.streamlit.app`
- [ ] アクセス方法の説明
- [ ] パスワード（認証を使用している場合）
- [ ] 使い方ガイド

### 共有テンプレート

```
件名: 【新サービス】社内AI検索アプリをリリースしました

皆様

社内情報を簡単に検索できるAIアプリをリリースしました。

■ アクセス方法
URL: https://internal-ai-search-app.streamlit.app
パスワード: [ここにパスワード]

■ 主な機能
- 社内文書の検索
- AIによる質問応答
- 情報源の明示

■ 使い方
詳細は以下のガイドをご覧ください：
[README_WEB_DEPLOYMENT.md のリンク]

■ 注意事項
- 社内専用のため、URLを外部に共有しないでください
- 1日の質問回数に制限があります（約750回/日）

ご質問は #ai-search-support までお願いします。
```

---

## ステップ10: 運用準備 🔧

### モニタリング設定

- [ ] Google AI Studio で使用量を定期確認
  - https://aistudio.google.com/app/apikey
- [ ] Streamlit Cloud のログを定期確認
- [ ] 異常なアクセスがないか監視

### 保守計画

- [ ] 月1回: アクセスログ確認
- [ ] 月1回: パスワード変更（認証使用時）
- [ ] 四半期1回: データファイル更新
- [ ] 四半期1回: 依存パッケージの更新確認

---

## 🎯 最終チェック

すべての項目にチェックが入ったら、公開準備完了です！

### 公開前の最終確認

- [ ] **セキュリティ**: 機密情報が含まれていない
- [ ] **動作**: ローカルとStreamlit Cloudで正常動作
- [ ] **アクセス制御**: 社内限定の設定が完了
- [ ] **ドキュメント**: 必要な資料がすべて揃っている
- [ ] **サポート**: 問い合わせ先を決定

---

## 📊 公開状況サマリー

| 項目 | ステータス |
|-----|-----------|
| コード準備 | ✅ 完了 |
| セキュリティ対策 | ✅ 実装済み |
| 認証機能 | ✅ 実装済み |
| ドキュメント | ✅ 作成済み |
| ローカル動作確認 | ⏳ 要確認 |
| GitHubプッシュ | ⏳ 要実施 |
| Streamlit Cloudデプロイ | ⏳ 要実施 |
| 本番環境テスト | ⏳ 要実施 |

---

## 🎉 公開完了後

公開が完了したら：

1. ✅ 社内メンバーに共有
2. ✅ フィードバックを収集
3. ✅ 使用状況をモニタリング
4. ✅ 定期的にメンテナンス

**お疲れ様でした！🚀**

---

## 📞 サポート

問題が発生した場合：

1. `DEPLOYMENT_GUIDE.md` のトラブルシューティングを確認
2. `SECURITY_CHECKLIST.md` で設定を再確認
3. GitHubのIssuesで質問
4. Streamlit公式ドキュメントを参照

---

**確認日**: ________________  
**確認者**: ________________  
**公開承認**: ________________  

