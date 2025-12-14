import os
import shutil

# 移動するファイルのリスト
files_to_move = [
    "会社情報_公式サイト参照.md",
    "会社概要_基本情報.md",
    "会社概要_詳細版.md",
    "会社データ_財務と規模.md",
    "会社データ_数値で見るMMI.md",
    "代表者プロフィール_橋本修一.md",
    "代表メッセージ_橋本修一社長.md",
    "沿革と歴史.md",
    "経営理念とビジョン.md",
    "マルハングループとの関係.md",
    "保有資格と認定.md"
]

source_dir = "data_integrated\\02_事業・サービス"
dest_dir = "data_integrated\\01_会社情報"

# 移動先ディレクトリが存在することを確認
if not os.path.exists(dest_dir):
    print(f"エラー: {dest_dir} が存在しません")
    exit(1)

moved_count = 0
for filename in files_to_move:
    source_path = os.path.join(source_dir, filename)
    dest_path = os.path.join(dest_dir, filename)
    
    if os.path.exists(source_path):
        try:
            shutil.move(source_path, dest_path)
            print(f"移動成功: {filename}")
            moved_count += 1
        except Exception as e:
            print(f"エラー: {filename} の移動に失敗しました - {e}")
    else:
        print(f"警告: {source_path} が見つかりません")

print(f"\n合計 {moved_count} ファイルを移動しました")
