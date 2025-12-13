# ロゴ・アバター機能ガイド

株式会社エムエムインターナショナル 社内情報検索AIアプリに、会社ロゴと管理部長アバター（口が動くアニメーション付き）を追加しました。

---

## ✅ 実装された機能

### 1. 会社ロゴ表示 🏢
- ウェルカム画面に大きく表示
- サイドバーに常時表示
- ホバーエフェクト付き

### 2. 管理部長アバター 👨‍💼
- かわいらしいイラスト風デザイン
- 40代男性、メガネ、スーツ姿
- 口が動くアニメーション機能
- 複数サイズ対応（40px, 80px, 120px, 150px）

### 3. アニメーション効果 ✨
- 口が動くトーキングアニメーション
- 上下に軽く揺れる動き
- スムーズなCSS3アニメーション

---

## 📁 作成されたファイル

1. ✅ **`avatar_manager.py`** - アバター・ロゴ管理モジュール（700行）
   - LogoManager クラス
   - AvatarManager クラス
   - アニメーション機能

2. ✅ **`assets/images/README.md`** - 画像配置ガイド

3. ✅ **`assets/images/`** - 画像格納フォルダ
   - `mm_logo.png` を配置（準備中）
   - `manager_avatar.png` を配置（準備中）

4. ✅ **`AVATAR_LOGO_GUIDE.md`** - このガイド

---

## 🎨 現在の表示

### デフォルト（画像未配置時）

アプリは自動的にSVGプレースホルダーを表示します：

#### ロゴ
- 青色の「MM International」テキストロゴ
- シンプルで見やすいデザイン

#### アバター
- かわいいイラスト風の管理部長
- メガネをかけた40代男性
- 紺色のスーツ
- 親しみやすい笑顔

**これらはすぐに使用できます！**

---

## 🖼️ カスタム画像の配置方法

### ステップ1: 画像を用意

#### ロゴ画像
**ファイル名:** `mm_logo.png`

**方法1: 既存ロゴを使用**
```
1. 会社の公式ロゴデータを入手
2. PNG形式で保存（透過背景推奨）
3. 幅200-400pxにリサイズ
```

**方法2: オンラインツールで作成**
- Canva: https://www.canva.com/
- LogoMaker: https://www.logomaker.com/

#### アバター画像
**ファイル名:** `manager_avatar.png`

**方法1: AI画像生成（推奨）** ⭐
```
ツール: Stable Diffusion, Midjourney, DALL-E

プロンプト:
"cute cartoon business manager avatar, 40s Japanese male, 
wearing glasses, navy suit, friendly smile, 
minimalist flat design, transparent background"
```

**方法2: オンライン無料ツール**
- Canva (https://www.canva.com/)
- Bitmoji (https://www.bitmoji.com/)
- Adobe Express (https://www.adobe.com/express/)

**方法3: 写真をイラスト化**
```
1. 管理部長の写真を撮影
2. ToonMe (https://toonme.com/) でイラスト化
3. remove.bg で背景を削除
4. 120x120pxにリサイズ
```

### ステップ2: 画像を配置

```bash
# 画像をassetsフォルダにコピー
コピー元: ダウンロード/mm_logo.png
コピー先: C:\Users\...\社内情報特化型生成AI検索アプリ\assets\images\mm_logo.png

コピー元: ダウンロード/manager_avatar.png
コピー先: C:\Users\...\社内情報特化型生成AI検索アプリ\assets\images\manager_avatar.png
```

### ステップ3: アプリを再起動

```bash
# Ctrl+C でアプリを停止
# 再度起動
streamlit run main.py
```

---

## 💻 使用方法

### アプリ起動時

アプリを起動すると自動的に：
1. ✅ サイドバーにロゴが表示
2. ✅ サイドバーにアバターが表示
3. ✅ 初回のみウェルカム画面を表示

### ウェルカム画面

初回アクセス時に表示されます：
- 大きな会社ロゴ
- 「社内情報検索AI」タイトル
- 管理部長アバター（150px）
- ウェルカムメッセージ

### サイドバー

常時表示されます：
- 小さな会社ロゴ（150px）
- 管理部長アバター（80px）
- 「AI管理部長」ラベル

---

## 🎬 アニメーション機能

### 口が動くアニメーション

```python
from avatar_manager import AvatarManager

# 通常表示
AvatarManager.show_avatar(talking=False)

# 話している（アニメーション）
AvatarManager.show_avatar(talking=True)
```

### アニメーションの詳細

- **動き:** 口が開閉する
- **速度:** 0.8秒で1サイクル
- **効果:** 上下に軽く揺れる
- **技術:** CSS3 アニメーション（軽量）

---

## 📊 表示箇所一覧

| 場所 | ロゴサイズ | アバターサイズ | アニメーション |
|------|-----------|--------------|--------------|
| ウェルカム画面 | 250px | 150px | なし |
| サイドバー | 150px | 80px | なし |
| チャット（将来） | - | 40px | あり |

---

## 🎨 カスタマイズ

### サイズ変更

```python
from avatar_manager import LogoManager, AvatarManager

# ロゴサイズ変更
LogoManager.show_logo(width=300)

# アバターサイズ変更
AvatarManager.show_avatar(size=200)
```

### 配置変更

```python
# ロゴを中央配置
LogoManager.show_logo(width=200, use_column=True)

# カスタム配置
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    LogoManager.show_logo(width=200)
```

---

## 🎯 実用例

### 例1: チャット内でアバターを使う

```python
from avatar_manager import show_chat_avatar

# ユーザーメッセージ
show_chat_avatar("JINNYの導入台数は？", is_user=True)

# AI管理部長の回答
show_chat_avatar("1,000台以上導入されています！", is_user=False)
```

### 例2: デモページを作成

```python
from avatar_manager import demo_avatar_showcase

# デモアプリを起動
demo_avatar_showcase()
```

---

## 🔧 トラブルシューティング

### 画像が表示されない

**原因1:** ファイル名が間違っている

**解決法:**
```
正: mm_logo.png
誤: mm-logo.png, mmlogo.png, MM_LOGO.PNG
```

**原因2:** ファイルパスが間違っている

**解決法:**
```
正しいパス:
C:\Users\...\社内情報特化型生成AI検索アプリ\assets\images\mm_logo.png
```

**原因3:** 画像形式が対応していない

**解決法:**
```
対応形式: PNG, JPG, JPEG
推奨: 透過PNG
```

### アニメーションが動かない

**原因:** ブラウザのキャッシュ

**解決法:**
```
1. Ctrl+Shift+R でハードリフレッシュ
2. または Ctrl+F5
```

### SVGプレースホルダーが消えない

**原因:** 画像ファイルが読み込まれていない

**解決法:**
```bash
# ファイルの存在確認
dir assets\images\

# アプリを再起動
```

---

## 📖 関連ファイル

### Pythonモジュール
- **`avatar_manager.py`** - メインモジュール
  - LogoManager クラス
  - AvatarManager クラス
  - アニメーション関数

### ドキュメント
- **`assets/images/README.md`** - 画像配置ガイド
- **`AVATAR_LOGO_GUIDE.md`** - このファイル

### 統合先
- **`main.py`** - アプリメインファイル
  - `avatar_manager` をインポート
  - スタイル適用
  - サイドバーに表示

---

## 🎨 デモアプリを試す

```bash
# アバター・ロゴのデモを起動
streamlit run avatar_manager.py
```

**含まれる機能:**
- ウェルカム画面のプレビュー
- アバターのバリエーション表示
- サイズ比較
- アニメーションデモ
- チャット例

---

## ✅ チェックリスト

画像配置の確認：
- [ ] `assets/images/mm_logo.png` を配置
- [ ] `assets/images/manager_avatar.png` を配置
- [ ] ロゴサイズが適切（200-400px幅）
- [ ] アバターサイズが適切（120x120px）
- [ ] 透過PNG形式
- [ ] アプリを再起動
- [ ] 表示を確認

機能確認：
- [ ] サイドバーにロゴが表示される
- [ ] サイドバーにアバターが表示される
- [ ] ウェルカム画面が表示される
- [ ] アニメーションが動作する
- [ ] レイアウトが崩れていない

---

## 💡 ヒント

### 画像がない場合でも使える

画像ファイルを配置しなくても、SVGプレースホルダーが表示されるので、すぐに使い始められます！

### 後から画像を追加可能

最初はSVGを使用し、後から実際の画像に差し替えることもできます。

### デモアプリで確認

実装前にデモアプリで表示を確認できます：
```bash
streamlit run avatar_manager.py
```

---

## 📞 サポート

ご質問やトラブルがあれば：
- **メール:** ai-support@mm-international.co.jp
- **デモアプリ:** `streamlit run avatar_manager.py`
- **詳細:** `assets/images/README.md`

---

*最終更新：2025年12月13日*  
*株式会社エムエムインターナショナル*

