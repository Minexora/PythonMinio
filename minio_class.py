from minio import Minio
from configs.config import settings
from io import BytesIO
from datetime import timedelta


class MinIOClass:
    client = None
    bucket_name = None
    file_list = []
    file_detail_list = []

    def __init__(self):
        try:
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
            self.client = Minio(
                "minio:9000",
                access_key=settings.minio.ACCESS_KEY,
                secret_key=settings.minio.SECRET_KEY,
                secure=False,
            )
        except Exception as e:
            print(str(e))

    def create_bucket(self, bucket_name=None):
        if not bucket_name:
            bucket_name = settings.minio.BUCKET_NAME
        self.bucket_name = bucket_name
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            return True
        else:
            return False

    def upload_file(self, object_name, data, content_type, bucket_name=None, change_file=False, file_share=True):
        try:
            if object_name in self.file_list and not change_file:
                return False, "File name already exists"
            res = self.client.put_object(
                bucket_name if bucket_name else self.bucket_name,
                object_name,
                BytesIO(data),
                length=len(data),
                content_type=content_type,
            )
            url = None
            if file_share:
                url = self.client.presigned_get_object(bucket_name if bucket_name else self.bucket_name, object_name, expires=timedelta(hours=settings.minio.SHARE_TIME))
            return True, url if url else res
        except Exception as e:
            print(str(e))
            return False, str(e)

    def download_file(self, file_name, download_path, bucket_name=None):
        try:
            response = self.client.get_object(bucket_name if bucket_name else self.bucket_name, file_name)
            with open(download_path, "wb") as file_data:
                for d in response.stream(32 * 1024):
                    file_data.write(d)
            response.close()
            response.release_conn()
            return True, None
        except Exception as e:
            print(str(e))
            return False, str(e)

    def get_file_list(self, bucket_name=None):
        try:
            objects = self.client.list_objects(bucket_name if bucket_name else self.bucket_name)
            file_list = []
            self.file_detail_list = []
            for obj in objects:
                url = self.client.presigned_get_object(bucket_name if bucket_name else self.bucket_name, obj.object_name)
                file_list.append(obj.object_name)
                self.file_detail_list.append({"name": obj.object_name, "url": url})
            return True, file_list
        except Exception as e:
            print(str(e))
            return False, str(e)


print("File uploaded successfully")

if __name__ == "__main__":
    cls = MinIOClass()
    data = BytesIO(b"Hello, MinIO!")
    is_ok, res = cls.upload_file(object_name="Hello.txt", data=data, content_type="text/plain", change_file=True)
    # cls.download_file(file_name="Hello.txt", download_path="hello-word.txt")
    # res = cls.get_file_list()
    # print("File List: ", res)
