import os
from uuid import uuid4
import logging

from minio import Minio
from minio.error import S3Error

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_settings = {
    "uri": os.environ.get("MINIO_URI", "localhost:9000"),
    "user": os.environ.get("MINIO_ROOT_USER", None),
    "password": os.environ.get("MINIO_ROOT_PASSWORD", None),
    "bucket": os.environ.get("MINIO_BUCKET", "test-bucket")
}

_client = Minio(
    endpoint=_settings["uri"],
    access_key=_settings["user"],
    secret_key=_settings["password"],
    secure=False  # Set to True if using HTTPS
)


def create_bucket_if_does_not_exist(bucket_name=_settings["bucket"]):
    """
    Creates a bucket in the S3-compatible storage if it does not exist.

    Parameters
    ----------
    bucket_name : str, optional
        The name of the bucket to create. Defaults to the value of `_settings["bucket"]`.

    Returns
    -------
    None
    """
    try:
        if not _client.bucket_exists(bucket_name):
            _client.make_bucket(bucket_name)
            logger.info(f"Bucket '{bucket_name}' created.")
        else:
            logger.info(f"Bucket '{bucket_name}' already exists.")
    except S3Error as err:
        logger.error(f"Error to create bucket {bucket_name}: {err}")
        raise err

def put(local_file_path, bucket_name=_settings["bucket"]):
    """
    Uploads a local file to a bucket in the S3-compatible storage.

    Parameters
    ----------
    local_file_path : str
        Path to the local file to upload.
    bucket_name : str, optional
        The name of the bucket to upload the file to. Defaults to the value of `_settings["bucket"]`.

    Returns
    -------
    str or None
        A unique identifier (file ID) for the uploaded file, or None if the upload fails.
    """
    file_id = str(uuid4())
    try:
        _client.fput_object(bucket_name, file_id, local_file_path)
        logger.info(f"'{local_file_path}' uploaded as '{file_id}' to bucket '{bucket_name}'.")
        return file_id
    except S3Error as err:
        logger.error(f"Error occurred while uploading: {err}")
        return None


def get(file_id, output_file, bucket_name=_settings["bucket"]):
    """
    Downloads a file from a bucket in the S3-compatible storage.

    Parameters
    ----------
    file_id : str
        The unique identifier of the file to download.
    output_file : str
        The local path where the downloaded file will be saved.
    bucket_name : str, optional
        The name of the bucket from which to download the file. Defaults to the value of `_settings["bucket"]`.

    Returns
    -------
    None
    """
    try:
        _client.fget_object(bucket_name, file_id, output_file)
        logger.info(f"'{file_id}' downloaded from bucket '{bucket_name}' into '{output_file}'.")
    except S3Error as err:
        logger.error(f"Error occurred while downloading: {err}")
