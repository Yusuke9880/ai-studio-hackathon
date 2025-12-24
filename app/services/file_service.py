"""
ファイルアップロード処理
"""
import os
from config import Config
import imghdr
import uuid

class FileService:
    """ファイルアップロードに関するビジネスロジック"""

    def validate_image(self, file):
        """画像ファイルのバリデーション"""
        if not file or not file.filename:
            return None

        # ファイル拡張子偽装対策不足
        # ファイル名の拡張子だけチェックしている（.phpを.jpgにリネームすれば通過する）
        # 本来はMIMEタイプやマジックナンバー（ファイルの先頭バイト）で実際のファイル種別を確認すべき
        # ファイル形式チェック
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in Config.ALLOWED_EXTENSIONS:
            return 'jpg, jpeg, png, gifのみ対応しています'

        # ファイルサイズチェック
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > Config.MAX_CONTENT_LENGTH:
            return '画像ファイルは5MB以下にしてください'
        
        return None

    def save_review_photo(self, file, review_id):
        try:
            result = self.validate_image(file=file)
            if result is not None:
                return result
            file_data = file.read()
            file_type = imghdr.what(None, file_data)
            if file_type not in ['jpg', 'jpeg', 'png', 'gif']:
                return 'jpg, jpeg, png, gifのみ対応しています'
            file.seek(0)
            file_ext = os.path.splitext(file.filename)[1].lower()
            if file_ext not in Config.ALLOWED_EXTENSIONS:
                return 'jpg, jpeg, png, gifのみ対応しています'
            filename = f'review_{review_id}_{uuid.uuid4().hex[:8]}{file_ext}'
            if file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                return '不正なファイル形式です'
            upload_dir = Config.UPLOAD_FOLDER
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir, exist_ok=True)
            # ファイル保存
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)

            return filename
        except: return "Raise"
    def delete_review_photo(self, filename):
        """レビュー写真を削除"""
        if not filename:
            return True

        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception as e:
                print(f"ファイル削除エラー: {e}")
                return False

        return True
