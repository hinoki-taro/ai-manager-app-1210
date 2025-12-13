# 社内情報特化型生成AI検索アプリ

社内文書を検索・問い合わせできるRAG（Retrieval-Augmented Generation）ベースのStreamlitアプリケーションです。

## 機能

- **社内文書検索モード**: 入力内容と関連性が高い社内文書を検索
- **社内問い合わせモード**: 質問に対してAIが回答を生成し、参照文書を表示

## 技術スタック

- **フレームワーク**: Streamlit
- **LLM**: Google Gemini（無料版: gemini-1.5-flash）
- **ベクターストア**: ChromaDB
- **ドキュメント処理**: LangChain
- **対応ファイル形式**: PDF, DOCX, CSV, TXT

## ローカル環境でのセットアップ

### 前提条件

- Python 3.9以上
- Google Gemini APIキー（無料で取得可能）

### インストール手順

1. **リポジトリのクローン**

```bash
git clone <repository-url>
cd 社内情報特化型生成AI検索アプリ
```

2. **仮想環境の作成と有効化**

```bash
# Windows
python -m venv env
env\Scripts\activate

# Mac/Linux
python3 -m venv env
source env/bin/activate
```

3. **依存パッケージのインストール**

```bash
# Windows
pip install -r requirements_windows.txt

# Mac
pip install -r requirements_mac.txt

# または汎用版
pip install -r requirements.txt
```

4. **環境変数の設定**

`env.template` をコピーして `.env` ファイルを作成し、Google Gemini APIキーを設定します。

```bash
# Windowsの場合
copy env.template .env

# Mac/Linuxの場合
cp env.template .env
```

`.env` ファイルを編集して、実際のAPIキーを設定してください：

```
GOOGLE_API_KEY=your-actual-google-gemini-api-key-here
```

5. **データの配置**

`data/` ディレクトリに検索対象の文書を配置します。以下の構造を推奨：

```
data/
├── MTG議事録/
├── サービスについて/
├── 会社について/
└── 顧客について/
```

6. **アプリケーションの起動**

```bash
streamlit run main.py
```

ブラウザで `http://localhost:8501` が自動的に開きます。

## WEBへのデプロイ（Streamlit Community Cloud）

### 準備

1. **GitHubリポジトリの作成**
   - GitHubで新しいリポジトリを作成
   - ローカルのコードをプッシュ

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

⚠️ **重要**: `.gitignore` により、以下のファイル/ディレクトリはGitにコミットされません：
- `.env` (APIキー)
- `data/` (社内文書)
- `.streamlit/secrets.toml` (機密情報)
- `logs/` (ログファイル)

### Streamlit Community Cloudでのデプロイ

1. **Streamlit Community Cloudにアクセス**
   - https://streamlit.io/cloud にアクセス
   - GitHubアカウントでサインイン

2. **新しいアプリをデプロイ**
   - "New app" をクリック
   - リポジトリ、ブランチ、メインファイル（`main.py`）を選択
   - "Advanced settings" をクリック

3. **環境変数（Secrets）の設定**
   
   "Secrets" セクションに以下を入力：

```toml
OPENAI_API_KEY = "sk-your-actual-api-key-here"
```

4. **データファイルのアップロード**

   社内文書は機密情報のため、以下のいずれかの方法で対応：

   **方法A: プライベートリポジトリを使用**
   - GitHubリポジトリをプライベートに設定
   - `data/` ディレクトリをコミット（この場合、`.gitignore`から`data/`を削除）

   **方法B: 外部ストレージを使用**
   - AWS S3、Google Cloud Storage等に文書を保存
   - アプリ起動時にダウンロードするコードを追加

   **方法C: 小規模データの場合**
   - Streamlit Cloudのファイルアップロード機能を使用（非推奨：大量のファイルには不向き）

5. **デプロイ実行**
   - "Deploy!" をクリック
   - ビルドとデプロイが完了するまで待機（数分かかります）

6. **アプリケーションの確認**
   - デプロイ完了後、URLが発行されます（例: `https://your-app-name.streamlit.app`）
   - アクセスして動作を確認

### セキュリティ設定

デプロイ後、以下のセキュリティ設定を推奨します：

1. **アクセス制限**
   - Streamlit Community Cloudの設定で、特定のメールドメインのみアクセス可能に設定
   - または、アプリ内で認証機能を実装

2. **HTTPS通信**
   - Streamlit Cloudは自動的にHTTPSを有効化

3. **APIキーの管理**
   - Google Gemini APIキーの使用量を定期的に監視
   - 必要に応じて使用制限を設定（無料枠：1分あたり15リクエスト、1日1500リクエスト）

## その他のデプロイオプション

### Azure App Service

```bash
# requirements.txtを使用
az webapp up --name your-app-name --runtime "PYTHON:3.9"
```

### Google Cloud Run

```bash
# Dockerfileを作成してデプロイ
gcloud run deploy --source .
```

### AWS EC2 / Lightsail

```bash
# EC2インスタンスでStreamlitを起動
streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```

## トラブルシューティング

### ローカル環境

**問題**: `ModuleNotFoundError`が発生する
- **解決**: 仮想環境が有効化されているか確認し、`pip install -r requirements.txt`を再実行

**問題**: Google Gemini APIエラー
- **解決**: `.env`ファイルのAPIキーが正しいか確認（https://aistudio.google.com/app/apikey で取得）

**問題**: 文字化けが発生する
- **解決**: Windowsの場合、`initialize.py`の`adjust_string`関数が自動的に対応します

### デプロイ環境

**問題**: アプリが起動しない
- **解決**: Streamlit Cloudのログを確認し、依存パッケージのバージョンを確認

**問題**: データが読み込めない
- **解決**: `data/`ディレクトリが正しく配置されているか確認

**問題**: APIキーエラー
- **解決**: Streamlit Cloudの"Secrets"設定を確認

## ライセンス

社内利用限定

## サポート

問題が発生した場合は、開発チームまでお問い合わせください。

