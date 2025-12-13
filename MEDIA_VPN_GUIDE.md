# メディア・VPN機能ガイド

株式会社エムエムインターナショナル 社内情報検索AIアプリに、画像・動画閲覧とVPN機能を追加するガイドです。

---

## 📋 概要

### 追加される機能

#### 1. 画像処理・閲覧 📸
- 画像の表示と情報取得
- QRコード生成・読み取り
- 画像リサイズ・変換
- OCR（光学文字認識）
- RAW画像対応
- WebP, AVIF対応

#### 2. 動画処理・再生 🎬
- 動画再生
- 動画情報取得
- YouTube動画ダウンロード
- 動画フレーム抽出
- 動画サムネイル生成
- 動画編集

#### 3. VPN・セキュリティ 🔐
- プロキシ設定
- SSHトンネル
- セキュアブラウジング
- 接続状態確認
- User-Agent偽装

---

## 🚀 インストール方法

### 方法1: ワンクリックインストール（推奨）

```bash
# ダブルクリック
install_media_vpn.bat
```

**選択肢:**
```
1. 基本版（軽量）- 約80MB
2. 完全版 - 約180MB
3. 画像処理のみ - 約40MB
4. 動画処理のみ - 約60MB
5. VPN機能のみ - 約20MB
```

### 方法2: 手動インストール

#### 基本版（推奨）
```bash
pip install -r requirements_media_basic.txt
```

#### 完全版
```bash
pip install -r requirements_media_vpn.txt
```

---

## 📦 パッケージ内容

### 基本版（80MB）

| カテゴリ | ライブラリ | 機能 |
|---------|-----------|------|
| 画像 | Pillow | 画像表示・編集 |
| 画像 | qrcode, pyzbar | QRコード |
| 画像 | imagehash | 画像類似度 |
| 動画 | pymediainfo | 動画情報 |
| 動画 | yt-dlp | YouTube |
| VPN | PySocks | プロキシ |
| VPN | sshtunnel | SSHトンネル |

### 完全版（180MB）

上記に加えて：

| カテゴリ | ライブラリ | 機能 |
|---------|-----------|------|
| 画像 | pytesseract | OCR |
| 画像 | opencv | 顔検出 |
| 画像 | rawpy | RAW画像 |
| 動画 | moviepy | 動画編集 |
| 動画 | ffmpeg | 動画変換 |
| VPN | openvpn | VPN |
| VPN | scapy | ネットワーク監視 |

---

## 💻 使用方法

### 1. 画像ビューワー

#### 基本的な使用方法

```python
from media_viewer import ImageViewer

# 画像を表示
ImageViewer.show_image("path/to/image.jpg", caption="サンプル画像")

# 画像情報を取得
info = ImageViewer.get_image_info("path/to/image.jpg")
print(info)  # {'width': 1920, 'height': 1080, ...}

# サムネイル作成
thumbnail = ImageViewer.create_thumbnail("path/to/image.jpg", size=(200, 200))
```

#### Streamlitアプリ内で使用

```python
import streamlit as st
from media_viewer import ImageViewer

st.title("画像ビューワー")

uploaded_file = st.file_uploader("画像をアップロード", type=['jpg', 'png'])

if uploaded_file:
    # 一時保存
    with open(f"temp_{uploaded_file.name}", 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    # 画像を表示
    ImageViewer.show_image(f"temp_{uploaded_file.name}")
```

---

### 2. QRコード機能

#### QRコード生成

```python
from media_viewer import QRCodeHandler

# QRコードを生成
qr_img = QRCodeHandler.generate_qr("https://mm-international.co.jp")

# ファイルに保存
qr_img.save("qrcode.png")
```

#### QRコード読み取り

```python
# QRコードを読み取る
results = QRCodeHandler.read_qr("qrcode.png")
print(results)  # ['https://mm-international.co.jp']
```

---

### 3. 動画ビューワー

#### 基本的な使用方法

```python
from media_viewer import VideoViewer

# 動画を再生
VideoViewer.show_video("path/to/video.mp4")

# 動画情報を取得
info = VideoViewer.get_video_info("path/to/video.mp4")
print(info)  # {'width': 1920, 'height': 1080, 'duration': '120秒', ...}
```

---

### 4. VPN・プロキシ

#### プロキシ設定

```python
from vpn_manager import ProxyManager

# プロキシマネージャーを作成
proxy = ProxyManager()

# プロキシを設定
proxy.set_proxy("localhost:8080", "http")

# プロキシ経由でリクエスト
response = proxy.get_request("https://example.com")
print(response.text)

# 接続テスト
if proxy.test_connection():
    print("接続成功")
```

#### SSHトンネル

```python
from vpn_manager import SSHTunnelManager

# SSHトンネルマネージャーを作成
tunnel = SSHTunnelManager()

# トンネルを作成
tunnel.create_tunnel(
    ssh_host="example.com",
    ssh_port=22,
    ssh_user="user",
    ssh_password="password"
)

# トンネルが有効か確認
if tunnel.is_active():
    print("トンネルが有効です")

# トンネルを閉じる
tunnel.close_tunnel()
```

#### セキュアブラウジング

```python
from vpn_manager import SecureBrowser

# セキュアブラウザを作成
browser = SecureBrowser()

# セキュアにリクエスト
response = browser.secure_get("https://example.com")

# リトライ付きリクエスト
response = browser.get_with_retry("https://example.com", max_retries=3)
```

---

### 5. メディアギャラリー

```python
from media_viewer import display_media_gallery

# ディレクトリ内の画像・動画をギャラリー表示
display_media_gallery("data/メディアについて", media_type="all")

# 画像のみ表示
display_media_gallery("data/メディアについて", media_type="image")

# 動画のみ表示
display_media_gallery("data/メディアについて", media_type="video")
```

---

## 🎯 実用例

### 例1: PDFの画像をOCRで検索可能にする

```python
from PIL import Image
import pytesseract

# PDFから画像を抽出（pdf2image使用）
from pdf2image import convert_from_path

images = convert_from_path('document.pdf')

# 各ページをOCR
for i, image in enumerate(images):
    text = pytesseract.image_to_string(image, lang='jpn')
    print(f"ページ {i+1}: {text}")
```

### 例2: 社内ドキュメントにQRコードを追加

```python
from media_viewer import QRCodeHandler

# 社内ポータルのURLをQRコード化
qr_img = QRCodeHandler.generate_qr("https://portal.mm-international.co.jp")
qr_img.save("portal_qr.png")
```

### 例3: プロキシ経由でWebスクレイピング

```python
from vpn_manager import ProxyManager
from bs4 import BeautifulSoup

proxy = ProxyManager()
proxy.set_proxy("localhost:8080", "http")

response = proxy.get_request("https://example.com")
soup = BeautifulSoup(response.text, 'html.parser')

# データを抽出
titles = soup.find_all('h2')
for title in titles:
    print(title.text)
```

### 例4: YouTube動画から議事録作成

```python
import yt_dlp

# YouTube動画の音声を取得
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=VIDEO_ID'])

# 音声をテキスト化（別途音声認識ライブラリが必要）
```

---

## 🎨 UIへの統合

### メインアプリに統合する方法

**`main.py` に追加:**

```python
import streamlit as st
from media_viewer import ImageViewer, VideoViewer, display_media_gallery

# サイドバーにメディアビューワーを追加
with st.sidebar:
    st.markdown("---")
    st.header("📸 メディア")
    
    media_option = st.selectbox(
        "メディア機能",
        ["なし", "画像アップロード", "動画アップロード", "ギャラリー"]
    )
    
    if media_option == "画像アップロード":
        uploaded_image = st.file_uploader("画像", type=['jpg', 'png'])
        if uploaded_image:
            ImageViewer.show_image(uploaded_image)
    
    elif media_option == "動画アップロード":
        uploaded_video = st.file_uploader("動画", type=['mp4', 'avi'])
        if uploaded_video:
            VideoViewer.show_video(uploaded_video)
    
    elif media_option == "ギャラリー":
        display_media_gallery("data/メディアについて")
```

---

## 📊 パフォーマンス影響

| 構成 | サイズ | 起動時間 | メモリ |
|------|--------|----------|--------|
| 基本版 | +80MB | +1-2秒 | +50MB |
| 完全版 | +180MB | +3-5秒 | +100MB |

**推奨:** 基本版で開始し、必要に応じて機能を追加

---

## 🔧 トラブルシューティング

### OCRが動作しない

**原因:** Tesseract本体がインストールされていない

**解決法:**
```bash
# Windows
# https://github.com/tesseract-ocr/tesseract
# からインストーラーをダウンロード・実行

# 環境変数に追加
set PATH=%PATH%;C:\Program Files\Tesseract-OCR
```

### 動画が再生できない

**原因:** FFmpegがインストールされていない

**解決法:**
```bash
# Windowsの場合
# https://ffmpeg.org/download.html
# からダウンロード・インストール
```

### プロキシが接続できない

**原因:** プロキシ設定が間違っている

**解決法:**
```python
# 正しい形式で設定
proxy.set_proxy("localhost:8080", "http")  # ポート番号を含める
```

---

## 🔐 セキュリティ注意事項

### VPN使用時

1. **信頼できるVPNサーバーのみ使用**
2. **SSH鍵認証を推奨**（パスワード認証より安全）
3. **接続ログを定期的に確認**

### プロキシ使用時

1. **社内プロキシのポリシーを確認**
2. **不明なプロキシは使用しない**
3. **SSL証明書を検証する**

---

## 📞 サポート

- **メール:** ai-support@mm-international.co.jp
- **関連ファイル:**
  - `media_viewer.py` - メディアビューワー
  - `vpn_manager.py` - VPNマネージャー
  - `requirements_media_basic.txt` - 基本版
  - `requirements_media_vpn.txt` - 完全版

---

*最終更新：2025年12月13日*  
*株式会社エムエムインターナショナル*

