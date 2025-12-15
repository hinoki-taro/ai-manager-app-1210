# Google Cloud Runへのデプロイ手順

## 前提条件
- Googleアカウント
- Google Cloud Platform（GCP）のアカウント作成（無料トライアルあり）

## ステップ1: Google Cloud SDKのインストール

### Windowsの場合
1. https://cloud.google.com/sdk/docs/install にアクセス
2. インストーラーをダウンロードして実行

### 初期化
```powershell
gcloud init
gcloud auth login
```

## ステップ2: プロジェクトの作成

```powershell
# プロジェクトIDを設定（小文字・数字・ハイフンのみ）
$PROJECT_ID = "ai-manager-app-2024"

# プロジェクトを作成
gcloud projects create $PROJECT_ID

# プロジェクトを設定
gcloud config set project $PROJECT_ID

# 必要なAPIを有効化
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

## ステップ3: 環境変数ファイルの作成

プロジェクトルートに`.env.yaml`を作成：

```yaml
GOOGLE_API_KEY: "AIzaSyCVOryUeFaYf1n8Oun9wAh9RxGYD4MkKuY"
OPENAI_API_KEY: "your-openai-api-key-here"
AUTH_PASSWORD: "your-secure-password-here"
AUTH_SESSION_TIMEOUT_MINUTES: "60"
AUTH_MAX_LOGIN_ATTEMPTS: "3"
```

## ステップ4: Dockerイメージのビルドとプッシュ

```powershell
# Artifact Registryを有効化
gcloud services enable artifactregistry.googleapis.com

# リポジトリを作成
gcloud artifacts repositories create ai-manager-repo `
  --repository-format=docker `
  --location=asia-northeast1 `
  --description="AI Manager App Repository"

# Dockerイメージをビルド
docker build -t asia-northeast1-docker.pkg.dev/$PROJECT_ID/ai-manager-repo/ai-manager-app:latest .

# Docker認証を設定
gcloud auth configure-docker asia-northeast1-docker.pkg.dev

# イメージをプッシュ
docker push asia-northeast1-docker.pkg.dev/$PROJECT_ID/ai-manager-repo/ai-manager-app:latest
```

## ステップ5: Cloud Runにデプロイ

```powershell
gcloud run deploy ai-manager-app `
  --image asia-northeast1-docker.pkg.dev/$PROJECT_ID/ai-manager-repo/ai-manager-app:latest `
  --platform managed `
  --region asia-northeast1 `
  --allow-unauthenticated `
  --port 8501 `
  --memory 2Gi `
  --cpu 2 `
  --timeout 300 `
  --env-vars-file .env.yaml
```

## ステップ6: デプロイ完了

デプロイが成功すると、URLが表示されます：
```
Service [ai-manager-app] revision [ai-manager-app-00001-xxx] has been deployed and is serving 100 percent of traffic.
Service URL: https://ai-manager-app-xxxxxxxxxx-an.a.run.app
```

このURLにアクセスすれば、どこからでもアプリが使えます！

## 料金について

Google Cloud Runの無料枠：
- 月200万リクエスト
- 月360,000 vCPU秒
- 月180,000 GiB秒のメモリ

通常の社内利用であれば、**無料枠内で十分です**。

## トラブルシューティング

### エラー: "Permission denied"
```powershell
gcloud auth login
gcloud config set project $PROJECT_ID
```

### エラー: "Service account does not have permission"
```powershell
# サービスアカウントに権限を付与
gcloud projects add-iam-policy-binding $PROJECT_ID `
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" `
  --role="roles/run.admin"
```

### ログの確認
```powershell
gcloud run logs read ai-manager-app --region asia-northeast1
```

## 更新方法

コードを変更した後：

```powershell
# 1. Gitにプッシュ
git add .
git commit -m "Update application"
git push origin main

# 2. 再ビルド＆プッシュ
docker build -t asia-northeast1-docker.pkg.dev/$PROJECT_ID/ai-manager-repo/ai-manager-app:latest .
docker push asia-northeast1-docker.pkg.dev/$PROJECT_ID/ai-manager-repo/ai-manager-app:latest

# 3. 再デプロイ
gcloud run deploy ai-manager-app `
  --image asia-northeast1-docker.pkg.dev/$PROJECT_ID/ai-manager-repo/ai-manager-app:latest `
  --platform managed `
  --region asia-northeast1
```

自動的に新しいバージョンがデプロイされます！

