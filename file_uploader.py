from minio import Minio
from minio.error import S3Error
import os


def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "play.min.io",
        access_key="wzSFCJobuRWG7NXy",
        secret_key="TMHWjmYKJHLxY0mrZsWB5UUOSap88bKZ",
    )

    found = client.bucket_exists("buckettest")
    if not found:
        client.make_bucket("buckettest")
    else:
        print("Bucket 'buckettest' already exists")

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    fds = sorted(os.listdir('Admin/Downloads/'))
    fds_dest = sorted(os.listdir('Admin/Destination/'))
    data_dir = "Admin/Downloads/"
    dest_dir = "Admin/Destination/"
    for file in fds:
        client.fput_object(
            "buckettest", data_dir + file, data_dir + file
        )
        print(
            ""f'{data_dir + file}'" is successfully uploaded as "
            ""f'{data_dir + file}'" to bucket 'buckettest'."
        )
    for file in fds_dest:
        client.fput_object(
            "buckettest", dest_dir + file, dest_dir + file
        )
        print(
            ""f'{dest_dir + file}'" is successfully uploaded as "
            ""f'{dest_dir + file}'" to bucket 'buckettest'."
        )



if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)