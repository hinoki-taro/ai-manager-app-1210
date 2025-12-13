# 🚀 社内情報特化型生成AI検索アプリ - デプロイガイド

## 目次

1. [はじめに](#はじめに)
2. [事前準備](#事前準備)
3. [Streamlit Cloudへのデプロイ手順](#streamlit-cloudへのデプロイ手順)
4. [セキュリティ設定](#セキュリティ設定)
5. [アクセス制御の設定](#アクセス制御の設定)
6. [トラブルシューティング](#トラブルシューティング)

---

## はじめに

このガイドでは、社内情報特化型生成AI検索アプリをStreamlit Cloudにデプロイする手順を説明します。

### デプロイ方法の選択肢

| 方法 | 推奨度 | 特徴 | コスト |
|------|-------|------|--------|
| **Streamlit Community Cloud** | ⭐⭐⭐ | 簡単、GitHubと連携 | 無料 |
| AWS/GCP/Azure | ⭐⭐ | 本格的な運用向け | 有料 |
| 社内サーバー | ⭐ | 完全なコントロール | サーバー管理が必要 |

このガイドでは **Streamlit Community Cloud**（無料）を使った方法を説明します。

---

## 事前準備

### 1. GitHubリポジトリの作成

```bash
# 1. GitHubで新しいリポジトリを作成
#    - Repository name: internal-ai-search-app（任意の名前）
#    - Private を選択（社内情報のため）

# 2. ローカルのプロジェクトをGitで管理
cd "C:\Users\mtokyo081\Desktop\cursor\社内情報特化型生成AI検索アプリ"
git init

# 3. .gitignoreの確認
#    機密情報が含まれていないことを確認
git status

# 4. 初回コミット
git add .
git commit -m "Initial commit: AI search app"

# 5. GitHubにプッシュ
git remote add origin https://github.com/あなたのユーザー名/internal-ai-search-app.git
git branch -M main
git push -u origin main
```

### 2. 必要なアカウント

- ✅ GitHubアカウント（無料）
- ✅ Streamlit Cloudアカウント（無料、GitHubで登録）
- ✅ Google Gemini API Key（無料）

---

## Streamlit Cloudへのデプロイ手順

### ステップ1: Streamlit Cloudにサインアップ

1. [Streamlit Community Cloud](https://share.streamlit.io/) にアクセス
2. 「Sign up with GitHub」をクリック
3. GitHubアカウントで認証

### ステップ2: 新しいアプリをデプロイ

1. ダッシュボードで「New app」をクリック
2. 以下の情報を入力：

```
Repository: あなたのGitHubユーザー名/internal-ai-search-app
Branch: main
Main file path: main.py
App URL: internal-ai-search-app（任意）
```

3. 「Deploy!」をクリック

⚠️ **この時点ではエラーが出ます**（APIキーが未設定のため）

### ステップ3: Secretsの設定

1. デプロイ画面の「Settings」→「Secrets」に移動
2. 以下の内容をコピー＆ペースト：

```toml
# Google Gemini API Key
GOOGLE_API_KEY = "AIzaSyBlp0GgqOrY5VLVP703PKk-J1UKuDHuhKQ"
```

3. 「Save」をクリック
4. アプリが自動的に再起動されます

### ステップ4: データファイルの配置

⚠️ **重要**: デフォルトでは `data/` ディレクトリは `.gitignore` に含まれています。

**オプション1: 少量のサンプルデータでテスト**

```bash
# data_sample フォルダを作成し、テスト用の数ファイルのみ配置
mkdir data_sample
# サンプルファイルをコピー
# Git にコミット
git add data_sample/
git commit -m "Add sample data"
git push
```

**オプション2: 本番データの配置（推奨しない）**

社内情報を含むため、**公開リポジトリには絶対にアップロードしないでください**。

代替案：
- Google Driveなどのクラウドストレージに配置し、起動時にダウンロード
- Streamlit Cloudのファイルアップロード機能を使用
- 環境変数で外部APIから取得

---

## セキュリティ設定

### 1. リポジトリのPrivate設定

```
GitHubリポジトリ → Settings → General
→ Danger Zone → Change repository visibility
→ Make private を選択
```

### 2. Streamlit Cloudのアクセス制限

**方法A: メールドメイン制限（推奨）**

1. アプリのSettings → Sharing
2. 「Restrict to specific email domains」を有効化
3. 社内ドメインを入力: `@mm-international.co.jp`

**方法B: 招待制**

1. Settings → Sharing
2. 「Invite viewers」で社員のメールアドレスを追加

**方法C: パスワード認証（実装済み）**

アプリ内の認証機能を使用する場合：

1. Streamlit Cloud の Secrets に追加：

```toml
[auth]
password = "your_secure_company_password_here"
```

2. アプリにアクセスすると、パスワード入力画面が表示されます

### 3. 環境変数のセキュリティ

✅ **必ずやること**:
- APIキーは `.env` や `.streamlit/secrets.toml` に保存
- これらのファイルは `.gitignore` に含める
- GitHubに機密情報をプッシュしない

⚠️ **やってはいけないこと**:
- コード内にAPIキーを直接記述
- `data/` フォルダをGitにコミット
- 公開リポジトリで社内情報を管理

---

## アクセス制御の設定

### パスワード認証の有効化

#### 方法1: 環境変数で設定

```bash
# ローカル（.env ファイル）
ACCESS_PASSWORD=your_secure_password

# 認証を無効化する場合
DISABLE_AUTH=true
```

#### 方法2: Streamlit Secrets で設定

```toml
# Streamlit Cloud の Secrets
[auth]
password = "your_secure_company_password"
```

#### 認証機能の特徴

✅ セッション管理: ログイン状態を保持
✅ ログアウト機能: サイドバーにボタンを表示
✅ 柔軟な設定: 環境に応じて有効/無効を切り替え可能

---

## トラブルシューティング

### 問題1: アプリが起動しない

**原因**: APIキーが未設定

**解決策**:
1. Settings → Secrets で `GOOGLE_API_KEY` を確認
2. 値が正しいか確認（余分なスペースなし）
3. 「Reboot app」をクリック

### 問題2: データが読み込まれない

**原因**: `data/` フォルダが存在しない

**解決策**:
1. サンプルデータで動作確認
2. 本番データは安全な方法で配置

### 問題3: Gemini APIの制限エラー

**エラー**: `429 Quota exceeded`

**解決策**:
- 無料版は1日1500リクエスト
- 翌日のUTC 0:00（日本時間9:00）に制限がリセット
- データファイル数を減らす（推奨: 25ファイル以下）

### 問題4: モジュールが見つからない

**エラー**: `ModuleNotFoundError: No module named 'xxx'`

**解決策**:
1. `requirements.txt` にパッケージが記載されているか確認
2. バージョン指定が正しいか確認
3. アプリを再デプロイ

### 問題5: 認証画面が表示されない

**原因**: パスワードが設定されていない

**確認**:
- 認証を有効にする場合は Secrets に `[auth]` セクションを追加
- 認証を無効にする場合は `DISABLE_AUTH=true` を設定

---

## デプロイ後のチェックリスト

- [ ] アプリが正常に起動する
- [ ] APIキーが正しく設定されている
- [ ] データファイルが読み込まれている
- [ ] 質問に対して適切な回答が返される
- [ ] アクセス制限が適切に設定されている
- [ ] パスワード認証（有効化している場合）が機能する
- [ ] GitHubリポジトリがPrivateになっている
- [ ] 機密情報がGitにコミットされていない

---

## サポート

### 公式ドキュメント

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Community Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Google Gemini API](https://ai.google.dev/gemini-api/docs)

### よくある質問

**Q: 無料で使い続けられますか？**
A: はい。Streamlit Community Cloudは無料で、Google Gemini APIも無料枠内で使用可能です。

**Q: 複数人で同時にアクセスできますか？**
A: はい。ただし、API制限（1日1500リクエスト）に注意してください。

**Q: データを更新するには？**
A: GitHubリポジトリを更新し、プッシュすると自動的にデプロイされます。

**Q: カスタムドメインは使えますか？**
A: Streamlit Community Cloudでは独自ドメインは使用できません。有料プランにアップグレードが必要です。

---

## まとめ

このガイドに従えば、安全に社内AI検索アプリをWEB公開できます。

### 重要ポイント

1. ✅ **セキュリティ第一**: 機密情報は絶対にGitにコミットしない
2. ✅ **アクセス制限**: 社内限定の設定を忘れずに
3. ✅ **API制限**: 無料版の制限を理解する
4. ✅ **定期的な確認**: 正常に動作しているか定期チェック

**お疲れ様でした！🎉**

