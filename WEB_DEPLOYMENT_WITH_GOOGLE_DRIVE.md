# WEBデプロイガイド - Google Drive連携対応版

株式会社エムエムインターナショナル 社内情報検索AIアプリをStreamlit Community Cloudにデプロイするためのガイドです。

---

## 🎯 デプロイ方式の選択

Google Drive連携を使用する場合、以下の2つの方式があります：

### 方式A: サービスアカウント方式（推奨）✨

**メリット:**
- ✅ WEBアプリで自動認証可能
- ✅ ユーザーのログイン不要
- ✅ Streamlit Community Cloudで完全動作

**デメリット:**
- Google Workspace管理者権限が必要
- 初期設定がやや複雑

### 方式B: OAuth 2.0方式（現在の実装）

**メリット:**
- 既に実装済み
- ユーザー単位の権限管理

**デメリット:**
- WEBアプリでは毎回ログインが必要
- トークンの永続化が困難

---

## 🚀 方式A: サービスアカウント方式でのデプロイ（推奨）

### ステップ1: サービスアカウントの作成

#### 1-1. Google Cloud Consoleでサービスアカウント作成

1. https://console.cloud.google.com/ にアクセス
2. プロジェクトを選択（または作成）
3. 左メニュー「IAMと管理」→「サービスアカウント」
4. 「サービスアカウントを作成」をクリック

**サービスアカウント情報:**
```
サービスアカウント名: 社内情報検索AI
サービスアカウントID: ai-search-service
説明: 社内情報検索AIアプリ用サービスアカウント
```

5. 「作成して続行」をクリック
6. ロール: 「基本」→「閲覧者」を選択
7. 「続行」→「完了」をクリック

#### 1-2. サービスアカウントキーの作成

1. 作成したサービスアカウントをクリック
2. 「キー」タブをクリック
3. 「鍵を追加」→「新しい鍵を作成」
4. キーのタイプ: **JSON**を選択
5. 「作成」をクリック
6. JSONファイルがダウンロードされる

**ダウンロードされたファイル:**
```
プロジェクト名-xxxxx.json
```

#### 1-3. Google Drive APIを有効化

1. 左メニュー「APIとサービス」→「ライブラリ」
2. 「Google Drive API」を検索
3. 「有効にする」をクリック

#### 1-4. サービスアカウントにGoogle Driveへのアクセス権を付与

**方法1: Google Driveで共有（簡単）**

1. Google Driveを開く
2. 共有したいフォルダを右クリック
3. 「共有」をクリック
4. サービスアカウントのメールアドレスを追加
   ```
   ai-search-service@プロジェクト名.iam.gserviceaccount.com
   ```
5. 権限: 「閲覧者」を選択
6. 「送信」をクリック

**方法2: ドメイン全体の委任（Google Workspace管理者のみ）**

1. Google Admin Consoleにアクセス
2. 「セキュリティ」→「APIの制御」
3. 「ドメイン全体の委任」を設定

---

### ステップ2: サービスアカウント用コードの作成

新しいファイルを作成します：

```python
# google_drive_service_account.py
```

このファイルには、サービスアカウント認証を使用したGoogle Drive接続コードが含まれます。

#### 2-1. requirements.txtに追加

```txt
# Google Drive API (Service Account)
google-auth==2.37.0
google-auth-httplib2==0.2.0
google-api-python-client==2.154.0
```

---

### ステップ3: Streamlit Secretsの設定

#### 3-1. ローカルでの設定

`.streamlit/secrets.toml` ファイルを作成：

```toml
# Google API Key (Gemini)
GOOGLE_API_KEY = "your-gemini-api-key-here"

# Google Drive Service Account
[google_drive_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nyour-private-key-here\n-----END PRIVATE KEY-----\n"
client_email = "ai-search-service@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

**重要:** ダウンロードしたJSONファイルの内容をこの形式に変換してください。

#### 3-2. Streamlit Community Cloudでの設定

デプロイ後、以下の手順で設定：

1. Streamlit Community Cloudのダッシュボードにアクセス
2. デプロイしたアプリを選択
3. 「Settings」→「Secrets」をクリック
4. 上記の内容をコピー＆ペースト
5. 「Save」をクリック

---

### ステップ4: GitHubリポジトリの準備

#### 4-1. .gitignoreの確認

以下が含まれていることを確認：

```gitignore
# 認証情報
.streamlit/secrets.toml
google_drive_credentials*.json
google_drive_token*.pickle
*service_account*.json

# 環境変数
.env

# データ
data/
chroma_db/
logs/
```

#### 4-2. GitHubリポジトリの作成

1. https://github.com にアクセス
2. 「New repository」をクリック
3. リポジトリ名: `ai-search-app`
4. プライベートを選択
5. 「Create repository」をクリック

#### 4-3. コードをプッシュ

```bash
git init
git add .
git commit -m "Initial commit: AI search app with Google Drive integration"
git branch -M main
git remote add origin https://github.com/your-username/ai-search-app.git
git push -u origin main
```

---

### ステップ5: Streamlit Community Cloudへのデプロイ

#### 5-1. Streamlit Community Cloudにログイン

1. https://share.streamlit.io/ にアクセス
2. GitHubアカウントでログイン
3. 「New app」をクリック

#### 5-2. アプリの設定

```
Repository: your-username/ai-search-app
Branch: main
Main file path: main.py
App URL: （カスタムURLまたは自動生成）
```

#### 5-3. Advanced settingsの設定

「Advanced settings」をクリック：

**Python version:**
```
3.11
```

**Secrets:**
`.streamlit/secrets.toml` の内容をコピー＆ペースト

#### 5-4. デプロイ

「Deploy」ボタンをクリック

---

## 🔄 方式B: 現在のOAuth 2.0方式でのデプロイ（制限あり）

### 制限事項

- ⚠️ Google Drive機能は使用できません
- ⚠️ ローカルでのみGoogle Drive機能が動作
- ✅ Gemini APIは正常に動作
- ✅ ローカルデータの検索は正常に動作

### デプロイ手順

#### ステップ1: Google Drive機能を無効化

`main.py` に条件分岐を追加：

```python
import os

# Streamlit Cloudかどうかを判定
is_streamlit_cloud = os.getenv('STREAMLIT_CLOUD', 'false') == 'true'

if not is_streamlit_cloud:
    # ローカル環境のみでGoogle Drive機能を有効化
    from google_drive_manager import GoogleDriveManager
    # Google Drive機能の処理
else:
    # Streamlit CloudではGoogle Drive機能をスキップ
    st.info("Google Drive機能はローカル環境でのみ利用可能です")
```

#### ステップ2: 通常のデプロイ手順

1. GitHubリポジトリにプッシュ
2. Streamlit Community Cloudで「New app」
3. Secretsに `GOOGLE_API_KEY` のみ設定
4. デプロイ

---

## 📋 必要なファイル一覧

### 必須ファイル

```
プロジェクトルート/
├── main.py                          # メインアプリ
├── requirements.txt                 # 依存パッケージ
├── .streamlit/
│   └── config.toml                 # Streamlit設定
├── constants.py                     # 定数
├── utils.py                        # ユーティリティ
├── initialize.py                   # 初期化
├── auth.py                         # 認証
├── components.py                   # コンポーネント
├── feedback.py                     # フィードバック
└── README.md                       # 説明
```

### オプション（Google Drive使用時）

```
├── google_drive_service_account.py  # サービスアカウント版
├── google_drive_manager.py          # マネージャー
└── google_drive_security.py         # セキュリティ
```

---

## 🔐 セキュリティ設定

### Streamlit Secretsに設定する内容

```toml
# 必須: Gemini API Key
GOOGLE_API_KEY = "your-gemini-api-key"

# 認証パスワード
[passwords]
admin = "your-admin-password-hash"

# Google Drive Service Account（方式Aの場合）
[google_drive_service_account]
# ... (サービスアカウントのJSON内容)
```

---

## ✅ デプロイ前チェックリスト

### コード

- [ ] `.gitignore` に認証情報を追加済み
- [ ] `requirements.txt` が最新
- [ ] ローカルで正常動作を確認
- [ ] エラーハンドリングを実装

### Google Cloud Console

- [ ] プロジェクトを作成
- [ ] Google Drive APIを有効化
- [ ] サービスアカウントを作成（方式Aの場合）
- [ ] サービスアカウントキーをダウンロード

### GitHub

- [ ] リポジトリを作成（プライベート推奨）
- [ ] コードをプッシュ
- [ ] `.streamlit/secrets.toml` はコミットしない

### Streamlit Community Cloud

- [ ] アカウントを作成
- [ ] GitHubと連携
- [ ] Secretsを設定
- [ ] デプロイ

---

## 🚨 トラブルシューティング

### エラー: ModuleNotFoundError

**原因:** requirements.txtに不足がある

**解決法:**
```bash
pip freeze > requirements.txt
```

### エラー: Google Drive API認証失敗

**原因:** Secretsの設定が間違っている

**解決法:**
1. Streamlit Community Cloudの「Settings」→「Secrets」を確認
2. サービスアカウントJSONの内容が正しいか確認
3. private_keyの改行（\n）が正しく設定されているか確認

### エラー: ファイルが見つからない

**原因:** dataフォルダがGitにプッシュされていない

**解決法:**
- 方法1: dataフォルダをGitに含める
- 方法2: Google Driveから動的に読み込む
- 方法3: 初回起動時にダウンロード

---

## 📞 サポート

- **メール:** ai-support@mm-international.co.jp
- **Streamlit Community Cloud:** https://share.streamlit.io/
- **Streamlit Docs:** https://docs.streamlit.io/

---

*作成日：2025年12月13日*  
*株式会社エムエムインターナショナル*



