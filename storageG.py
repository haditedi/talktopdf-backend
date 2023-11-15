from google.cloud import storage
from typing import List


def set_bucket_public_iam(
    bucket_name: str = "your-bucket-name",
    members: List[str] = ["allUsers"],
):
    """Set a public IAM Policy to bucket"""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append({"role": "roles/storage.objectViewer", "members": members})

    bucket.set_iam_policy(policy)

    print(f"Bucket {bucket.name} is now publicly readable")


def authenticate(project_id="your-google-cloud-project-id"):
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")


# authenticate(project_id="talktopdf")


def list_buckets():
    """Lists all buckets."""

    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print(bucket.name)


# list_buckets()


def list_blobs(bucket_name):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)
    for blob in blobs:
        print(blob.name)


def delete_blob(bucket_name, blob_name):
    try:
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        # generation_match_precondition = None
        # blob.reload()
        # generation_match_precondition = blob.generation
        # blob.delete(if_generation_match=generation_match_precondition)
        blob.delete()

        print(f"Blob {blob_name} deleted.")
    except Exception as e:
        print("ERROR delete blob ", e)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    generation_match_precondition = 0

    blob.upload_from_filename(
        source_file_name, if_generation_match=generation_match_precondition
    )

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def upload_blob_from_stream(bucket_name, file_obj, destination_blob_name):
    """Uploads bytes from a stream or other file-like object to a blob."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The stream or file (file-like object) from which to read
    # import io
    # file_obj = io.BytesIO()
    # file_obj.write(b"This is test data.")

    # The desired name of the uploaded GCS object (blob)
    # destination_blob_name = "storage-object-name"

    # Construct a client-side representation of the blob.
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Rewind the stream to the beginning. This step can be omitted if the input
    # stream will always be at a correct position.
    file_obj.seek(0)

    # Upload data from the stream to your bucket.
    blob.upload_from_file(file_obj)
    # blob.upload_from_filename(file_obj)
    print(f"Stream data uploaded to {destination_blob_name} in bucket {bucket_name}.")


# upload_blob("talktopdf.appspot.com","upload/Product Atomy.pdf","Product Atomy.pdf")
# set_bucket_public_iam(bucket_name="talktopdf.appspot.com",members= ["allUsers"])
# delete_blob("talktopdf.appspot.com","invoice.pdf")
# list_blobs("talktopdf.appspot.com")
# upload_blob_from_stream("talktopdf.appspot.com", "./upload/credit.pdf", "OLALA")
