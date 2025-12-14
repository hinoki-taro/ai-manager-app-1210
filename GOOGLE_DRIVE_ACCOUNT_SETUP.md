# 特定Googleアカウントでの連携セットアップ

株式会社エムエムインターナショナル 社内情報検索AIアプリで、**特定のGoogleアカウント**を指定してGoogle Driveを参照する方法を説明します。

---

## 📋 概要

### できること

1. ✅ **特定のGoogleアカウントを指定**
2. ✅ **複数のGoogleアカウントを管理**
3. ✅ **アカウントごとに異なるフォルダを参照**
4. ✅ **アカウントの切り替え**
5. ✅ **共有ドライブ（Shared Drives）の参照**

---

## 🎯 ユースケース

### ケース1: 社内共有アカウント

```
アカウント: shared-docs@mm-international.co.jp
用途: 全社員が参照できる社内文書
```

### ケース2: 部門別アカウント

```
アカウント1: sales@mm-international.co.jp
→ 営業資料フォルダ

アカウント2: hr@mm-international.co.jp
→ 人事資料フォルダ

アカウント3: tech@mm-international.co.jp
→ 技術資料フォルダ
```

### ケース3: 個人アカウント

```
アカウント: yamada@mm-international.co.jp
→ 個人のマイドライブ
```

---

## 🚀 セットアップ手順

### ステップ1: Googleアカウントの準備

#### 1-1. 使用するGoogleアカウントを決定

**推奨:**
- 社内共有用のGoogle Workspaceアカウント
- または個人の社内アカウント

**アカウント例:**
```
メインアカウント: shared-docs@mm-international.co.jp
サブアカウント: dept-admin@mm-international.co.jp
```

#### 1-2. アカウントの権限を確認

各アカウントで以下を確認：
- Google Driveへのアクセス権限
- 参照したいフォルダの閲覧権限

---

### ステップ2: Google Cloud Console設定（アカウントごと）

#### 2-1. プロジェクトの作成

1. https://console.cloud.google.com/ にアクセス
2. **使用するGoogleアカウントでログイン**
3. 新しいプロジェクトを作成
   - プロジェクト名: `社内情報検索AI-共有アカウント`

#### 2-2. Google Drive APIを有効化

1. 「APIとサービス」→「ライブラリ」
2. 「Google Drive API」を検索
3. 「有効にする」をクリック

#### 2-3. OAuth同意画面を設定

1. 「APIとサービス」→「OAuth同意画面」
2. ユーザータイプ: **内部**（Google Workspaceの場合）
3. アプリ情報を入力:
   - **アプリ名:** 社内情報検索AI
   - **ユーザーサポートメール:** 使用するアカウントのメール
   - **デベロッパーの連絡先:** 使用するアカウントのメール

#### 2-4. 認証情報を作成

1. 「APIとサービス」→「認証情報」
2. 「認証情報を作成」→「OAuth クライアント ID」
3. アプリケーションの種類: **デスクトップアプリ**
4. 名前: `社内情報検索AI-共有アカウント`
5. 「作成」をクリック
6. **JSONをダウンロード**

#### 2-5. 認証情報ファイルをリネーム

```bash
# ダウンロードしたファイルをアカウント別にリネーム
client_secret_xxxxx.json
↓
google_drive_credentials.json         # メインアカウント用
google_drive_credentials_dept.json    # 部門アカウント用
google_drive_credentials_admin.json   # 管理者アカウント用
```

---

### ステップ3: 設定ファイルの編集

#### 3-1. 設定ファイルをコピー

```bash
copy google_drive_config.json.template google_drive_config.json
```

#### 3-2. アカウント情報を設定

`google_drive_config.json` を開いて編集：

```json
{
    "enabled": true,
    "accounts": [
        {
            "name": "社内共有アカウント",
            "email": "shared-docs@mm-international.co.jp",
            "credentials_file": "google_drive_credentials.json",
            "token_file": "google_drive_token.pickle",
            "active": true
        },
        {
            "name": "管理部アカウント",
            "email": "admin@mm-international.co.jp",
            "credentials_file": "google_drive_credentials_admin.json",
            "token_file": "google_drive_token_admin.pickle",
            "active": false
        }
    ],
    "folders": [
        {
            "name": "社内文書",
            "folder_id": "1aBcDeFgHiJkLmNoPqRs",
            "local_path": "./data/google_drive/社内文書",
            "sync": true,
            "file_types": ["pdf", "docx", "txt"],
            "account": "社内共有アカウント"
        },
        {
            "name": "管理部資料",
            "folder_id": "2bCdEfGhIjKlMnOpQrSt",
            "local_path": "./data/google_drive/管理部資料",
            "sync": true,
            "file_types": ["pdf", "xlsx"],
            "account": "管理部アカウント"
        }
    ]
}
```

**設定項目:**

| 項目 | 説明 | 例 |
|------|------|-----|
| `name` | アカウントの識別名 | `"社内共有アカウント"` |
| `email` | Googleアカウントのメール | `"shared@mm-international.co.jp"` |
| `credentials_file` | 認証情報ファイル名 | `"google_drive_credentials.json"` |
| `token_file` | トークンファイル名 | `"google_drive_token.pickle"` |
| `active` | このアカウントを使用するか | `true` または `false` |
| `account` | フォルダが属するアカウント名 | `"社内共有アカウント"` |

---

### ステップ4: 各アカウントで認証

#### 4-1. メインアカウントで認証

```bash
# デモアプリを起動
streamlit run google_drive_manager.py
```

1. ブラウザで認証画面が開く
2. **メインアカウント**（shared-docs@mm-international.co.jp）でログイン
3. 権限を許可
4. 「認証に成功しました」と表示される

→ `google_drive_token.pickle` が作成される

#### 4-2. サブアカウントで認証（必要な場合）

設定ファイルで `active: true` に変更してから：

```bash
streamlit run google_drive_manager.py
```

1. **サブアカウント**でログイン
2. 権限を許可

→ `google_drive_token_admin.pickle` が作成される

---

## 💻 使用方法

### 方法1: デモアプリで確認

```bash
streamlit run google_drive_manager.py
```

**アカウント情報の確認:**
- サイドバーに現在のアカウントが表示される
- フォルダ一覧でアカウント別にフォルダが表示される

### 方法2: Pythonコードで使用

```python
import google_drive_manager as gdm
import json

# 設定ファイルを読み込む
with open('google_drive_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# アクティブなアカウントを取得
active_account = None
for account in config['accounts']:
    if account.get('active', False):
        active_account = account
        break

# Google Driveマネージャーを初期化
drive = gdm.GoogleDriveManager(account_config=active_account)

# 認証確認
if drive.is_authenticated():
    print(f"認証済みアカウント: {drive.account_email}")
    
    # フォルダ一覧を取得
    folders = drive.list_folders()
    for folder in folders:
        print(f"📁 {folder['name']}")
```

### 方法3: アカウント別に同期

```python
import json
from google_drive_manager import GoogleDriveManager

# 設定を読み込む
with open('google_drive_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 各アカウントでフォルダを同期
for account in config['accounts']:
    if not account.get('active', False):
        continue
    
    print(f"アカウント: {account['email']}")
    
    # アカウント用のマネージャーを作成
    drive = GoogleDriveManager(account_config=account)
    
    # このアカウントのフォルダを取得
    for folder_config in config['folders']:
        if folder_config.get('account') == account['name']:
            print(f"  同期: {folder_config['name']}")
            
            files = drive.list_files(folder_config['folder_id'])
            # ダウンロード処理...
```

---

## 🔄 アカウントの切り替え

### 方法1: 設定ファイルで切り替え

`google_drive_config.json` を編集：

```json
{
    "accounts": [
        {
            "name": "社内共有アカウント",
            "email": "shared@mm-international.co.jp",
            "active": false  ← false に変更
        },
        {
            "name": "管理部アカウント",
            "email": "admin@mm-international.co.jp",
            "active": true   ← true に変更
        }
    ]
}
```

### 方法2: 複数アカウントを同時使用

```python
# アカウント1でフォルダAを同期
drive1 = GoogleDriveManager(account_config={
    'email': 'shared@mm-international.co.jp',
    'credentials_file': 'google_drive_credentials.json',
    'token_file': 'google_drive_token.pickle'
})
drive1.download_folder('FOLDER_A_ID', './data/folder_a')

# アカウント2でフォルダBを同期
drive2 = GoogleDriveManager(account_config={
    'email': 'admin@mm-international.co.jp',
    'credentials_file': 'google_drive_credentials_admin.json',
    'token_file': 'google_drive_token_admin.pickle'
})
drive2.download_folder('FOLDER_B_ID', './data/folder_b')
```

---

## 🔐 セキュリティベストプラクティス

### 1. アカウントの分離

**推奨構成:**
```
公開資料 → 共有アカウント（全社員アクセス可）
機密資料 → 管理者アカウント（制限付き）
個人資料 → 個人アカウント
```

### 2. 認証情報の管理

```
認証情報ファイル:
- google_drive_credentials.json         # 共有アカウント用
- google_drive_credentials_admin.json   # 管理者用

トークンファイル:
- google_drive_token.pickle             # 共有アカウント用
- google_drive_token_admin.pickle       # 管理者用

→ すべて .gitignore に含まれる
```

### 3. アクセス権限の最小化

- 読み取り専用スコープのみ使用
- 必要なフォルダのみ共有
- 定期的にアクセス権限を見直す

---

## 🎯 実用例

### 例1: 部門別アカウント構成

```json
{
    "accounts": [
        {
            "name": "営業部",
            "email": "sales@mm-international.co.jp",
            "credentials_file": "google_drive_credentials_sales.json",
            "token_file": "google_drive_token_sales.pickle",
            "active": true
        },
        {
            "name": "技術部",
            "email": "tech@mm-international.co.jp",
            "credentials_file": "google_drive_credentials_tech.json",
            "token_file": "google_drive_token_tech.pickle",
            "active": true
        }
    ],
    "folders": [
        {
            "name": "営業資料",
            "folder_id": "...",
            "account": "営業部"
        },
        {
            "name": "技術文書",
            "folder_id": "...",
            "account": "技術部"
        }
    ]
}
```

### 例2: 個人アカウント + 共有アカウント

```json
{
    "accounts": [
        {
            "name": "個人アカウント",
            "email": "yamada.taro@mm-international.co.jp",
            "credentials_file": "google_drive_credentials_personal.json",
            "token_file": "google_drive_token_personal.pickle",
            "active": true
        },
        {
            "name": "共有アカウント",
            "email": "shared@mm-international.co.jp",
            "credentials_file": "google_drive_credentials_shared.json",
            "token_file": "google_drive_token_shared.pickle",
            "active": true
        }
    ]
}
```

---

## 🔧 トラブルシューティング

### 間違ったアカウントで認証してしまった

**解決法:**

```bash
# 1. トークンファイルを削除
del google_drive_token.pickle

# 2. アプリを再起動
streamlit run google_drive_manager.py

# 3. 正しいアカウントでログイン
```

### 複数アカウントで同じ認証情報ファイルを使ってしまった

**解決法:**

各アカウント用に別々の認証情報を作成：
1. Google Cloud Consoleで各アカウント用のプロジェクトを作成
2. 各プロジェクトで認証情報を作成
3. 異なるファイル名で保存

### アカウントの切り替えがうまくいかない

**解決法:**

```bash
# すべてのトークンファイルを削除
del google_drive_token*.pickle

# 各アカウントで再認証
```

---

## 📊 アカウント管理のベストプラクティス

### 命名規則

```
認証情報ファイル:
- google_drive_credentials.json           # メイン
- google_drive_credentials_{部門名}.json  # 部門別

トークンファイル:
- google_drive_token.pickle               # メイン
- google_drive_token_{部門名}.pickle      # 部門別
```

### フォルダ構成

```
プロジェクトルート/
├── google_drive_credentials.json        # 共有アカウント
├── google_drive_credentials_admin.json  # 管理者
├── google_drive_credentials_sales.json  # 営業部
├── google_drive_token.pickle            # 共有アカウントトークン
├── google_drive_token_admin.pickle      # 管理者トークン
└── google_drive_token_sales.pickle      # 営業部トークン
```

---

## ✅ チェックリスト

アカウント別セットアップ：

- [ ] 使用するGoogleアカウントを決定
- [ ] 各アカウントでGoogle Cloud Consoleにアクセス
- [ ] 各アカウントでプロジェクトを作成
- [ ] 各アカウントでGoogle Drive APIを有効化
- [ ] 各アカウントで認証情報を作成・ダウンロード
- [ ] 認証情報ファイルをアカウント別にリネーム・配置
- [ ] `google_drive_config.json` にアカウント情報を追加
- [ ] 各アカウントで認証（トークン生成）
- [ ] アカウント別にフォルダを割り当て
- [ ] 動作確認

---

## 📞 サポート

- **メール:** ai-support@mm-international.co.jp
- **デモアプリ:** `streamlit run google_drive_manager.py`
- **基本ガイド:** `GOOGLE_DRIVE_SETUP.md`

---

*最終更新：2025年12月13日*  
*株式会社エムエムインターナショナル*



