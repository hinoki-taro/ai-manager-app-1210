# 特定Googleアカウント連携クイックスタート

**5分で完了！** 特定のGoogleアカウントを指定してGoogle Driveを参照する最速セットアップガイド

---

## 🎯 やりたいこと

```
✅ 特定のGoogleアカウント（例: shared@mm-international.co.jp）
  ↓
✅ そのアカウントのGoogle Drive
  ↓
✅ 指定したフォルダ
  ↓
✅ AIアプリで検索可能に！
```

---

## ⚡ 5ステップで完了

### 【1】ライブラリをインストール

```bash
pip install -r requirements_google_drive.txt
```

**所要時間:** 約1分

---

### 【2】アカウントを設定

```bash
python setup_google_account.py
```

**入力例:**
```
アカウント名: 社内共有アカウント
メールアドレス: shared@mm-international.co.jp
認証情報ファイル名: （Enterでデフォルト）
アクティブにしますか？: Y
```

→ `google_drive_config.json` が自動生成！

**所要時間:** 約30秒

---

### 【3】Google Cloud Consoleで認証情報を作成

#### 3-1. プロジェクト作成

1. https://console.cloud.google.com/ にアクセス
2. **使用するGoogleアカウント**（shared@mm-international.co.jp）でログイン
3. 「プロジェクトを作成」
   - 名前: `社内情報検索AI`

#### 3-2. APIを有効化

1. 「APIとサービス」→「ライブラリ」
2. 「Google Drive API」を検索
3. 「有効にする」

#### 3-3. OAuth同意画面

1. 「APIとサービス」→「OAuth同意画面」
2. ユーザータイプ: **内部**
3. アプリ名: `社内情報検索AI`
4. メール: shared@mm-international.co.jp

#### 3-4. 認証情報を作成

1. 「APIとサービス」→「認証情報」
2. 「認証情報を作成」→「OAuth クライアント ID」
3. アプリケーションの種類: **デスクトップアプリ**
4. **JSONをダウンロード**

#### 3-5. ファイルを配置

```bash
# ダウンロードしたファイルをリネーム
client_secret_xxxxx.json
↓
google_drive_credentials.json

# アプリのルートディレクトリに配置
```

**所要時間:** 約2-3分

---

### 【4】Google DriveフォルダIDを取得

1. Google Driveで参照したいフォルダを開く
2. URLからIDをコピー

```
https://drive.google.com/drive/folders/1aBcDeFgHiJkLmNoPqRs
                                        ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
                                        この部分をコピー
```

**所要時間:** 約10秒

---

### 【5】フォルダを追加して認証

```bash
python setup_google_account.py
```

メニューから「3. フォルダを追加」を選択

**入力例:**
```
フォルダ名: 社内文書
フォルダID: 1aBcDeFgHiJkLmNoPqRs
ローカル保存先: （Enterでデフォルト）
ファイル形式: （Enterでデフォルト: pdf,docx,txt）
使用するアカウント: 1
自動同期を有効にしますか？: Y
```

**初回認証:**
```bash
streamlit run google_drive_manager.py
```

1. ブラウザが開く
2. **shared@mm-international.co.jp** でログイン
3. 権限を許可
4. 完了！

**所要時間:** 約1分

---

## ✅ 完了！

これで、指定したGoogleアカウントのGoogle Driveフォルダが参照できます！

### 動作確認

```bash
streamlit run google_drive_manager.py
```

デモアプリで以下を確認：
- ✅ アカウント情報が表示される
- ✅ フォルダ一覧が取得できる
- ✅ ファイルをダウンロードできる

---

## 🎯 設定例

### 例1: 社内共有アカウント1つ

```json
{
    "enabled": true,
    "accounts": [
        {
            "name": "社内共有アカウント",
            "email": "shared@mm-international.co.jp",
            "credentials_file": "google_drive_credentials.json",
            "token_file": "google_drive_token.pickle",
            "active": true
        }
    ],
    "folders": [
        {
            "name": "社内文書",
            "folder_id": "YOUR_FOLDER_ID",
            "local_path": "./data/google_drive/社内文書",
            "sync": true,
            "file_types": ["pdf", "docx", "txt"],
            "account": "社内共有アカウント"
        }
    ]
}
```

### 例2: 複数のアカウントと複数のフォルダ

```json
{
    "enabled": true,
    "accounts": [
        {
            "name": "営業部アカウント",
            "email": "sales@mm-international.co.jp",
            "credentials_file": "google_drive_credentials_sales.json",
            "token_file": "google_drive_token_sales.pickle",
            "active": true
        },
        {
            "name": "技術部アカウント",
            "email": "tech@mm-international.co.jp",
            "credentials_file": "google_drive_credentials_tech.json",
            "token_file": "google_drive_token_tech.pickle",
            "active": true
        }
    ],
    "folders": [
        {
            "name": "営業資料",
            "folder_id": "SALES_FOLDER_ID",
            "account": "営業部アカウント"
        },
        {
            "name": "技術文書",
            "folder_id": "TECH_FOLDER_ID",
            "account": "技術部アカウント"
        }
    ]
}
```

---

## 🔧 よくある質問

### Q1: どのGoogleアカウントを使えばいい？

**A:** 参照したいGoogle Driveフォルダにアクセス権限があるアカウント

**推奨:**
- 社内の共有アカウント
- または個人の社内Google Workspaceアカウント

### Q2: 複数のアカウントを使える？

**A:** はい！アカウントごとに認証情報ファイルを用意すれば、複数のアカウントを同時に使えます。

### Q3: 認証は毎回必要？

**A:** いいえ。初回認証後、トークンファイルが保存されるので、次回から自動的にログインされます。

### Q4: 間違ったアカウントで認証してしまった

**A:** トークンファイルを削除して再認証：
```bash
del google_drive_token.pickle
streamlit run google_drive_manager.py
```

---

## 📚 詳細ガイド

もっと詳しく知りたい場合：

- **基本ガイド:** `GOOGLE_DRIVE_SETUP.md`
- **アカウント指定:** `GOOGLE_DRIVE_ACCOUNT_SETUP.md`
- **機能一覧:** `GOOGLE_DRIVE_SUMMARY.md`

---

## 📞 サポート

- **メール:** ai-support@mm-international.co.jp
- **設定ツール:** `python setup_google_account.py`
- **デモアプリ:** `streamlit run google_drive_manager.py`

---

*所要時間合計: 約5-7分*  
*株式会社エムエムインターナショナル*



