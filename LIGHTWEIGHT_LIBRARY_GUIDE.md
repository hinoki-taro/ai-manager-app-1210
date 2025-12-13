# 軽量ライブラリセット完全ガイド

株式会社エムエムインターナショナル 社内情報検索AIアプリ用の軽量で効率的なライブラリガイドです。

---

## 🎯 コンセプト

**「必要な機能を、最小限の重さで」**

- 各セット約25-100MB
- 起動時間への影響は最小限（+0.5〜3秒）
- 必要なものだけを選択してインストール
- 合計200以上の軽量ライブラリを10のセットに分類

---

## 📦 10の軽量ライブラリセット

### セット01: 高速テキスト処理 ⚡
**サイズ:** 約50MB | **影響:** +1-2秒

#### 含まれるライブラリ
- `orjson`, `ujson` - 高速JSON処理（標準の5-10倍）
- `ruamel.yaml` - 高速YAML処理
- `python-Levenshtein` - テキスト類似度計算
- `ftfy` - テキスト修正・正規化

#### できること
```python
import orjson

# 標準jsonより5-10倍高速
data = orjson.loads(json_string)
result = orjson.dumps(data)

# テキスト類似度
from Levenshtein import ratio
similarity = ratio("会社情報", "会社概要")  # 0.67
```

---

### セット02: 効率的なデータ処理 💾
**サイズ:** 約40MB | **影響:** +1秒

#### 含まれるライブラリ
- `polars` - Pandasより高速なデータフレーム
- `pyarrow` - 高速配列処理
- `tinydb` - 軽量JSONデータベース
- `diskcache` - ディスクキャッシュ

#### できること
```python
import polars as pl

# Pandasより高速
df = pl.read_csv("large_file.csv")
result = df.filter(pl.col("status") == "active")

# 軽量データベース
from tinydb import TinyDB
db = TinyDB('db.json')
db.insert({'name': '株式会社エムエムインターナショナル'})
```

---

### セット03: 日本語特化処理 🇯🇵 ★人気
**サイズ:** 約100MB | **影響:** +2-3秒

#### 含まれるライブラリ
- `janome` - 軽量日本語形態素解析
- `sudachipy` - 高精度日本語解析
- `mojimoji` - 全角半角変換
- `neologdn` - 日本語正規化
- `pykakasi` - ひらがな・カタカナ変換

#### できること
```python
from janome.tokenizer import Tokenizer

# 日本語形態素解析
t = Tokenizer()
tokens = t.tokenize("株式会社エムエムインターナショナル")

# 全角半角変換
import mojimoji
text = mojimoji.zen_to_han("１２３ＡＢＣ")  # "123ABC"

# ひらがな変換
import pykakasi
kks = pykakasi.kakasi()
result = kks.convert("株式会社")  # かぶしきがいしゃ
```

---

### セット04: Webスクレイピング強化 🌐
**サイズ:** 約60MB | **影響:** +1-2秒

#### 含まれるライブラリ
- `httpx` - 高速非同期HTTPクライアント
- `selectolax` - 高速HTMLパーサー
- `feedparser` - RSSフィード処理
- `fake-useragent` - User-Agent生成

#### できること
```python
import httpx

# 非同期リクエスト
async with httpx.AsyncClient() as client:
    response = await client.get('https://example.com')

# 高速HTMLパーサー
from selectolax.parser import HTMLParser
tree = HTMLParser(html)
title = tree.css_first('title').text()
```

---

### セット05: APIクライアント 🔌
**サイズ:** 約30MB | **影響:** +1秒

#### 含まれるライブラリ
- `slack-bolt` - Slack API
- `line-bot-sdk` - LINE API
- `notion-client` - Notion API
- `PyGithub` - GitHub API

#### できること
```python
from slack_sdk import WebClient

# Slack通知
client = WebClient(token="xoxb-...")
client.chat_postMessage(
    channel="#general",
    text="検索システムが起動しました"
)

# Notion連携
from notion_client import Client
notion = Client(auth="secret_...")
results = notion.databases.query(database_id="...")
```

---

### セット06: ファイル処理特化 📁
**サイズ:** 約40MB | **影響:** +1秒

#### 含まれるライブラリ
- `filetype` - ファイル形式判定
- `py7zr` - 7zip処理
- `watchfiles` - ファイル監視（軽量）
- `chardet` - 文字コード判定

#### できること
```python
import filetype

# ファイル形式を自動判定
kind = filetype.guess('document.pdf')
print(kind.mime)  # 'application/pdf'

# 文字コード判定
import chardet
result = chardet.detect(byte_str)
print(result['encoding'])  # 'utf-8'
```

---

### セット07: パフォーマンス最適化 🚀
**サイズ:** 約35MB | **影響:** +1秒

#### 含まれるライブラリ
- `joblib` - 並列処理
- `aiofiles` - 非同期ファイルIO
- `more-itertools` - 高速イテレーション
- `lru-dict` - 高速LRUキャッシュ

#### できること
```python
from joblib import Parallel, delayed

# 並列処理
results = Parallel(n_jobs=4)(
    delayed(process_file)(f) for f in files
)

# 非同期ファイル読み込み
import aiofiles
async with aiofiles.open('file.txt', 'r') as f:
    content = await f.read()
```

---

### セット08: ユーティリティ強化 🛠️
**サイズ:** 約25MB | **影響:** +0.5秒

#### 含まれるライブラリ
- `rich` - 美しいターミナル出力
- `pendulum` - 日時処理
- `typer` - CLIツール作成
- `validators` - データ検証

#### できること
```python
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="検索統計")
table.add_column("質問", style="cyan")
table.add_column("回数", style="magenta")
console.print(table)

# 日時処理
import pendulum
now = pendulum.now('Asia/Tokyo')
tomorrow = now.add(days=1)
```

---

### セット09: エンタープライズ対応 🏢
**サイズ:** 約45MB | **影響:** +1秒

#### 含まれるライブラリ
- `authlib` - OAuth認証
- `casbin` - アクセス制御
- `ratelimit` - レート制限（軽量）
- `tenacity` - リトライロジック

#### できること
```python
from ratelimit import limits, sleep_and_retry

# レート制限
@sleep_and_retry
@limits(calls=10, period=60)
def call_api():
    # 1分間に10回まで
    pass

# リトライロジック
from tenacity import retry, stop_after_attempt
@retry(stop=stop_after_attempt(3))
def unreliable_function():
    # 3回まで自動リトライ
    pass
```

---

### セット10: 開発者ツール 👨‍💻
**サイズ:** 約30MB | **影響:** +1秒

#### 含まれるライブラリ
- `icecream` - デバッグ支援
- `py-spy` - プロファイリング
- `pdoc` - ドキュメント生成
- `pipdeptree` - 依存関係可視化

#### できること
```python
from icecream import ic

# デバッグ出力（printより便利）
ic(variable)  # ic| variable: 'value'

# 依存関係チェック
# コマンドライン:
# pipdeptree
```

---

## 🎯 推奨インストールプラン

### プラン1: 最小限（現在）
```
既存の requirements.txt のみ
```
**サイズ:** 約500MB  
**機能:** 基本的な検索機能

### プラン2: 日本語強化 ⭐推奨
```bash
# セット03のみ
pip install -r requirements_lightweight_03.txt
```
**追加サイズ:** +100MB  
**追加機能:** 高度な日本語処理

### プラン3: 推奨セット ⭐⭐推奨
```bash
# セット1,3,7,8
install_lightweight.bat
# → 「12. 推奨セット」を選択
```
**追加サイズ:** +210MB  
**追加機能:**
- 高速テキスト処理
- 日本語特化処理
- パフォーマンス最適化
- ユーティリティ

### プラン4: フル機能
```bash
# 全セット
install_lightweight.bat
# → 「11. すべてインストール」を選択
```
**追加サイズ:** +455MB  
**追加機能:** すべて

---

## 🚀 インストール方法

### 対話式インストール（推奨）

```bash
# ダブルクリック
install_lightweight.bat
```

**メニューが表示されます：**
```
 1. 高速テキスト処理（約50MB）
 2. 効率的なデータ処理（約40MB）
 3. 日本語特化処理（約100MB）★人気
 4. Webスクレイピング強化（約60MB）
 5. APIクライアント（約30MB）
 6. ファイル処理特化（約40MB）
 7. パフォーマンス最適化（約35MB）
 8. ユーティリティ強化（約25MB）
 9. エンタープライズ対応（約45MB）
10. 開発者ツール（約30MB）
11. すべてインストール（約455MB）
12. 推奨セット（1,3,7,8のみ 約210MB）★おすすめ
```

### 個別インストール

```bash
# セット03（日本語処理）だけインストール
pip install -r requirements_lightweight_03.txt
```

---

## 💡 使用例

### 例1: 日本語形態素解析で検索精度向上

```python
from janome.tokenizer import Tokenizer

t = Tokenizer()

def extract_keywords(text):
    """日本語テキストからキーワードを抽出"""
    tokens = t.tokenize(text, wakati=True)
    # 名詞のみ抽出
    keywords = [token for token in tokens 
                if token.part_of_speech.startswith('名詞')]
    return keywords

# 検索クエリから重要キーワードを抽出
keywords = extract_keywords("JINNYの導入台数について教えて")
# → ['JINNY', '導入', '台数']
```

### 例2: 高速JSONでログ処理

```python
import orjson

# 標準jsonより5-10倍高速
def save_log_fast(log_data):
    with open('log.json', 'wb') as f:
        f.write(orjson.dumps(log_data))

def load_log_fast():
    with open('log.json', 'rb') as f:
        return orjson.loads(f.read())
```

### 例3: 並列処理で初期化高速化

```python
from joblib import Parallel, delayed

def process_file(file_path):
    # ファイル処理
    return load_and_process(file_path)

# 並列処理で高速化
files = ['file1.pdf', 'file2.pdf', 'file3.pdf']
results = Parallel(n_jobs=4)(
    delayed(process_file)(f) for f in files
)
```

---

## 📊 パフォーマンス比較

### 標準 vs 軽量ライブラリ

| タスク | 標準ライブラリ | 軽量ライブラリ | 速度向上 |
|--------|--------------|--------------|----------|
| JSON処理 | `json` | `orjson` | **5-10倍** |
| データ処理 | `pandas` | `polars` | **2-5倍** |
| HTML解析 | `BeautifulSoup` | `selectolax` | **10-20倍** |
| 並列処理 | `multiprocessing` | `joblib` | **1.5-2倍** |

---

## ⚖️ サイズとパフォーマンスのバランス

### 既存（requirements.txt）
- **サイズ:** 約500MB
- **起動時間:** 10-15秒
- **メモリ:** 約300MB

### +推奨セット
- **サイズ:** 約710MB（+210MB）
- **起動時間:** 12-18秒（+2-3秒）
- **メモリ:** 約400MB（+100MB）
- **パフォーマンス:** 2-5倍高速化

### +全セット
- **サイズ:** 約955MB（+455MB）
- **起動時間:** 15-20秒（+5秒）
- **メモリ:** 約500MB（+200MB）
- **パフォーマンス:** 5-10倍高速化

---

## 🎯 機能別推奨セット

| やりたいこと | 推奨セット | サイズ |
|-------------|-----------|--------|
| 日本語処理を強化 | 03 | +100MB |
| 処理を高速化 | 01, 07 | +85MB |
| Web連携 | 04, 05 | +90MB |
| ファイル処理強化 | 06 | +40MB |
| 開発効率化 | 08, 10 | +55MB |
| エンタープライズ | 09 | +45MB |

---

## 🔧 トラブルシューティング

### インストールエラー
```bash
# キャッシュをクリアして再試行
pip cache purge
pip install -r requirements_lightweight_03.txt
```

### 依存関係の競合
```bash
# 仮想環境を再作成
rmdir /s env
python -m venv env
env\Scripts\activate.bat
pip install -r requirements.txt
pip install -r requirements_lightweight_03.txt
```

---

## 📞 サポート

- **メール:** ai-support@mm-international.co.jp
- **関連ファイル:**
  - `requirements_lightweight_01.txt` 〜 `10.txt`
  - `install_lightweight.bat`

---

*最終更新：2025年12月13日*  
*株式会社エムエムインターナショナル*

