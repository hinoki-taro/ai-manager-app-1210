# ✅ セットアップチェックリスト

このチェックリストに従って、アプリをセットアップしてください。

---

## 📝 事前準備

- [ ] Googleアカウントを持っている（Gmail等）
- [ ] Python 3.9以上がインストールされている
- [ ] 仮想環境（env）が作成されている

---

## 🔑 ステップ1: Google Gemini APIキーを取得

- [ ] https://aistudio.google.com/app/apikey にアクセス
- [ ] Googleアカウントでログイン
- [ ] "Create API Key" をクリック
- [ ] "Create API key in new project" を選択
- [ ] 表示されたAPIキーをコピー（例: `AIzaSyD...`）
- [ ] APIキーを安全な場所にメモ

**所要時間: 約1分**

---

## 🔧 ステップ2: 環境変数ファイルを作成

プロジェクトのルートディレクトリに `.env` ファイルを作成：

### 方法1: 手動で作成（推奨）

1. エディタで新しいファイルを作成
2. ファイル名を `.env` に設定
3. 以下の内容を記述：

```
GOOGLE_API_KEY=ここに取得したAPIキーを貼り付け
```

4. 保存

### 方法2: コマンドで作成

**Windows (コマンドプロンプト):**
```cmd
echo GOOGLE_API_KEY=your-api-key-here > .env
```

**Mac/Linux (ターミナル):**
```bash
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

- [ ] `.env` ファイルが作成された
- [ ] ファイル内に `GOOGLE_API_KEY=...` が記述されている
- [ ] 実際のAPIキーが正しく貼り付けられている（余分なスペースなし）

---

## 📦 ステップ3: 依存パッケージをインストール

### 3-1: 仮想環境を有効化

**⚠️ Windows重要: コマンドプロンプト（cmd）を使用してください**

フォルダ名に日本語が含まれている場合、PowerShellではエラーが発生します。
必ず**コマンドプロンプト（cmd）**を使用してください。

**コマンドプロンプトの開き方:**
1. Windowsキー + R を押す
2. `cmd` と入力してEnter
3. プロジェクトフォルダに移動:
   ```cmd
   cd C:\Users\mtokyo081\Desktop\cursor\社内情報特化型生成AI検索アプリ
   ```

**Windows (コマンドプロンプト):**
```cmd
env\Scripts\activate
```

**Mac/Linux (ターミナル):**
```bash
source env/bin/activate
```

- [ ] コマンドプロンプトの先頭に `(env)` が表示された

**トラブルシューティング:**
- PowerShellで「認識されていません」エラーが出る場合 → cmd（コマンドプロンプト）を使う
- 「activate が見つかりません」エラーが出る場合 → 方法2（仮想環境なし）を試す

### 3-2: パッケージをインストール

**方法A: 仮想環境を使う場合（推奨）**

```bash
pip install -r requirements.txt
```

**方法B: 仮想環境が使えない場合（代替案）**

仮想環境の有効化がどうしてもできない場合は、グローバルにインストール：

```bash
python -m pip install -r requirements.txt
```

または、仮想環境のPythonを直接指定：

```bash
env\Scripts\python.exe -m pip install -r requirements.txt
```

- [ ] インストールが完了した（エラーなし）
- [ ] `langchain-google-genai` がインストールされた
- [ ] `google-generativeai` がインストールされた

**所要時間: 2〜5分**

---

## 🚀 ステップ4: アプリを起動

**方法A: 仮想環境を有効化している場合**

```bash
streamlit run main.py
```

**方法B: 仮想環境を有効化していない場合**

```bash
python -m streamlit run main.py
```

または

```bash
env\Scripts\python.exe -m streamlit run main.py
```

- [ ] コマンドを実行した
- [ ] ブラウザで `http://localhost:8501` が自動的に開いた
- [ ] アプリの画面が表示された

**初回起動時は1〜2分かかります（データの読み込みとベクトル化）**

---

## ✅ ステップ5: 動作確認

### テスト1: 社内文書検索モード

1. 左サイドバーで「社内文書検索」を選択
2. チャット欄に入力: `会社概要について`
3. 送信

- [ ] 関連するファイルパスが表示された
- [ ] エラーが表示されていない

### テスト2: 社内問い合わせモード

1. 左サイドバーで「社内問い合わせ」を選択
2. チャット欄に入力: `EcoTeeのサービス内容を教えて`
3. 送信

- [ ] AIからの回答が表示された
- [ ] 情報源（ファイルパス）が表示された
- [ ] エラーが表示されていない

### テスト3: 処理中の入力制御

1. 質問を送信
2. 回答生成中に、すぐに別の質問を送信しようとする

- [ ] チャット入力欄が無効化された（グレーアウト）
- [ ] 「現在、回答を生成中です...」というメッセージが表示された
- [ ] 回答完了後、自動的に入力欄が有効化された

---

## 🎉 セットアップ完了！

すべてのチェックが完了したら、アプリを自由に使ってください。

---

## ⚠️ エラーが出た場合

### エラー0: `'env\Scripts\activate' は認識されていません`（Windows PowerShell）

**症状:**
```
'env\Scripts\activate' は、内部コマンドまたは外部コマンド、
操作可能なプログラムまたはバッチ ファイルとして認識されていません。
```

**原因:**
- PowerShellを使っている（日本語パスに対応していない）
- フォルダ名に日本語が含まれている

**解決方法:**
1. **コマンドプロンプト（cmd）を使う（推奨）**
   - Windowsキー + R を押す
   - `cmd` と入力してEnter
   - プロジェクトフォルダに移動して再度試す
   
   ```cmd
   cd C:\Users\mtokyo081\Desktop\cursor\社内情報特化型生成AI検索アプリ
   env\Scripts\activate
   ```

2. **または、仮想環境を使わずに実行**
   ```cmd
   python -m pip install -r requirements.txt
   python -m streamlit run main.py
   ```

---

### エラー1: `GOOGLE_API_KEY が見つかりません`

**症状:**
```
KeyError: 'GOOGLE_API_KEY'
```

**解決方法:**
1. `.env` ファイルがプロジェクトのルートディレクトリに存在するか確認
2. `.env` ファイルを開いて、`GOOGLE_API_KEY=...` が記述されているか確認
3. アプリを再起動（Ctrl+Cで停止 → `streamlit run main.py` で再起動）

---

### エラー2: `ModuleNotFoundError: No module named 'langchain_google_genai'`

**症状:**
```
ModuleNotFoundError: No module named 'langchain_google_genai'
```

**解決方法:**
1. 仮想環境が有効化されているか確認（`(env)` が表示されているか）
2. 以下を実行：
   ```bash
   pip install langchain-google-genai google-generativeai
   ```
3. アプリを再起動

---

### エラー3: `Google API Error: Invalid API Key`

**症状:**
```
google.api_core.exceptions.InvalidArgument: 400 API key not valid
```

**解決方法:**
1. `.env` ファイルのAPIキーを確認
   - 余分なスペースがないか
   - 完全にコピーされているか（途中で切れていないか）
2. Google AI Studioで新しいAPIキーを再発行
3. `.env` ファイルを更新してアプリを再起動

---

### エラー4: `Quota Exceeded (429)`

**症状:**
```
ResourceExhausted: 429 Quota exceeded for quota metric
```

**解決方法:**
- 1分あたりのリクエスト制限（15リクエスト）を超えています
- **1分待ってから**再度試してください
- 質問の頻度を少し下げてください

---

### エラー5: 初期化エラー

**症状:**
```
初期化処理に失敗しました
```

**解決方法:**
1. `data/` ディレクトリにファイルが存在するか確認
2. ログファイル `logs/application.log` を確認してエラー内容を特定
3. 開発チームに問い合わせ（ログファイルを添付）

---

## 📞 サポート

問題が解決しない場合は、以下の情報を添えて開発チームに問い合わせてください：

1. エラーメッセージのスクリーンショット
2. `logs/application.log` の最新のエラーログ
3. 実行したコマンドと手順

---

## 🔐 セキュリティチェック

- [ ] `.env` ファイルが `.gitignore` に含まれている（確認済み）
- [ ] APIキーをGitHubなどに公開していない
- [ ] APIキーをチャットやメールで平文で送信していない

---

## 📚 参考ドキュメント

- **詳細な手順**: `QUICK_START_GEMINI.md`
- **デプロイ方法**: `DEPLOYMENT.md`
- **基本情報**: `README.md`

---

**セットアップお疲れ様でした！楽しいAI体験を！** 🎉


