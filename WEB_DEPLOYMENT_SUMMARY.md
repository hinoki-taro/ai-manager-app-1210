# WEBデプロイ完了報告

株式会社エムエムインターナショナル 社内情報検索AIアプリのWEBデプロイ準備が完了しました！

---

## ✅ 作成されたファイル

### デプロイ関連（4個）

1. ✅ **`WEB_DEPLOYMENT_WITH_GOOGLE_DRIVE.md`** - 完全デプロイガイド
2. ✅ **`google_drive_service_account.py`** - サービスアカウント連携モジュール
3. ✅ **`deploy_streamlit.bat`** - デプロイ準備スクリプト
4. ✅ **`WEB_DEPLOYMENT_SUMMARY.md`** - この報告書

### 更新ファイル

5. ✅ **`.streamlit/secrets.toml.template`** - サービスアカウント設定を追加

---

## 🎯 デプロイ方式

### 推奨: サービスアカウント方式 ✨

**メリット:**
- ✅ WEBアプリで自動認証
- ✅ ユーザーログイン不要
- ✅ Streamlit Community Cloudで完全動作

**必要なもの:**
- Google Cloud Consoleアカウント
- サービスアカウントキー（JSON）
- Gemini API Key

---

## 🚀 デプロイ手順（5ステップ）

### ステップ1: Google Cloud Console設定

#### サービスアカウントの作成

```
1. https://console.cloud.google.com/ にアクセス
2. プロジェクトを選択（または作成）
3. 「IAMと管理」→「サービスアカウント」
4. 「サービスアカウントを作成」をクリック

サービスアカウント名: 社内情報検索AI
サービスアカウントID: ai-search-service

5. キーを作成（JSON形式）
6. JSONファイルをダウンロード
```

#### Google Drive APIを有効化

```
1. 「APIとサービス」→「ライブラリ」
2. 「Google Drive API」を検索
3. 「有効にする」をクリック
```

#### フォルダを共有

```
1. Google Driveで共有したいフォルダを開く
2. 「共有」をクリック
3. サービスアカウントのメールアドレスを追加:
   ai-search-service@プロジェクト名.iam.gserviceaccount.com
4. 権限: 「閲覧者」を選択
5. 「送信」をクリック
```

---

### ステップ2: GitHubリポジトリの準備

#### デプロイスクリプトを実行

```bash
deploy_streamlit.bat
```

**メニュー:**
1. デプロイ前チェック
2. GitHubリポジトリの初期化
3. コードをGitHubにプッシュ

#### または手動で実行

```bash
# リポジトリ初期化
git init
git branch -M main

# GitHubでリポジトリを作成してURLを取得
git remote add origin https://github.com/your-username/ai-search-app.git

# コミット＆プッシュ
git add .
git commit -m "Initial commit: AI search app with Google Drive"
git push -u origin main
```

---

### ステップ3: Streamlit Community Cloudへデプロイ

#### 3-1. Streamlit Community Cloudにアクセス

```
https://share.streamlit.io/
```

GitHubアカウントでログイン

#### 3-2. New appをクリック

```
Repository: your-username/ai-search-app
Branch: main
Main file path: main.py
App URL: （カスタムまたは自動生成）
```

#### 3-3. Advanced settings

「Advanced settings」をクリック

**Python version:**
```
3.11
```

---

### ステップ4: Secretsの設定 ⚙️

「Advanced settings」→「Secrets」で以下を設定：

#### 必須: Gemini API Key

```toml
GOOGLE_API_KEY = "your-gemini-api-key-here"
```

#### 必須: 認証パスワード

```toml
[auth]
password = "your-secure-password"
session_timeout_minutes = 60
max_login_attempts = 5
```

#### オプション: Google Drive Service Account

サービスアカウントキー（JSON）の内容を貼り付け：

```toml
[google_drive_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_KEY\n-----END PRIVATE KEY-----\n"
client_email = "ai-search-service@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

---

### ステップ5: デプロイ実行 🚀

「Deploy!」ボタンをクリック

**デプロイ時間:** 約3-5分

---

## ✅ デプロイ後の確認

### アプリにアクセス

```
https://your-app-name.streamlit.app/
```

### 動作確認

1. ✅ ログイン画面が表示される
2. ✅ パスワードでログイン
3. ✅ AI検索が正常に動作
4. ✅ Google Drive連携が動作（設定した場合）

---

## 📊 デプロイ構成

### ファイル構成

```
GitHubリポジトリ/
├── main.py                          # メインアプリ
├── requirements.txt                 # 依存パッケージ
├── .streamlit/
│   ├── config.toml                 # Streamlit設定
│   └── secrets.toml.template       # Secrets設定例
├── constants.py
├── utils.py
├── initialize.py
├── auth.py
├── components.py
├── feedback.py
├── google_drive_service_account.py  # サービスアカウント版
└── README.md
```

### Streamlit Community Cloud設定

```
環境変数（Secrets）:
├── GOOGLE_API_KEY                  # Gemini API
├── [auth]                          # 認証設定
└── [google_drive_service_account] # Google Drive（オプション）
```

---

## 🔐 セキュリティ

### 実装済みセキュリティ機能

1. ✅ パスワード認証
2. ✅ ログイン試行回数制限
3. ✅ セッションタイムアウト
4. ✅ IPアドレス制限（オプション）
5. ✅ アクセスログ記録
6. ✅ 入力サニタイゼーション
7. ✅ XSRF保護
8. ✅ Google Drive読み取り専用アクセス

### ベストプラクティス

- ✅ 認証情報は`.gitignore`で除外
- ✅ GitHubリポジトリはプライベート推奨
- ✅ Streamlit Secretsで認証情報を管理
- ✅ サービスアカウントは読み取り専用権限

---

## 🎯 Google Drive連携の選択肢

### オプション1: サービスアカウント方式（推奨）

**使用するファイル:**
- `google_drive_service_account.py`

**メリット:**
- WEBで完全動作
- ユーザーログイン不要

**設定が必要:**
- Google Cloud Consoleでサービスアカウント作成
- Streamlit Secretsに設定

### オプション2: Google Drive機能を無効化

**メリット:**
- 設定が簡単
- Gemini APIのみ使用

**制限:**
- Google Drive連携は使用不可
- ローカルデータのみ検索

**コード:**
```python
# main.pyで条件分岐
if "google_drive_service_account" in st.secrets:
    # Google Drive機能を有効化
    from google_drive_service_account import GoogleDriveServiceAccount
else:
    # Google Drive機能をスキップ
    st.info("Google Drive機能はオプションです")
```

---

## 📖 詳細ドキュメント

### デプロイ関連

1. **`WEB_DEPLOYMENT_WITH_GOOGLE_DRIVE.md`**
   - 完全なデプロイガイド
   - サービスアカウント設定手順
   - トラブルシューティング

2. **`setup_google_cloud_console.md`**
   - Google Cloud Console設定手順
   - 認証情報作成方法

3. **`DEPLOYMENT_GUIDE.md`**
   - 基本的なデプロイ手順
   - Streamlit Community Cloud設定

### Google Drive関連

4. **`GOOGLE_DRIVE_SETUP.md`**
   - Google Drive連携の基本
5. **`GOOGLE_DRIVE_ACCOUNT_SETUP.md`**
   - アカウント指定設定
6. **`GOOGLE_DRIVE_SECURITY_GUIDE.md`**
   - セキュリティガイド

---

## 🔧 トラブルシューティング

### エラー: ModuleNotFoundError

**原因:** requirements.txtに不足がある

**解決法:**
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements.txt"
git push
```

### エラー: Google Drive認証失敗

**原因:** Secretsの設定が間違っている

**解決法:**
1. Streamlit Community Cloud → Settings → Secrets
2. サービスアカウントJSONの内容を再確認
3. private_keyの改行（\n）が正しいか確認
4. アプリを再起動

### エラー: データが見つからない

**原因:** dataフォルダがGitにプッシュされていない

**解決法:**

**方法1: dataフォルダをGitに含める**
```bash
# .gitignoreから除外
# data/ の行をコメントアウトまたは削除
git add data/
git commit -m "Add data folder"
git push
```

**方法2: Google Driveから読み込む**
- サービスアカウントを設定
- Google Driveにデータをアップロード
- アプリ起動時に自動ダウンロード

---

## ✅ チェックリスト

デプロイ完了確認：

- [ ] Google Cloud Consoleでサービスアカウント作成
- [ ] サービスアカウントキー（JSON）をダウンロード
- [ ] Google Drive APIを有効化
- [ ] Google Driveでフォルダを共有
- [ ] GitHubリポジトリを作成（プライベート推奨）
- [ ] コードをGitHubにプッシュ
- [ ] Streamlit Community Cloudにログイン
- [ ] New appでデプロイ設定
- [ ] Secretsに認証情報を設定
  - [ ] GOOGLE_API_KEY
  - [ ] [auth] password
  - [ ] [google_drive_service_account]（オプション）
- [ ] Deploy実行
- [ ] アプリにアクセスして動作確認
- [ ] ログイン機能の確認
- [ ] AI検索機能の確認
- [ ] Google Drive機能の確認（設定した場合）

---

## 📞 サポート

- **メール:** ai-support@mm-international.co.jp
- **デプロイスクリプト:** `deploy_streamlit.bat`
- **詳細ガイド:** `WEB_DEPLOYMENT_WITH_GOOGLE_DRIVE.md`
- **Streamlit Docs:** https://docs.streamlit.io/

---

## 🎉 まとめ

✅ **WEBデプロイの準備が完了**  
✅ **Google Drive連携対応**  
✅ **サービスアカウント方式実装**  
✅ **デプロイスクリプト提供**  
✅ **詳細ドキュメント完備**  

これで、Streamlit Community Cloudへのデプロイが可能になりました！

---

*作成日：2025年12月13日*  
*株式会社エムエムインターナショナル*



