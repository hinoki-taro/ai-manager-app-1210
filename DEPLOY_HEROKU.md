# Herokuへのデプロイ手順

## 前提条件
- Herokuアカウント（https://signup.heroku.com/）
- Heroku CLIのインストール

## ステップ1: Heroku CLIのインストール

### Windowsの場合
1. https://devcenter.heroku.com/articles/heroku-cli にアクセス
2. インストーラーをダウンロードして実行

### ログイン
```powershell
heroku login
```

ブラウザが開くので、ログインします。

## ステップ2: Herokuアプリの作成

```powershell
# アプリを作成（アプリ名は一意である必要があります）
heroku create ai-manager-app-2024

# または、自動生成された名前を使用
heroku create
```

## ステップ3: 環境変数の設定

```powershell
# Google Gemini APIキー
heroku config:set GOOGLE_API_KEY="AIzaSyCVOryUeFaYf1n8Oun9wAh9RxGYD4MkKuY"

# OpenAI APIキー
heroku config:set OPENAI_API_KEY="your-openai-api-key-here"

# 認証設定
heroku config:set AUTH_PASSWORD="your-secure-password-here"
heroku config:set AUTH_SESSION_TIMEOUT_MINUTES="60"
heroku config:set AUTH_MAX_LOGIN_ATTEMPTS="3"
```

## ステップ4: Buildpackの設定

```powershell
# Pythonビルドパックを追加
heroku buildpacks:set heroku/python

# 必要に応じてapt-buildpackを追加（システムパッケージ用）
heroku buildpacks:add --index 1 heroku-community/apt
```

## ステップ5: デプロイ

```powershell
# Gitリモートを追加（heroku createで自動追加される場合はスキップ）
heroku git:remote -a ai-manager-app-2024

# デプロイ
git push heroku main
```

## ステップ6: アプリを開く

```powershell
heroku open
```

ブラウザが開き、アプリが表示されます！

## ステップ7: ログの確認

```powershell
# リアルタイムログを表示
heroku logs --tail

# 最新500行のログを表示
heroku logs -n 500
```

## 料金について

Herokuの料金プラン：
- **Eco Dynos**: $5/月（推奨）
  - 1,000 dyno hours/月
  - スリープなし
  - メモリ512MB
- **Basic Dynos**: $7/月
  - メモリ512MB
  - カスタムドメイン対応

**注意**: Herokuは2022年11月から無料プランを廃止しています。

## トラブルシューティング

### エラー: "Application error"
```powershell
# ログを確認
heroku logs --tail

# アプリを再起動
heroku restart
```

### エラー: "No web process running"
`Procfile`が正しく設定されているか確認：
```
web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
```

### メモリ不足エラー
```powershell
# Dynoのスケールアップ
heroku ps:scale web=1:standard-1x
```

## 更新方法

コードを変更した後：

```powershell
# 1. Gitにコミット
git add .
git commit -m "Update application"

# 2. Herokuにプッシュ
git push heroku main
```

自動的に再デプロイされます！

## カスタムドメインの設定（オプション）

```powershell
# ドメインを追加
heroku domains:add www.example.com

# SSL証明書を自動設定
heroku certs:auto:enable
```

## データベースの追加（必要な場合）

```powershell
# PostgreSQLを追加
heroku addons:create heroku-postgresql:mini

# 接続情報を確認
heroku config:get DATABASE_URL
```

## パフォーマンス監視

```powershell
# メトリクスを確認
heroku ps

# Dynoの状態を確認
heroku ps:type
```

