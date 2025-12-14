# Google Cloud Console 認証情報作成ガイド

Google Driveアクセスに必要な認証情報を作成する詳細な手順です。

---

## 📋 事前準備

### 必要なもの

1. ✅ Googleアカウント（@mm-international.co.jpなど）
2. ✅ ブラウザ（Chrome推奨）
3. ✅ 約10分の作業時間

---

## 🚀 ステップバイステップ手順

### ステップ1: Google Cloud Consoleにアクセス

1. ブラウザで以下のURLを開く：
   ```
   https://console.cloud.google.com/
   ```

2. 使用するGoogleアカウントでログイン
   - 推奨: `shared@mm-international.co.jp`
   - または個人の社内アカウント

---

### ステップ2: プロジェクトを作成

#### 2-1. プロジェクト選択画面を開く

1. 画面上部の「プロジェクトを選択」をクリック
2. 表示されたダイアログで「新しいプロジェクト」をクリック

#### 2-2. プロジェクト情報を入力

```
プロジェクト名: 社内情報検索AI
プロジェクトID: （自動生成でOK）
場所: 組織なし（または適切な組織を選択）
```

3. 「作成」ボタンをクリック
4. プロジェクトが作成されるまで数秒待つ

#### 2-3. プロジェクトを選択

1. 画面上部のプロジェクト選択で「社内情報検索AI」を選択
2. ダッシュボードが表示される

---

### ステップ3: Google Drive APIを有効化

#### 3-1. APIライブラリに移動

1. 左側のメニューから「APIとサービス」をクリック
2. 「ライブラリ」をクリック

または以下のURLに直接アクセス：
```
https://console.cloud.google.com/apis/library
```

#### 3-2. Google Drive APIを検索

1. 検索ボックスに「Google Drive API」と入力
2. 検索結果から「Google Drive API」をクリック

#### 3-3. APIを有効化

1. 「有効にする」ボタンをクリック
2. 有効化が完了するまで数秒待つ
3. 「APIが有効になりました」と表示される

---

### ステップ4: OAuth同意画面を設定

#### 4-1. OAuth同意画面に移動

1. 左側のメニューから「APIとサービス」→「OAuth同意画面」をクリック

または以下のURLに直接アクセス：
```
https://console.cloud.google.com/apis/credentials/consent
```

#### 4-2. ユーザータイプを選択

**Google Workspaceアカウントの場合:**
- 「内部」を選択
- 「作成」をクリック

**個人のGoogleアカウントの場合:**
- 「外部」を選択
- 「作成」をクリック

#### 4-3. アプリ情報を入力

**必須項目:**

```
アプリ名: 社内情報検索AI
ユーザーサポートのメール: （あなたのメールアドレス）
例: shared@mm-international.co.jp

アプリのロゴ: （スキップ可）

アプリのドメイン:
- アプリのホームページ: （スキップ可）
- アプリのプライバシーポリシー: （スキップ可）
- アプリの利用規約: （スキップ可）

承認済みドメイン:
- mm-international.co.jp （必要に応じて）

デベロッパーの連絡先情報:
- （あなたのメールアドレス）
```

4. 「保存して次へ」をクリック

#### 4-4. スコープ（権限）の設定

1. 「スコープを追加または削除」をクリック
2. フィルタに「Google Drive API」と入力
3. 以下のスコープを選択:
   - `.../auth/drive.readonly` （読み取り専用）
   - `.../auth/drive.metadata.readonly` （メタデータ読み取り）

**または手動で追加:**
```
https://www.googleapis.com/auth/drive.readonly
https://www.googleapis.com/auth/drive.metadata.readonly
```

4. 「更新」をクリック
5. 「保存して次へ」をクリック

#### 4-5. テストユーザー（外部の場合のみ）

**「外部」を選択した場合:**
1. 「テストユーザーを追加」をクリック
2. 使用するGoogleアカウントのメールアドレスを入力
3. 「追加」をクリック

**「内部」を選択した場合:**
- このステップはスキップされます

4. 「保存して次へ」をクリック

#### 4-6. 確認

1. 設定内容を確認
2. 「ダッシュボードに戻る」をクリック

---

### ステップ5: 認証情報（OAuth クライアント ID）を作成

#### 5-1. 認証情報画面に移動

1. 左側のメニューから「APIとサービス」→「認証情報」をクリック

または以下のURLに直接アクセス：
```
https://console.cloud.google.com/apis/credentials
```

#### 5-2. 認証情報を作成

1. 画面上部の「認証情報を作成」をクリック
2. ドロップダウンから「OAuth クライアント ID」を選択

#### 5-3. アプリケーションの種類を選択

```
アプリケーションの種類: デスクトップアプリ
名前: 社内情報検索AIクライアント
```

**重要:** 必ず「デスクトップアプリ」を選択してください。
（「ウェブアプリケーション」ではありません）

#### 5-4. 作成

1. 「作成」ボタンをクリック
2. 「OAuth クライアントを作成しました」というダイアログが表示される

#### 5-5. 認証情報をダウンロード

1. ダイアログに表示される「JSONをダウンロード」をクリック
2. ファイルがダウンロードされる
   - ファイル名例: `client_secret_123456789.apps.googleusercontent.com.json`

3. ダイアログを閉じる

---

### ステップ6: 認証情報ファイルを配置

#### 6-1. ダウンロードしたファイルをリネーム

ダウンロードしたファイルを以下の名前に変更：

```
元のファイル名:
client_secret_123456789...json

変更後:
google_drive_credentials.json
```

**複数のアカウントを使用する場合:**
```
google_drive_credentials.json         # メインアカウント
google_drive_credentials_admin.json   # 管理者用
google_drive_credentials_sales.json   # 営業部用
```

#### 6-2. ファイルをアプリのルートに配置

ファイルを以下のディレクトリに移動：
```
C:\Users\mtokyo081\Desktop\cursor\社内情報特化型生成AI検索アプリ\
```

---

### ステップ7: 設定ファイルを作成

#### 7-1. アカウント設定ツールを実行

```bash
python setup_google_account.py
```

#### 7-2. アカウント情報を入力

```
アカウント名: 社内共有アカウント
メールアドレス: shared@mm-international.co.jp
認証情報ファイル名: （Enterでgoogle_drive_credentials.json）
アクティブにしますか？: Y
```

#### 7-3. セキュリティ設定を作成

```bash
copy google_drive_security_config.json.template google_drive_security_config.json
```

---

### ステップ8: 初回認証

#### 8-1. デモアプリを起動

```bash
streamlit run google_drive_manager.py
```

#### 8-2. ブラウザで認証

1. ブラウザが自動的に開く
2. Googleアカウント選択画面が表示される
3. 設定したアカウント（shared@mm-international.co.jp）を選択

#### 8-3. 「このアプリは確認されていません」画面

**「外部」で作成した場合に表示されます:**

1. 「詳細」をクリック
2. 「（アプリ名）に移動」をクリック

#### 8-4. 権限を許可

1. 「Google Driveのファイルの表示」権限の確認
2. 「許可」ボタンをクリック

#### 8-5. 認証完了

1. 「認証が完了しました」と表示される
2. ブラウザを閉じる
3. Streamlitアプリに戻る

---

## ✅ 完了確認

### 確認事項

以下のファイルが作成されていることを確認：

```
社内情報特化型生成AI検索アプリ/
├── google_drive_credentials.json     # 認証情報（作成済み）
├── google_drive_token.pickle          # トークン（認証後に自動作成）
├── google_drive_config.json           # 設定（setup_google_account.pyで作成）
└── google_drive_security_config.json  # セキュリティ設定
```

### 動作確認

```bash
# デモアプリで確認
streamlit run google_drive_manager.py

# または駆動テストを再実行
python test_google_drive.py
```

---

## 🔧 トラブルシューティング

### エラー: 「アクセスがブロックされました」

**原因:** OAuth同意画面が正しく設定されていない

**解決法:**
1. Google Cloud Consoleに戻る
2. 「OAuth同意画面」を確認
3. 公開ステータスを確認
4. テストユーザーにメールアドレスが追加されているか確認

### エラー: 「このアプリは確認されていません」

**原因:** OAuth同意画面のユーザータイプが「外部」の場合に表示される

**解決法:**
1. 「詳細」をクリック
2. 「（アプリ名）に移動」をクリック
3. これは正常な動作です

**本番環境の場合:**
- アプリを「公開」ステータスに変更（Googleの審査が必要）
- または「内部」（Google Workspace）に変更

### エラー: 認証情報ファイルが見つからない

**原因:** ファイル名またはパスが間違っている

**解決法:**
1. ファイル名を確認: `google_drive_credentials.json`
2. 配置場所を確認: アプリのルートディレクトリ
3. パスを確認:
   ```bash
   dir google_drive_credentials.json
   ```

### APIクォータ超過

**原因:** Google Drive APIの無料枠を超えた

**解決法:**
1. Google Cloud Consoleでクォータを確認
2. 必要に応じて課金を有効化
3. または翌日まで待つ

---

## 📞 サポート

### 問い合わせ先

- **メール:** ai-support@mm-international.co.jp
- **設定ツール:** `python setup_google_account.py`
- **テスト:** `python test_google_drive.py`

### 参考リンク

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Drive API ドキュメント](https://developers.google.com/drive/api/v3/about-sdk)
- [OAuth 2.0 認証](https://developers.google.com/identity/protocols/oauth2)

---

## ✅ チェックリスト

認証情報作成完了確認：

- [ ] Google Cloud Consoleにログイン
- [ ] プロジェクトを作成
- [ ] Google Drive APIを有効化
- [ ] OAuth同意画面を設定
- [ ] OAuth クライアント IDを作成
- [ ] 認証情報JSONをダウンロード
- [ ] ファイルをリネーム（google_drive_credentials.json）
- [ ] ファイルをアプリのルートに配置
- [ ] アカウント設定ツールを実行
- [ ] セキュリティ設定を作成
- [ ] デモアプリで初回認証
- [ ] 動作確認

---

*作成日：2025年12月13日*  
*株式会社エムエムインターナショナル*



