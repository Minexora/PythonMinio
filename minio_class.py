import time
from io import BytesIO
from minio import Minio
from datetime import timedelta
from configs.config import settings
from console_log import create_log_app
from urllib.parse import urlparse, urlunparse

console_log = create_log_app()

class MinIOClass:
    client = None
    bucket_name = None
    file_list = []
    file_detail_list = []

    def __init__(self):
        try:
            console_log.success("Minio bağlantısı oluşturuluyor..")
            if not self.client:
                self.connect()
            is_create = self.create_bucket()
            if not is_create:
                is_ok, res = self.get_file_list()
                if is_ok:
                    self.file_list = res
                else:
                    raise Exception("The file list could not be retrieved.")
        except Exception as e:
            print(str(e))

    def connect(self):
        try:
            while not self.client:
                self.client = Minio(
                    f"{settings.minio.HOST}:{settings.minio.PORT}",
                    access_key=settings.minio.ACCESS_KEY,
                    secret_key=settings.minio.SECRET_KEY,
                    secure=False,
                )
                console_log.success("Minio bağlantısı oluşturuldu.")
                time.sleep(1)
        except Exception as e:
            print(str(e))

    def create_bucket(self, bucket_name=None):
        console_log.success("Minio bucket kontrolu yapılıyor...")
        if not bucket_name:
            bucket_name = settings.minio.BUCKET_NAME
        self.bucket_name = bucket_name
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            console_log.success("Minio bucket oluşturuldu.")
            return True
        else:
            console_log.success("Minio bucket zaten mevcuttur.")
            return False

    def upload_file(self, object_name, data, content_type, bucket_name=None, change_file=False, file_share=True):
        try:
            console_log.info("Minio file upload işlemi başlatılıyor...")
            if object_name in self.file_list and not change_file:
                console_log.success("Minio file upload işlemi başarısız. Dosya daha önceden yüklenmiş")
                return False, "File name already exists"
            res = self.client.put_object(
                bucket_name if bucket_name else self.bucket_name,
                object_name,
                BytesIO(data),
                length=len(data),
                content_type=content_type,
            )
            console_log.success("Minio file upload işlemi başarılı. Url oluşturuluyor...")
            url = None
            if file_share:
                url = self.client.presigned_get_object(bucket_name if bucket_name else self.bucket_name, object_name, expires=timedelta(hours=settings.minio.SHARE_TIME))
                parsed_url = urlparse(url)
                custom_netloc = "localhost:9001"
                url = urlunparse(parsed_url._replace(netloc=custom_netloc))
                console_log.success("Url oluşturuldu.")
            _, _ = self.get_file_list()
            return True, url if url else res
        except Exception as e:
            print(str(e))
            return False, str(e)

    def download_file(self, file_name, download_path, bucket_name=None):
        try:
            console_log.success("Minio file download işlemi başlatılıyor...")
            response = self.client.get_object(bucket_name if bucket_name else self.bucket_name, file_name)
            with open(download_path, "wb") as file_data:
                for d in response.stream(32 * 1024):
                    file_data.write(d)
            response.close()
            response.release_conn()
            console_log.success("Minio file download işlemi tamamlandı.")
            return True, None
        except Exception as e:
            print(str(e))
            return False, str(e)

    def get_file_list(self, bucket_name=None):
        try:
            console_log.success("Minio file listesi çekiliyor...")
            objects = self.client.list_objects(bucket_name if bucket_name else self.bucket_name)
            file_list = []
            self.file_detail_list = []
            for obj in objects:
                console_log.success("Minio file listesi çekildi. Urller oluşturuluyor...")
                url = self.client.get_presigned_url(method="GET", bucket_name=bucket_name if bucket_name else self.bucket_name, object_name=obj.object_name, expires=timedelta(hours=settings.minio.SHARE_TIME))
                file_list.append(obj.object_name)
                parsed_url = urlparse(url)
                custom_netloc = "localhost:9001"
                url = urlunparse(parsed_url._replace(netloc=custom_netloc))
                self.file_detail_list.append({"name": obj.object_name, "url": url})
                console_log.success("İşlem tamamlandı.")
            return True, file_list
        except Exception as e:
            print(str(e))
            return False, str(e)


if __name__ == "__main__":
    cls = MinIOClass()
    data = BytesIO(b"Hello, MinIO!")
    is_ok, res = cls.upload_file(object_name="Hello.txt", data=data, content_type="text/plain", change_file=True)
    # cls.download_file(file_name="Hello.txt", download_path="hello-word.txt")
    # res = cls.get_file_list()
    # print("File List: ", res)
