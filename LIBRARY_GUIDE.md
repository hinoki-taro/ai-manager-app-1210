# 拡張ライブラリガイド

株式会社エムエムインターナショナル 社内情報検索AIアプリで使用可能な拡張ライブラリの完全ガイドです。

---

## 📋 目次

1. [インストール方法](#インストール方法)
2. [ライブラリ一覧](#ライブラリ一覧)
3. [カテゴリ別詳細](#カテゴリ別詳細)
4. [使用例](#使用例)
5. [推奨構成](#推奨構成)

---

## 🚀 インストール方法

### 方法1: 対話式インストール（推奨）

```bash
# バッチスクリプトをダブルクリック
install_extended.bat
```

**選択肢:**
1. すべての拡張ライブラリをインストール（時間がかかる）
2. カテゴリ別にインストール（推奨）
3. 推奨ライブラリのみインストール（軽量）

### 方法2: 一括インストール

```bash
# 仮想環境をアクティベート
env\Scripts\activate.bat

# すべてをインストール
pip install -r requirements_extended.txt
```

### 方法3: 個別インストール

```bash
# 必要なライブラリだけをインストール
pip install python-pptx openpyxl matplotlib
```

---

## 📚 ライブラリ一覧

### 現在使用中（標準）
- `streamlit` - Webアプリフレームワーク
- `langchain` - LLMフレームワーク
- `chromadb` - ベクトルデータベース
- `pandas`, `numpy` - データ処理
- その他（`requirements.txt` 参照）

### 拡張ライブラリ（140+個）
詳細は `requirements_extended.txt` を参照

---

## 📁 カテゴリ別詳細

### 1. ドキュメント処理拡張 📄

#### PowerPoint処理
```python
from pptx import Presentation

# PowerPointファイルの読み込み
prs = Presentation('presentation.pptx')
for slide in prs.slides:
    for shape in slide.shapes:
        if hasattr(shape, "text"):
            print(shape.text)
```

**インストール:**
```bash
pip install python-pptx
```

**用途:**
- PowerPointファイルからテキスト抽出
- スライド内容をRAGのデータソースに追加

#### Excel処理
```python
import openpyxl

# Excelファイルの読み込み
wb = openpyxl.load_workbook('data.xlsx')
ws = wb.active
for row in ws.iter_rows(values_only=True):
    print(row)
```

**インストール:**
```bash
pip install openpyxl xlsxwriter
```

**用途:**
- Excelファイルの読み書き
- データのエクスポート機能
- レポート生成

#### OCR（光学文字認識）
```python
from PIL import Image
import pytesseract

# 画像からテキスト抽出
image = Image.open('document.png')
text = pytesseract.image_to_string(image, lang='jpn')
print(text)
```

**インストール:**
```bash
pip install pytesseract Pillow pdf2image
# Tesseract本体も別途インストールが必要
```

**用途:**
- スキャンされたPDFからテキスト抽出
- 画像ファイルの内容を検索可能にする

---

### 2. データベース接続 🗄️

#### PostgreSQL
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="company_db",
    user="user",
    password="password"
)
```

**用途:**
- 社内データベースとの連携
- ユーザー情報の管理
- 検索履歴の保存

#### SQLAlchemy（ORM）
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:pass@localhost/db')
Session = sessionmaker(bind=engine)
```

**用途:**
- データベース操作の簡素化
- マイグレーション管理

---

### 3. API・ネットワーク 🌐

#### FastAPI（API構築）
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/search")
async def search(query: str):
    # 検索処理
    return {"result": "..."}
```

**用途:**
- 社内APIの構築
- 他システムとの連携
- マイクロサービス化

#### Selenium（Web自動化）
```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://example.com')
content = driver.page_source
```

**用途:**
- 動的Webページのスクレイピング
- 社内システムからのデータ取得自動化

---

### 4. セキュリティ 🔐

#### 暗号化
```python
from cryptography.fernet import Fernet

# 暗号化キーの生成
key = Fernet.generate_key()
cipher = Fernet(key)

# データの暗号化
encrypted = cipher.encrypt(b"Secret data")
decrypted = cipher.decrypt(encrypted)
```

**用途:**
- センシティブなデータの暗号化
- APIキーの安全な保存

#### JWT認証
```python
import jwt

# トークンの生成
token = jwt.encode(
    {"user_id": 123},
    "secret_key",
    algorithm="HS256"
)

# トークンの検証
decoded = jwt.decode(token, "secret_key", algorithms=["HS256"])
```

**用途:**
- より高度な認証システム
- APIトークン認証

---

### 5. データ分析・可視化 📊

#### Matplotlib（グラフ作成）
```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
plt.title('使用状況')
plt.savefig('usage.png')
```

**用途:**
- 検索統計のグラフ化
- レポート生成

#### Plotly（インタラクティブグラフ）
```python
import plotly.express as px

fig = px.bar(df, x='category', y='count')
fig.show()
```

**用途:**
- Streamlit上でのインタラクティブな可視化
- ダッシュボード機能

---

### 6. 自然言語処理（NLP）拡張 🔤

#### spaCy（日本語NLP）
```python
import spacy

nlp = spacy.load("ja_core_news_sm")
doc = nlp("株式会社エムエムインターナショナルは清掃ロボットを提供します。")

for ent in doc.ents:
    print(ent.text, ent.label_)
```

**インストール:**
```bash
pip install spacy
python -m spacy download ja_core_news_sm
```

**用途:**
- 固有表現抽出（会社名、人名など）
- より高度な質問理解
- キーワード抽出

#### Sentence Transformers
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode(['文章1', '文章2'])
```

**用途:**
- より高精度な文章埋め込み
- 意味的類似度の計算

---

### 7. ベクトルデータベース拡張 🔍

#### FAISS（高速検索）
```python
import faiss
import numpy as np

# インデックスの作成
dimension = 128
index = faiss.IndexFlatL2(dimension)

# ベクトルの追加
vectors = np.random.random((1000, dimension)).astype('float32')
index.add(vectors)

# 検索
D, I = index.search(vectors[:5], 10)
```

**用途:**
- 大規模データの高速検索
- ChromaDBの代替

#### Pinecone（クラウドベクトルDB）
```python
import pinecone

pinecone.init(api_key="YOUR_API_KEY")
index = pinecone.Index("company-docs")

# ベクトルの追加
index.upsert([("id1", [0.1, 0.2, ...], {"text": "..."})])
```

**用途:**
- クラウドでのベクトル管理
- スケーラブルな検索

---

### 8. 音声処理 🎤

#### 音声認識
```python
import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio, language='ja-JP')
```

**用途:**
- 音声による質問入力
- 議事録の自動文字起こし

#### 音声合成
```python
from gtts import gTTS

tts = gTTS('こんにちは', lang='ja')
tts.save('output.mp3')
```

**用途:**
- 回答の読み上げ機能
- アクセシビリティ向上

---

### 9. テスト・品質管理 🧪

#### pytest（テストフレームワーク）
```python
# test_utils.py
def test_get_llm_response():
    response = get_llm_response("テスト質問")
    assert response is not None
    assert "answer" in response
```

**実行:**
```bash
pytest tests/
```

**用途:**
- 自動テスト
- 品質保証
- リグレッション防止

#### Black（コードフォーマット）
```bash
black *.py
```

**用途:**
- コードの自動整形
- チーム開発での統一性

---

## 🎯 推奨構成

### レベル1: 基本（現在）
```
streamlit + langchain + chromadb
↓
社内情報検索の基本機能
```

### レベル2: 標準拡張（推奨）
```
+ python-pptx  # PowerPoint対応
+ openpyxl     # Excel対応
+ matplotlib   # グラフ化
+ pytest       # テスト
+ loguru       # ログ強化
↓
より多様なファイル形式に対応
```

### レベル3: 高度な機能
```
+ spacy              # 高度なNLP
+ sentence-transformers  # 高精度埋め込み
+ fastapi           # API化
+ selenium          # Web自動化
↓
エンタープライズ対応
```

### レベル4: エンタープライズ
```
+ PostgreSQL/MongoDB  # データベース統合
+ Redis              # キャッシング
+ JWT                # 高度な認証
+ Celery             # バックグラウンドタスク
↓
大規模展開
```

---

## 💡 機能別推奨ライブラリ

### より多様なファイル形式に対応
```bash
pip install python-pptx openpyxl python-docx
```

### データ分析・レポート機能
```bash
pip install pandas matplotlib plotly
```

### API化・他システム連携
```bash
pip install fastapi uvicorn requests
```

### セキュリティ強化
```bash
pip install cryptography pyjwt bcrypt
```

### 音声対応（将来）
```bash
pip install SpeechRecognition gtts pydub
```

### テスト・品質管理
```bash
pip install pytest black flake8
```

---

## 📊 使用例: PowerPoint対応の実装

### ステップ1: ライブラリのインストール
```bash
pip install python-pptx
```

### ステップ2: constants.py に追加
```python
from pptx import Presentation

def load_pptx(file_path):
    prs = Presentation(file_path)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return "\n".join(text)

SUPPORTED_EXTENSIONS = {
    ".pdf": PyMuPDFLoader,
    ".docx": Docx2txtLoader,
    ".pptx": load_pptx,  # 追加
    # ...
}
```

### ステップ3: dataフォルダにPowerPointファイルを配置
```
data/
  └── メディアについて/
      └── 会社紹介.pptx  # 自動的に読み込まれる
```

---

## 🔧 トラブルシューティング

### エラー: DLL load failed
**原因:** C++ランタイムが不足

**解決法:**
```bash
# Microsoft Visual C++ 再頒布可能パッケージをインストール
# https://aka.ms/vs/17/release/vc_redist.x64.exe
```

### エラー: ModuleNotFoundError
**原因:** ライブラリが未インストール

**解決法:**
```bash
pip install <ライブラリ名>
```

### エラー: ImportError
**原因:** バージョン不整合

**解決法:**
```bash
pip install --upgrade <ライブラリ名>
```

---

## 📈 パフォーマンスへの影響

### 軽量構成（現在）
- **起動時間:** 10-15秒
- **メモリ使用量:** 約300MB
- **ディスク使用量:** 約500MB

### 標準拡張
- **起動時間:** 15-20秒
- **メモリ使用量:** 約500MB
- **ディスク使用量:** 約1GB

### フル拡張
- **起動時間:** 20-30秒
- **メモリ使用量:** 約800MB
- **ディスク使用量:** 約2GB

---

## 📞 サポート

- **メール:** ai-support@mm-international.co.jp
- **関連ファイル:**
  - `requirements_extended.txt` - 拡張ライブラリリスト
  - `install_extended.bat` - インストールスクリプト

---

*最終更新：2025年12月13日*  
*株式会社エムエムインターナショナル*

