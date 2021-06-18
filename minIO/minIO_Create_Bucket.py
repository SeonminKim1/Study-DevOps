from minio import Minio
from minio.error import S3Error

def main():
    # Create a client with the MinIO server playground, its access key and secret key.
    client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    # Make 'test_a' bucket if not exist.
    found = client.bucket_exists("test-bucket")
    if not found:
        client.make_bucket("test-bucket")
    else:
        print("Bucket 'test_bucket' already exists")

    # Upload '/data/a.log' as object name(test_object)
    client.fput_object(
        "test-bucket", "test_object", "data/a.log",
    )
    # print(
    #     "bucket 'test_bucket' is successfully uploaded\n"
    #     "object 'test_object' to bucket 'test_bucket'."
    # )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)