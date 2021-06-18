from minio import Minio
from minio.error import S3Error

def main():
    client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    # Get a full object
    obj = client.get_object('test-bucket', 'test_object')
    print(obj.data) # hello world ~

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)

