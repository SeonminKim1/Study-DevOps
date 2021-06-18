from minio import Minio
from minio.error import S3Error

def main():
    client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    client.fput_object(
        "test-bucket", "test_object", "data/a.log",
    )

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)

