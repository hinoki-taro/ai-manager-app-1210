# Google Drive連携セットアップガイド

株式会社エムエムインターナショナル 社内情報検索AIアプリに、Google Driveフォルダを参照する機能を追加するガイドです。

---

## 📋 概要

### できること

1. ✅ **Google Driveフォルダの閲覧**
2. ✅ **ファイルの検索**
3. ✅ **ファイルのダウンロード**
4. ✅ **フォルダ全体の同期**
5. ✅ **自動同期（定期的に更新）**

### 対応ファイル形式

- PDF
- Word（.docx）
- Excel（.xlsx）
- PowerPoint（.pptx）
- テキスト（.txt）
- CSV

---

## 🚀 セットアップ手順

### ステップ1: ライブラリのインストール

```bash
# Google Drive APIライブラリをインストール
pip install -r requirements_google_drive.txt
```

**含まれるライブラリ:**
- `google-api-python-client` - Google Drive API
- `google-auth` - Google認証
- `google-auth-oauthlib` - OAuth2.0認証

---

### ステップ2: Google Cloud Console設定

#### 2-1. Google Cloud Consoleにアクセス

https://console.cloud.google.com/

#### 2-2. 新しいプロジェクトを作成

1. 「プロジェクトを選択」をクリック
2. 「新しいプロジェクト」をクリック
3. プロジェクト名を入力（例: `社内情報検索AI`）
4. 「作成」をクリック

#### 2-3. Google Drive APIを有効化

1. 左メニューから「APIとサービス」→「ライブラリ」
2. 「Google Drive API」を検索
3. 「有効にする」をクリック

#### 2-4. OAuth同意画面を設定

1. 左メニューから「APIとサービス」→「OAuth同意画面」
2. ユーザータイプ: **内部**（Google Workspaceの場合）または **外部**
3. 「作成」をクリック
4. アプリ情報を入力:
   - **アプリ名:** 社内情報検索AI
   - **ユーザーサポートメール:** あなたのメールアドレス
   - **デベロッパーの連絡先情報:** あなたのメールアドレス
5. 「保存して次へ」
6. スコープ: 追加不要（デフォルトのまま）
7. 「保存して次へ」
8. 「ダッシュボードに戻る」

#### 2-5. 認証情報を作成

1. 左メニューから「APIとサービス」→「認証情報」
2. 「認証情報を作成」→「OAuth クライアント ID」
3. アプリケーションの種類: **デスクトップアプリ**
4. 名前: 任意（例: `社内情報検索AIクライアント`）
5. 「作成」をクリック
6. **JSONをダウンロード**をクリック

#### 2-6. 認証情報ファイルを配置

```bash
# ダウンロードしたJSONファイルをリネーム
ダウンロードしたファイル: client_secret_xxxxx.json
↓
google_drive_credentials.json

# アプリのルートディレクトリに配置
配置先: C:\Users\...\社内情報特化型生成AI検索アプリ\google_drive_credentials.json
```

---

### ステップ3: Google DriveフォルダIDの取得

#### 3-1. Google Driveでフォルダを開く

ブラウザでGoogle Driveにアクセスし、参照したいフォルダを開く

#### 3-2. URLからフォルダIDをコピー

```
URL例:
https://drive.google.com/drive/folders/1aBcDeFgHiJkLmNoPqRsTuVwXyZ123456

フォルダID:
1aBcDeFgHiJkLmNoPqRsTuVwXyZ123456
       ↑ この部分をコピー
```

#### 3-3. 複数のフォルダIDを取得

参照したいフォルダごとにIDを取得します：

- 社内文書フォルダ → フォルダID1
- メディアフォルダ → フォルダID2
- 顧客情報フォルダ → フォルダID3

---

### ステップ4: 設定ファイルの作成

#### 4-1. テンプレートをコピー

```bash
# テンプレートをコピー
copy google_drive_config.json.template google_drive_config.json
```

#### 4-2. 設定ファイルを編集

`google_drive_config.json` を開いて編集:

```json
{
    "enabled": true,
    "folders": [
        {
            "name": "社内文書",
            "folder_id": "1aBcDeFgHiJkLmNoPqRsTuVwXyZ123456",
            "local_path": "./data/google_drive/社内文書",
            "sync": true,
            "file_types": ["pdf", "docx", "txt"]
        },
        {
            "name": "メディアについて",
            "folder_id": "2bCdEfGhIjKlMnOpQrStUvWxYz234567",
            "local_path": "./data/google_drive/メディアについて",
            "sync": true,
            "file_types": ["pdf", "docx", "pptx"]
        }
    ],
    "sync_on_startup": true,
    "auto_sync_interval_minutes": 60
}
```

**設定項目:**
- `enabled`: Google Drive連携を有効にするか（`true` または `false`）
- `folder_id`: Google DriveのフォルダID（ステップ3で取得）
- `local_path`: ダウンロード先のローカルパス
- `sync`: 同期を有効にするか
- `file_types`: 同期するファイル形式
- `sync_on_startup`: アプリ起動時に自動同期するか
- `auto_sync_interval_minutes`: 自動同期の間隔（分）

---

### ステップ5: 初回認証

#### 5-1. デモアプリで認証

```bash
# デモアプリを起動
streamlit run google_drive_manager.py
```

#### 5-2. 認証フロー

1. アプリ起動時にブラウザが開く
2. Googleアカウントでログイン
3. 「このアプリは確認されていません」と表示される場合:
   - 「詳細」をクリック
   - 「（アプリ名）に移動」をクリック
4. 権限を確認して「許可」をクリック
5. 「認証に成功しました」と表示される

#### 5-3. トークンの保存

認証が成功すると、`google_drive_token.pickle` が作成されます。
このファイルには認証情報が保存され、次回から自動的にログインされます。

---

## 💻 使用方法

### 方法1: デモアプリを使用

```bash
streamlit run google_drive_manager.py
```

**機能:**
- フォルダ一覧の表示
- ファイル検索
- ファイルのダウンロード
- 設定管理

### 方法2: Pythonコードで使用

```python
import google_drive_manager as gdm

# 初期化
drive = gdm.GoogleDriveManager()

# フォルダ一覧を取得
folders = drive.list_folders()

# ファイル一覧を取得
files = drive.list_files(folder_id='YOUR_FOLDER_ID')

# ファイルをダウンロード
drive.download_file(file_id='YOUR_FILE_ID', destination_path='local_file.pdf')

# フォルダ全体をダウンロード
drive.download_folder(folder_id='YOUR_FOLDER_ID', destination_dir='./downloads')
```

### 方法3: 自動同期

```python
from google_drive_manager import sync_google_drive_folders

# 設定ファイルに基づいて同期
sync_google_drive_folders()
```

---

## 🔄 メインアプリへの統合

### `initialize.py` に追加

```python
# Google Drive同期を追加
try:
    from google_drive_manager import sync_google_drive_folders
    
    # 設定ファイルを読み込む
    if os.path.exists('google_drive_config.json'):
        with open('google_drive_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 起動時同期が有効な場合
        if config.get('sync_on_startup', False):
            sync_google_drive_folders()
except Exception as e:
    logger.warning(f"Google Drive同期に失敗: {str(e)}")
```

---

## 📊 フォルダ構成例

### ローカルフォルダ構成

```
data/
├── google_drive/
│   ├── 社内文書/
│   │   ├── 規則規程.pdf
│   │   ├── 手順書.docx
│   │   └── FAQ.txt
│   ├── メディアについて/
│   │   ├── プレスリリース.pdf
│   │   └── 会社紹介.pptx
│   └── 顧客について/
│       ├── 顧客リスト.xlsx
│       └── 契約書.pdf
└── メディアについて/
    └── （既存のファイル）
```

### Google Drive構成

```
マイドライブ/
├── 社内情報検索AI/
│   ├── 社内文書/
│   │   └── （共有ファイル）
│   ├── メディアについて/
│   │   └── （共有ファイル）
│   └── 顧客について/
│       └── （共有ファイル）
```

---

## 🔐 セキュリティ

### 認証情報の保護

#### `.gitignore` に追加（済み）

```
# Google Drive認証情報
google_drive_credentials.json
google_drive_token.pickle
google_drive_config.json
```

### アクセス権限

- **読み取り専用:** デフォルトで読み取り専用アクセス
- **最小権限の原則:** 必要最小限の権限のみ要求
- **トークンの有効期限:** 定期的にリフレッシュ

### ベストプラクティス

1. **認証情報は共有しない**
2. **トークンファイルは Git に含めない**
3. **社内専用のGoogle Workspaceアカウントを使用**
4. **定期的にアクセス権限を見直す**

---

## 🔧 トラブルシューティング

### エラー: 認証情報が見つかりません

**原因:** `google_drive_credentials.json` が配置されていない

**解決法:**
1. Google Cloud Consoleで認証情報をダウンロード
2. `google_drive_credentials.json` にリネーム
3. アプリのルートディレクトリに配置

### エラー: このアプリは確認されていません

**原因:** OAuth同意画面が「テスト」モードの場合に表示される

**解決法:**
1. 「詳細」をクリック
2. 「（アプリ名）に移動」をクリック
3. 本番環境では、アプリを「公開」に設定

### エラー: 403 Forbidden

**原因:** APIが有効化されていない、または権限不足

**解決法:**
1. Google Cloud ConsoleでGoogle Drive APIが有効か確認
2. OAuth同意画面のスコープを確認
3. トークンを削除して再認証: `del google_drive_token.pickle`

### ファイルがダウンロードできない

**原因:** ファイルへのアクセス権限がない

**解決法:**
1. Google Driveでファイルの共有設定を確認
2. 認証に使用したアカウントに閲覧権限があるか確認

---

## 📈 自動同期の設定

### 定期的な同期

```python
# initialize.pyまたは別のスケジューラーで設定

import schedule
import time
from google_drive_manager import sync_google_drive_folders

# 1時間ごとに同期
schedule.every(60).minutes.do(sync_google_drive_folders)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 📞 サポート

### ヘルプが必要な場合

- **メール:** ai-support@mm-international.co.jp
- **デモアプリ:** `streamlit run google_drive_manager.py`
- **Google Cloud Console:** https://console.cloud.google.com/

---

## ✅ チェックリスト

セットアップ完了確認：

- [ ] `requirements_google_drive.txt` からインストール
- [ ] Google Cloud Consoleでプロジェクト作成
- [ ] Google Drive APIを有効化
- [ ] OAuth同意画面を設定
- [ ] 認証情報（OAuth クライアント ID）を作成
- [ ] `google_drive_credentials.json` を配置
- [ ] Google DriveフォルダIDを取得
- [ ] `google_drive_config.json` を作成・編集
- [ ] デモアプリで初回認証
- [ ] `google_drive_token.pickle` が作成される
- [ ] ファイルのダウンロードをテスト
- [ ] フォルダ同期をテスト

---

*最終更新：2025年12月13日*  
*株式会社エムエムインターナショナル*

