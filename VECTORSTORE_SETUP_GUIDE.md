# ベクターストア事前作成ガイド

Google Gemini APIの無料枠クォータ問題を解決するため、ローカルでベクターストアを事前作成してデプロイします。

---

## 📋 概要

### 問題
- Streamlit Cloud上でアプリを起動するたびに、218個のチャンクに対して埋め込みAPIを呼び出す
- Google Gemini APIの無料枠では、埋め込みAPIのクォータが非常に少ない（limit: 0）
- 毎回起動時にクォータを超過してしまう

### 解決策
- **ローカルで一度だけ**ベクターストアを作成
- 作成したベクターストアをGitHubにコミット
- Streamlit Cloud上では既存のベクターストアを読み込むだけ（埋め込みAPIを呼ばない）

---

## 🚀 実行手順

### ステップ1: .envファイルの確認

プロジェクトのルートディレクトリに `.env` ファイルがあることを確認してください。

**`.env` の内容:**
```
GOOGLE_API_KEY=AIzaSyBlp0GgqOrY5VLVP703PKk-J1UKuDHuhKQ
```

**ファイルがない場合:**
1. プロジェクトのルートディレクトリに `.env` という名前のファイルを作成
2. 上記の内容を記述して保存

---

### ステップ2: ベクターストアを作成

Cursorのターミナルで以下のコマンドを実行してください：

```bash
python create_vectorstore_local.py
```

**所要時間:** 約5-10分（データ量によります）

**実行中の表示:**
```
============================================================
ベクターストア作成スクリプト
============================================================

🔄 データを読み込んでいます...
✓ 67個のドキュメントを読み込みました

🔄 テキストを正規化しています...
✓ テキストの正規化が完了しました

🔄 埋め込みモデルを初期化しています...
✓ APIキーを取得しました（先頭10文字: AIzaSyBlp0...）
✓ 埋め込みモデルの初期化が完了しました

🔄 ドキュメントを分割しています...
✓ 218個のチャンクに分割しました

🔄 ベクターストアを作成しています（これには数分かかる場合があります）...
⚠️ この処理中にGemini APIのクォータを消費します
✓ ベクターストアの作成が完了しました
✓ ベクターストアを保存しました: ./vectorstore/

============================================================
✅ 完了！
============================================================
```

---

### ステップ3: 作成されたファイルを確認

プロジェクトのルートに `vectorstore/` フォルダが作成されたことを確認してください。

```
社内情報特化型生成AI検索アプリ/
├── vectorstore/              ← 新しく作成される
│   ├── chroma.sqlite3
│   └── [その他のファイル]
├── create_vectorstore_local.py
├── initialize.py
└── ...
```

---

### ステップ4: GitHubにプッシュ

Cursorのターミナルで以下のコマンドを実行してください：

```bash
git add vectorstore/
git add initialize.py
git add create_vectorstore_local.py
git add VECTORSTORE_SETUP_GUIDE.md
git commit -m "Add pre-built vectorstore to avoid API quota issues"
git push origin main
```

---

### ステップ5: Streamlit Cloudで再起動

1. https://share.streamlit.io/ にアクセス
2. `mmi-ai-manager` を選択
3. 左メニューの **「Reboot app」** をクリック
4. 確認ダイアログで **「Reboot app」** をクリック

---

## ✅ 成功時の表示

Streamlit Cloud上でアプリが起動すると、以下のように表示されます：

```
🔄 事前作成されたベクターストアを読み込んでいます...
✓ ベクターストアの読み込みが完了しました
✅ 初期化が正常に完了しました！
```

**重要なポイント:**
- ✅ 「事前作成されたベクターストアを読み込んでいます」と表示される
- ✅ 「データを読み込んでいます」「分割しています」などは表示されない
- ✅ 初期化が**数秒で完了**する（以前は数分かかっていた）
- ✅ APIクォータエラーが発生しない

---

## 🔧 トラブルシューティング

### エラー1: `GOOGLE_API_KEY が設定されていません`

**原因:** `.env` ファイルが存在しない、または内容が正しくない

**対処:**
1. プロジェクトのルートに `.env` ファイルを作成
2. 以下を記述:
   ```
   GOOGLE_API_KEY=AIzaSyBlp0GgqOrY5VLVP703PKk-J1UKuDHuhKQ
   ```
3. 保存して再実行

---

### エラー2: `429 You exceeded your current quota`

**原因:** Google Gemini APIの無料枠クォータを超過

**対処:**

#### オプションA: 24時間待つ
無料枠は24時間でリセットされます。明日再実行してください。

#### オプションB: OpenAI APIに切り替える（推奨）
1. OpenAI APIキーを用意
2. `.env` を以下に変更:
   ```
   OPENAI_API_KEY=sk-proj-...
   ```
3. 以下のコマンドを実行:
   ```bash
   cd openai_version
   python create_vectorstore_local_openai.py
   ```

---

### エラー3: `ModuleNotFoundError: No module named 'XXX'`

**原因:** 必要なパッケージがインストールされていない

**対処:**
```bash
pip install -r requirements.txt
```

---

### エラー4: Streamlit Cloudで `ベクターストアが見つかりません`

**原因:** `vectorstore/` フォルダがGitHubにプッシュされていない

**対処:**
1. ローカルで `vectorstore/` フォルダが存在することを確認
2. 以下のコマンドを実行:
   ```bash
   git add vectorstore/
   git commit -m "Add vectorstore"
   git push origin main
   ```
3. Streamlit Cloudで再起動

---

## 📊 データ更新時の手順

データ（`data/` フォルダ）を更新した場合は、ベクターストアも再作成する必要があります。

### 手順
1. データを更新（ファイルの追加・削除・編集）
2. `python create_vectorstore_local.py` を実行
3. GitHubにプッシュ:
   ```bash
   git add data/
   git add vectorstore/
   git commit -m "Update data and vectorstore"
   git push origin main
   ```
4. Streamlit Cloudで再起動

---

## 💡 メリット

### 1. APIクォータ問題の解決
- 起動時に埋め込みAPIを呼ばないので、クォータエラーが発生しない
- 無料枠で安定して動作

### 2. 高速起動
- 以前: 数分かかっていた（218回の埋め込みAPI呼び出し）
- 現在: 数秒で完了（既存のベクターストアを読み込むだけ）

### 3. コスト削減
- 毎回の起動でAPIを呼ばないので、有料APIに切り替えた場合もコスト削減

---

## ⚠️ 注意事項

1. **ローカルでの初回作成時のみ、APIクォータを消費します**
   - 218個のチャンク × 1回 = 218回のAPI呼び出し
   - これは1回だけなので、無料枠で対応可能（24時間でリセット）

2. **`vectorstore/` フォルダはGitHubにコミットする**
   - `.gitignore` で除外しない
   - サイズは約10-50MB程度

3. **データを更新したら、ベクターストアも再作成する**
   - そうしないと、古いデータのままになる

---

## 📞 サポート

問題が解決しない場合は、以下を確認してください：
- `.env` ファイルが正しく設定されているか
- `vectorstore/` フォルダが作成されているか
- GitHubに正しくプッシュされているか
- Streamlit Cloudで再起動したか

---

**作成日:** 2025年12月13日  
**対象:** 株式会社エムエムインターナショナル  
**アプリ名:** mmi-ai-manager



