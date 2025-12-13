"""
メディアビューワーモジュール
画像・動画の表示と処理機能を提供します。

使用方法:
    import media_viewer
    media_viewer.show_image("path/to/image.jpg")
    media_viewer.show_video("path/to/video.mp4")
"""

import os
from pathlib import Path
from typing import Optional, List, Tuple
import streamlit as st

# 画像処理
try:
    from PIL import Image
    import piexif
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

# 動画処理
try:
    from pymediainfo import MediaInfo
    MEDIAINFO_AVAILABLE = True
except ImportError:
    MEDIAINFO_AVAILABLE = False

# QRコード
try:
    import qrcode
    from pyzbar import pyzbar
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False


class ImageViewer:
    """画像ビューワークラス"""
    
    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """サポートされている画像形式かチェック"""
        ext = Path(file_path).suffix.lower()
        return ext in ImageViewer.SUPPORTED_FORMATS
    
    @staticmethod
    def show_image(image_path: str, caption: str = None, width: int = None):
        """
        Streamlitで画像を表示
        
        Args:
            image_path: 画像ファイルのパス
            caption: キャプション
            width: 表示幅（ピクセル）
        """
        if not PILLOW_AVAILABLE:
            st.error("画像表示にはPillowライブラリが必要です: pip install Pillow")
            return
        
        try:
            if not os.path.exists(image_path):
                st.error(f"画像ファイルが見つかりません: {image_path}")
                return
            
            # 画像を読み込み
            image = Image.open(image_path)
            
            # メタデータを取得
            info = ImageViewer.get_image_info(image_path)
            
            # 画像を表示
            if width:
                st.image(image, caption=caption, width=width)
            else:
                st.image(image, caption=caption, use_container_width=True)
            
            # 情報を表示
            with st.expander("📊 画像情報"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**サイズ:** {info['width']} x {info['height']}")
                    st.write(f"**フォーマット:** {info['format']}")
                with col2:
                    st.write(f"**モード:** {info['mode']}")
                    st.write(f"**ファイルサイズ:** {info['file_size']}")
        
        except Exception as e:
            st.error(f"画像の表示に失敗しました: {str(e)}")
    
    @staticmethod
    def get_image_info(image_path: str) -> dict:
        """画像のメタデータを取得"""
        try:
            image = Image.open(image_path)
            file_size = os.path.getsize(image_path)
            
            return {
                'width': image.width,
                'height': image.height,
                'format': image.format,
                'mode': image.mode,
                'file_size': f"{file_size / 1024:.1f} KB"
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def create_thumbnail(image_path: str, size: Tuple[int, int] = (200, 200)) -> Optional[Image.Image]:
        """サムネイル画像を作成"""
        if not PILLOW_AVAILABLE:
            return None
        
        try:
            image = Image.open(image_path)
            image.thumbnail(size)
            return image
        except Exception:
            return None
    
    @staticmethod
    def resize_image(image_path: str, width: int, height: int, output_path: str):
        """画像をリサイズして保存"""
        if not PILLOW_AVAILABLE:
            raise ImportError("Pillowライブラリが必要です")
        
        try:
            image = Image.open(image_path)
            resized = image.resize((width, height), Image.Resampling.LANCZOS)
            resized.save(output_path)
            return True
        except Exception as e:
            st.error(f"画像のリサイズに失敗: {str(e)}")
            return False


class VideoViewer:
    """動画ビューワークラス"""
    
    SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """サポートされている動画形式かチェック"""
        ext = Path(file_path).suffix.lower()
        return ext in VideoViewer.SUPPORTED_FORMATS
    
    @staticmethod
    def show_video(video_path: str, start_time: int = 0):
        """
        Streamlitで動画を表示
        
        Args:
            video_path: 動画ファイルのパス
            start_time: 開始時間（秒）
        """
        try:
            if not os.path.exists(video_path):
                st.error(f"動画ファイルが見つかりません: {video_path}")
                return
            
            # 動画を表示
            with open(video_path, 'rb') as video_file:
                video_bytes = video_file.read()
                st.video(video_bytes, start_time=start_time)
            
            # 動画情報を表示
            info = VideoViewer.get_video_info(video_path)
            
            if info and 'error' not in info:
                with st.expander("📹 動画情報"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**解像度:** {info.get('width', 'N/A')} x {info.get('height', 'N/A')}")
                        st.write(f"**フレームレート:** {info.get('frame_rate', 'N/A')} fps")
                    with col2:
                        st.write(f"**長さ:** {info.get('duration', 'N/A')}")
                        st.write(f"**ファイルサイズ:** {info.get('file_size', 'N/A')}")
        
        except Exception as e:
            st.error(f"動画の表示に失敗しました: {str(e)}")
    
    @staticmethod
    def get_video_info(video_path: str) -> dict:
        """動画のメタデータを取得"""
        if not MEDIAINFO_AVAILABLE:
            # pymediainfoがない場合は基本情報のみ
            file_size = os.path.getsize(video_path)
            return {
                'file_size': f"{file_size / (1024 * 1024):.1f} MB",
                'format': Path(video_path).suffix[1:].upper()
            }
        
        try:
            media_info = MediaInfo.parse(video_path)
            file_size = os.path.getsize(video_path)
            
            info = {
                'file_size': f"{file_size / (1024 * 1024):.1f} MB",
                'format': Path(video_path).suffix[1:].upper()
            }
            
            # ビデオトラック情報
            for track in media_info.tracks:
                if track.track_type == "Video":
                    info['width'] = track.width
                    info['height'] = track.height
                    info['frame_rate'] = f"{track.frame_rate:.2f}" if track.frame_rate else "N/A"
                    info['duration'] = f"{int(track.duration / 1000)}秒" if track.duration else "N/A"
                    break
            
            return info
        
        except Exception as e:
            return {'error': str(e)}


class QRCodeHandler:
    """QRコード生成・読み取りクラス"""
    
    @staticmethod
    def generate_qr(data: str, output_path: str = None) -> Optional[Image.Image]:
        """
        QRコードを生成
        
        Args:
            data: QRコードに埋め込むデータ
            output_path: 保存先パス（Noneの場合は保存しない）
        
        Returns:
            QRコード画像
        """
        if not QR_AVAILABLE:
            st.error("QRコード生成にはqrcodeライブラリが必要です: pip install qrcode")
            return None
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            if output_path:
                img.save(output_path)
            
            return img
        
        except Exception as e:
            st.error(f"QRコードの生成に失敗: {str(e)}")
            return None
    
    @staticmethod
    def read_qr(image_path: str) -> List[str]:
        """
        画像からQRコードを読み取る
        
        Args:
            image_path: 画像ファイルのパス
        
        Returns:
            読み取ったデータのリスト
        """
        if not QR_AVAILABLE:
            st.error("QRコード読み取りにはpyzbarライブラリが必要です: pip install pyzbar")
            return []
        
        try:
            image = Image.open(image_path)
            decoded_objects = pyzbar.decode(image)
            
            results = []
            for obj in decoded_objects:
                results.append(obj.data.decode('utf-8'))
            
            return results
        
        except Exception as e:
            st.error(f"QRコードの読み取りに失敗: {str(e)}")
            return []


def display_media_gallery(directory: str, media_type: str = "all"):
    """
    ディレクトリ内のメディアファイルをギャラリー表示
    
    Args:
        directory: ディレクトリパス
        media_type: "image", "video", or "all"
    """
    if not os.path.exists(directory):
        st.error(f"ディレクトリが見つかりません: {directory}")
        return
    
    files = []
    
    # ファイルを収集
    for file in Path(directory).rglob('*'):
        if file.is_file():
            if media_type == "image" and ImageViewer.is_supported(str(file)):
                files.append(file)
            elif media_type == "video" and VideoViewer.is_supported(str(file)):
                files.append(file)
            elif media_type == "all" and (ImageViewer.is_supported(str(file)) or VideoViewer.is_supported(str(file))):
                files.append(file)
    
    if not files:
        st.info("メディアファイルが見つかりませんでした。")
        return
    
    st.write(f"**{len(files)}個のファイルが見つかりました**")
    
    # ギャラリー表示
    cols = st.columns(3)
    
    for idx, file_path in enumerate(files):
        col_idx = idx % 3
        
        with cols[col_idx]:
            if ImageViewer.is_supported(str(file_path)):
                # 画像の場合
                thumbnail = ImageViewer.create_thumbnail(str(file_path))
                if thumbnail:
                    st.image(thumbnail, caption=file_path.name)
                    if st.button(f"表示 ({file_path.name})", key=f"img_{idx}"):
                        ImageViewer.show_image(str(file_path))
            
            elif VideoViewer.is_supported(str(file_path)):
                # 動画の場合
                st.write(f"🎬 {file_path.name}")
                if st.button(f"再生 ({file_path.name})", key=f"vid_{idx}"):
                    VideoViewer.show_video(str(file_path))


# デモ用の関数
def demo_media_viewer():
    """メディアビューワーのデモ"""
    st.title("📸 メディアビューワー")
    
    tab1, tab2, tab3 = st.tabs(["画像表示", "動画再生", "QRコード"])
    
    with tab1:
        st.header("画像表示")
        uploaded_file = st.file_uploader("画像をアップロード", type=['jpg', 'jpeg', 'png', 'gif', 'bmp'])
        
        if uploaded_file:
            # 一時保存
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            ImageViewer.show_image(temp_path, caption=uploaded_file.name)
            
            # クリーンアップ
            os.remove(temp_path)
    
    with tab2:
        st.header("動画再生")
        video_file = st.file_uploader("動画をアップロード", type=['mp4', 'avi', 'mov', 'mkv'])
        
        if video_file:
            # 一時保存
            temp_path = f"temp_{video_file.name}"
            with open(temp_path, 'wb') as f:
                f.write(video_file.getbuffer())
            
            VideoViewer.show_video(temp_path)
            
            # クリーンアップ
            os.remove(temp_path)
    
    with tab3:
        st.header("QRコード")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("QRコード生成")
            qr_text = st.text_input("埋め込むテキスト")
            
            if st.button("QRコード生成"):
                if qr_text:
                    qr_img = QRCodeHandler.generate_qr(qr_text)
                    if qr_img:
                        st.image(qr_img, caption="生成されたQRコード")
        
        with col2:
            st.subheader("QRコード読み取り")
            qr_image = st.file_uploader("QRコード画像をアップロード", type=['jpg', 'png'])
            
            if qr_image:
                temp_path = f"temp_{qr_image.name}"
                with open(temp_path, 'wb') as f:
                    f.write(qr_image.getbuffer())
                
                results = QRCodeHandler.read_qr(temp_path)
                
                if results:
                    st.success("QRコードを読み取りました:")
                    for result in results:
                        st.code(result)
                else:
                    st.warning("QRコードが見つかりませんでした。")
                
                os.remove(temp_path)


if __name__ == "__main__":
    demo_media_viewer()

