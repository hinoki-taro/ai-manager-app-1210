# OpenAI版への切り替えガイド

株式会社エムエムインターナショナル 社内情報検索AIアプリを、Google GeminiからOpenAIへ切り替える方法を説明します。

---

## 📋 概要

### 現在のバージョン（デフォルト）
- **LLM:** Google Gemini (`gemini-1.5-flash`)
- **埋め込みモデル:** Google Generative AI Embeddings
- **APIキー:** `GOOGLE_API_KEY`

### OpenAI版
- **LLM:** OpenAI GPT (`gpt-4o-mini`)
- **埋め込みモデル:** OpenAI Embeddings (`text-embedding-3-small`)
- **APIキー:** `OPENAI_API_KEY`

---

## 🔄 切り替え手順

### 方法1: ファイルを入れ替える（推奨）

#### ステップ1: バックアップの作成
```bash
# 現在のファイルをバックアップ
copy utils.py utils_gemini_backup.py
copy initialize.py initialize_gemini_backup.py
```

#### ステップ2: OpenAI版のファイルをコピー
```bash
# OpenAI版のファイルをメインディレクトリにコピー
copy openai_version\utils_openai.py utils.py
copy openai_version\initialize_openai.py initialize.py
```

#### ステップ3: 依存パッケージのインストール
```bash
# 仮想環境をアクティベート
env\Scripts\activate.bat

# OpenAI用のパッケージをインストール
pip install langchain-openai==0.2.14
```

#### ステップ4: APIキーの設定
`.env` ファイルを編集：
```env
# Google Gemini APIキー（コメントアウト）
# GOOGLE_API_KEY=your_google_api_key

# OpenAI APIキー
OPENAI_API_KEY=your_openai_api_key_here
```

#### ステップ5: アプリを起動
```bash
streamlit run main.py
```

---

### 方法2: 環境変数で切り替える

#### ステップ1: `.env` に両方のAPIキーを設定
```env
# Google Gemini APIキー
GOOGLE_API_KEY=your_google_api_key

# OpenAI APIキー
OPENAI_API_KEY=your_openai_api_key
```

#### ステップ2: `constants.py` で切り替え
`constants.py` の `MODEL` を変更：
```python
# Google Gemini を使用（デフォルト）
MODEL = "gemini-1.5-flash"

# または OpenAI を使用
# MODEL = MODEL_OPENAI  # "gpt-4o-mini"
```

#### ステップ3: 対応するファイルを使用
- Google Gemini を使用する場合: `utils.py`, `initialize.py`（現在のファイル）
- OpenAI を使用する場合: `utils_openai.py`, `initialize_openai.py`（`openai_version/`フォルダ内）

---

## 💰 コスト比較

### Google Gemini（無料枠あり）
- **無料枠:** 1日1,500リクエスト、月間150万トークン
- **制限:** Embedding APIは無料枠が制限的
- **コスト:** 無料枠内なら0円

### OpenAI（従量課金）
- **GPT-4o-mini:**
  - 入力: $0.150 / 1Mトークン
  - 出力: $0.600 / 1Mトークン
- **text-embedding-3-small:**
  - $0.020 / 1Mトークン
- **推定コスト（月間1,000質問）:** 約$5〜$10

---

## 🔑 OpenAI APIキーの取得方法

### ステップ1: OpenAIアカウントの作成
1. https://platform.openai.com/ にアクセス
2. 「Sign up」をクリック
3. メールアドレスで登録

### ステップ2: APIキーの作成
1. https://platform.openai.com/api-keys にアクセス
2. 「Create new secret key」をクリック
3. 名前を入力（例: `社内情報検索AI`）
4. APIキーをコピー（**一度しか表示されません！**）

### ステップ3: 使用量の上限設定（推奨）
1. https://platform.openai.com/account/limits にアクセス
2. 「Usage limits」で月間の上限を設定（例: $20）
3. これにより予期しない高額請求を防げます

---

## 📊 どちらを選ぶべきか？

### Google Gemini を選ぶ場合
✅ 無料で使いたい  
✅ 質問数が少ない（1日1,500回以下）  
✅ コストを最小限にしたい  

### OpenAI を選ぶ場合
✅ より高品質な回答が欲しい  
✅ 質問数が多い（1日1,500回以上）  
✅ Embedding APIも制限なく使いたい  
✅ 少額の費用は問題ない  

---

## 🔧 トラブルシューティング

### エラー: `No module named 'langchain_openai'`
**解決法:**
```bash
pip install langchain-openai==0.2.14
```

### エラー: `You didn't provide an API key`
**解決法:**
1. `.env` ファイルに `OPENAI_API_KEY` が設定されているか確認
2. アプリを再起動

### エラー: `You exceeded your current quota`
**解決法:**
1. OpenAIの使用量を確認: https://platform.openai.com/usage
2. クレジットカードを登録（無料枠を超えた場合）
3. 使用量の上限を設定

### 回答が生成されない
**解決法:**
1. `logs/langchain_log.json` でエラーを確認
2. APIキーが正しいか確認
3. インターネット接続を確認

---

## 🔄 Gemini版に戻す方法

### 方法1: バックアップから復元
```bash
# バックアップファイルから復元
copy utils_gemini_backup.py utils.py
copy initialize_gemini_backup.py initialize.py
```

### 方法2: Gitから復元
```bash
# 最新のコミットから復元
git checkout utils.py initialize.py
```

### APIキーを戻す
`.env` ファイルを編集：
```env
# Google Gemini APIキー
GOOGLE_API_KEY=your_google_api_key

# OpenAI APIキー（コメントアウト）
# OPENAI_API_KEY=your_openai_api_key
```

---

## 📁 OpenAI版のファイル一覧

### `openai_version/` フォルダ内
- `utils_openai.py` - OpenAI版のユーティリティ関数
- `initialize_openai.py` - OpenAI版の初期化処理
- `requirements_openai.txt` - OpenAI用の依存パッケージ
- `.env.openai.template` - OpenAI用の環境変数テンプレート
- `README_OPENAI.md` - このファイル
- `SWITCH_GUIDE.md` - 詳細な切り替えガイド

---

## 🚀 推奨事項

### 開発・テスト環境
- **Google Gemini** を使用（無料）
- コストをかけずに機能を開発

### 本番環境
- **OpenAI** を使用（有料だが安定）
- より高品質な回答
- 制限が少ない

### ハイブリッド構成
- **Gemini:** 通常の質問
- **OpenAI:** 重要な質問や複雑な質問
- 環境変数で切り替え可能に設定

---

## 📞 サポート

質問やトラブルがあれば：
- **メール:** ai-support@mm-international.co.jp
- **詳細ガイド:** `SWITCH_GUIDE.md`

---

*最終更新：2025年12月13日*  
*株式会社エムエムインターナショナル*

