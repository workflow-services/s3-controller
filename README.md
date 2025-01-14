# s3-controller

VERY Simple package to manipulate files on S3-based object stores (e.g., MinIO).

## Install

pip install git+https://github.com/workflow-services/s3-controller

## Utilization

1. Define the environment variables:

```
MINIO_URI=localhost:9000
MINIO_ROOT_USER=
MINIO_ROOT_PASSWORD=
MINIO_BUCKET=test_bucket
```

2. Use it in your python script

```python
from s3_controller import get, put, create_bucket_if_does_not_exist

create_bucket_if_does_not_exist()

file_id = put('/path/to/file.txt')

get(file_id, '/path/to/output_file.txt')
```
