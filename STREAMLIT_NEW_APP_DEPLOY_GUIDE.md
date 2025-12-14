# Streamlit Community Cloud 新規アプリデプロイ手順

株式会社エムエムインターナショナル 社内情報検索AIアプリ  
アプリ名: **mmi-ai-manager**

---

## 📋 デプロイ情報

| 項目 | 設定値 |
|------|--------|
| **アプリ名** | mmi-ai-manager |
| **アプリURL** | https://mmi-ai-manager.streamlit.app/ |
| **GitHubリポジトリ** | hinoki-taro/ai-manager-app-1210 |
| **ブランチ** | main |
| **メインファイル** | main.py |
| **Python バージョン** | 3.11 |

---

## 🚀 デプロイ手順

### ステップ1: Streamlit Community Cloudにアクセス

**URL:**
```
https://share.streamlit.io/
```

1. ブラウザで上記URLを開く
2. GitHubアカウント（hinoki-taro）でログイン

---

### ステップ2: 新しいアプリを作成

1. 画面右上の **「New app」** ボタン（＝Create app）をクリック

---

### ステップ3: デプロイ設定を入力

#### Repository *（必須）
```
hinoki-taro/ai-manager-app-1210
```

#### Branch *（必須）
```
main
```

#### Main file path *（必須）
```
main.py
```

#### App URL（カスタムURL）
```
mmi-ai-manager
```
※ これで `https://mmi-ai-manager.streamlit.app/` になります

---

### ステップ4: Advanced settings

1. 画面下部の **「Advanced settings」** をクリック

2. **Python version** を選択:
```
3.11
```

---

### ステップ5: Secrets設定

**「Secrets」** の入力欄に以下をコピー&ペースト:

```toml
GOOGLE_API_KEY = "AIzaSyBlp0GgqOrY5VLVP703PKk-J1UKuDHuhKQ"

[auth]
password = "MMI-SecurePass-2025!"
session_timeout_minutes = 60
max_login_attempts = 5
```

**⚠️ 重要:**
- `GOOGLE_API_KEY`は最初（`[auth]`の前）に記述
- `=`の前後にスペース
- 値を`"`で囲む
- 改行を保持

---

### ステップ6: デプロイ実行

#### デプロイ前チェックリスト

- [ ] Repository: `hinoki-taro/ai-manager-app-1210`
- [ ] Branch: `main`
- [ ] Main file path: `main.py`
- [ ] App URL: `mmi-ai-manager`
- [ ] Python version: `3.11`
- [ ] Secrets: 正しく設定済み

#### 実行

画面右下の **「Deploy!」** ボタンをクリック

---

### ステップ7: デプロイ進行確認

**所要時間:** 約3-5分

**進行状況:**
```
🚀 Deploying your app...
🖥️ Provisioning machine...
🎛️ Preparing system...
📦 Processing dependencies...
```

**確認ポイント:**
- ログに `Using Python 3.11.x` と表示されることを確認

---

### ステップ8: デプロイ完了確認

**成功メッセージ:**
```
✅ Your app is live!
🌐 https://mmi-ai-manager.streamlit.app/
```

**アプリを開く:**
- **「Open app」** ボタンをクリック
- または直接URLにアクセス

---

### ステップ9: 初期化確認

アプリが開くと、デバッグ情報が表示されます:

**正常な場合:**
```
🔄 データを読み込んでいます...

📋 デバッグ情報:
環境変数 GOOGLE_API_KEY: 設定なし
Secrets keys: ['GOOGLE_API_KEY', 'auth']
✓ APIキーを取得しました（先頭10文字: AIzaSyBlp0...）

✓ XX個のドキュメントを読み込みました
✓ テキストの正規化が完了しました
✓ 埋め込みモデルの初期化が完了しました
✓ XX個のチャンクに分割しました
✓ ベクターストアの作成が完了しました

✅ 初期化が正常に完了しました！
```

**初期化時間:** ベクターストア作成で1-2分かかる場合があります

---

### ステップ10: ログインテスト

**ログイン画面が表示されます:**

```
社内情報検索AI
株式会社エムエムインターナショナル

🔐 ログイン

パスワード: [___________________]

[ログイン]
```

**ログイン情報:**
- **パスワード:** `MMI-SecurePass-2025!`

**ログイン後:** AI検索画面が表示される

---

### ステップ11: 動作確認

**テスト質問を試す:**

#### テスト1: 会社情報
```
質問: 会社の事業内容を教えてください
```

**期待される回答:**
- AI清掃ロボットJINNY
- プロパティマネジメント
- 不動産事業

#### テスト2: JINNY
```
質問: JINNYについて詳しく教えてください
```

**期待される回答:**
- 自動走行清掃ロボット
- 1000台以上の導入実績
- 清掃3.0のコンセプト

#### テスト3: 清掃3.0
```
質問: 清掃3.0とは何ですか？
```

**期待される回答:**
- ロボットと人の協働
- データ活用による効率化

---

## 🔗 重要なURL

### アプリ関連

| 項目 | URL |
|------|-----|
| アプリURL | https://mmi-ai-manager.streamlit.app/ |
| Streamlit Cloud | https://share.streamlit.io/ |
| GitHubリポジトリ | https://github.com/hinoki-taro/ai-manager-app-1210 |

### 管理画面

1. https://share.streamlit.io/ にアクセス
2. `mmi-ai-manager` を選択
3. **「Manage app」** をクリック

**管理メニュー:**
- **Analytics** - アクセス統計
- **Logs** - ログ確認
- **Settings** - 設定（Secrets含む）
- **Reboot app** - 再起動
- **Pause app** - 一時停止
- **Delete app** - 削除

---

## ⚙️ Secrets設定（再確認用）

**場所:** Manage app → Settings → Secrets

**設定内容:**

```toml
GOOGLE_API_KEY = "AIzaSyBlp0GgqOrY5VLVP703PKk-J1UKuDHuhKQ"

[auth]
password = "MMI-SecurePass-2025!"
session_timeout_minutes = 60
max_login_attempts = 5
```

**設定変更後:**
1. **「Save」** をクリック
2. **「Reboot app」** をクリック

---

## 🔧 トラブルシューティング

### エラー1: 「App URL already taken」

**症状:**
```
❌ This URL is already taken
```

**対処:**
別のアプリ名を試す:
- `mmi-ai-search`
- `mmi-info-search`
- `mm-international-ai`
- `mmi-ai-manager-v2`

---

### エラー2: 初期化エラー

**症状:**
```
❌ 初期化中にエラーが発生しました
```

**対処:**

#### A. Secretsを確認
1. Manage app → Settings → Secrets
2. 形式が正しいか確認
3. `GOOGLE_API_KEY`が`[auth]`の前にあるか確認
4. 保存して再起動

#### B. ログを確認
1. Manage app → Logs
2. エラーメッセージを確認
3. 具体的なエラー内容に応じて対処

#### C. APIキーを確認
- Google Cloud Consoleで有効か確認
- クォータが残っているか確認

---

### エラー3: Python 3.13を使用してしまう

**症状:**
```
Using Python 3.13.x environment
```

**対処:**
1. リポジトリに `.python-version` ファイルが存在することを確認
2. 内容が `3.11` であることを確認
3. Manage app → Reboot app

---

### エラー4: データが読み込めない

**症状:**
```
❌ 0個のドキュメントを読み込みました
```

**対処:**
1. GitHubリポジトリに `data/` フォルダが存在するか確認
2. `.gitignore` で除外されていないか確認
3. ローカルで確認: `git ls-files data/`

---

### エラー5: ログインできない

**症状:**
- パスワードが正しくありません

**対処:**
1. Secretsの `[auth]` セクションを確認
2. `password = "MMI-SecurePass-2025!"` が正しいか
3. 大文字小文字、記号を確認
4. 保存して再起動

---

## 🔄 アプリの再起動方法

### 方法1: 管理画面から

1. https://share.streamlit.io/ にアクセス
2. `mmi-ai-manager` を選択
3. **「Manage app」** をクリック
4. 左メニューの **「🔄 Reboot app」** をクリック
5. 確認ダイアログで **「Reboot app」** をクリック

### 方法2: 設定変更後の自動再起動

Secrets、リポジトリ（GitHub）の変更後は自動的に再デプロイされます。

---

## 📊 デプロイ後の管理

### アクセス統計の確認

1. Manage app → Analytics
2. 以下の情報を確認:
   - 訪問者数
   - ページビュー
   - アクセス時間帯

### ログの監視

1. Manage app → Logs
2. リアルタイムでログを確認
3. エラーの早期発見

### 定期的なメンテナンス

**推奨:**
- 週1回: ログ確認
- 月1回: パッケージ更新確認
- 必要時: データ更新（GitHubにプッシュ）

---

## 🔐 セキュリティ設定

### 実装済みセキュリティ機能

1. **パスワード認証**
   - 社員全員が共有するパスワード

2. **ログイン試行制限**
   - 10分間に5回まで
   - 超過すると一時的にブロック

3. **セッションタイムアウト**
   - 60分間操作がないと自動ログアウト

4. **アクセスログ**
   - すべてのアクセスを記録

5. **入力サニタイゼーション**
   - SQLインジェクション対策
   - XSS対策

6. **XSRF保護**
   - Streamlit標準機能

### パスワードの変更方法

1. Manage app → Settings → Secrets
2. `[auth]` セクションの `password` を変更
3. **「Save」** → **「Reboot app」**
4. 新しいパスワードを社員に共有（安全な方法で）

---

## 📞 サポート情報

### 内部サポート

- **メール:** ai-support@mm-international.co.jp

### 外部ドキュメント

- **Streamlit Docs:** https://docs.streamlit.io/
- **Streamlit Community:** https://discuss.streamlit.io/
- **LangChain Docs:** https://python.langchain.com/

---

## 📝 関連ドキュメント

プロジェクト内の他のドキュメント:

| ファイル名 | 内容 |
|-----------|------|
| `README.md` | プロジェクト概要 |
| `USER_GUIDE.md` | ユーザー利用ガイド |
| `ADMIN_GUIDE.md` | 管理者ガイド |
| `TROUBLESHOOTING.md` | トラブルシューティング |
| `SECURITY_GUIDE.md` | セキュリティガイド |
| `DEPLOYMENT_GUIDE.md` | デプロイガイド |
| `WEB_DEPLOYMENT_WITH_GOOGLE_DRIVE.md` | Google Drive連携付きデプロイ |
| `STREAMLIT_DEPLOY_STEP_BY_STEP.md` | ステップバイステップガイド |

---

## 🎯 クイックリファレンス

### よく使うコマンド

```bash
# ローカルでの確認
streamlit run main.py

# データフォルダの確認
git ls-files data/

# 最新のコードをプッシュ
git add .
git commit -m "Update: 説明"
git push origin main
```

### よく使うURL

```
アプリURL:
https://mmi-ai-manager.streamlit.app/

管理画面:
https://share.streamlit.io/

GitHubリポジトリ:
https://github.com/hinoki-taro/ai-manager-app-1210
```

---

## ✅ デプロイ完了チェックリスト

### 初回デプロイ時

- [ ] Streamlit Cloudにログイン
- [ ] New app をクリック
- [ ] リポジトリ情報を入力
  - [ ] Repository: `hinoki-taro/ai-manager-app-1210`
  - [ ] Branch: `main`
  - [ ] Main file path: `main.py`
  - [ ] App URL: `mmi-ai-manager`
- [ ] Advanced settings を設定
  - [ ] Python version: `3.11`
- [ ] Secrets を設定
  - [ ] GOOGLE_API_KEY
  - [ ] [auth] セクション
- [ ] Deploy! をクリック
- [ ] デプロイ完了を確認（3-5分）
- [ ] アプリにアクセス
- [ ] デバッグ情報を確認
- [ ] ログインテスト
- [ ] 動作テスト（3つの質問）
- [ ] URLを社員に共有
- [ ] パスワードを共有（安全な方法で）

### 設定変更時

- [ ] Manage app → Settings → Secrets
- [ ] 内容を編集
- [ ] Save をクリック
- [ ] Reboot app をクリック
- [ ] 動作確認

---

## 📅 作成情報

- **作成日:** 2025年12月13日
- **最終更新:** 2025年12月13日
- **対象:** 株式会社エムエムインターナショナル
- **アプリ名:** mmi-ai-manager
- **バージョン:** 1.0

---

*このドキュメントは、Streamlit Community Cloudでの新規アプリデプロイの完全な手順書です。*

