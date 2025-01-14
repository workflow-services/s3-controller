import os
import tempfile
from s3_controller import put, get, create_bucket_if_does_not_exist

# Test case for uploading and downloading a file from MinIO
def test_minio_file_operations():
    # Step 1: Write a dummy text file
    test_content = "This is a test file content."
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        local_file_path = temp_file.name
        temp_file.write(test_content.encode('utf-8'))
        temp_file.close()

    try:
        # Step 2: Upload this file to MinIO
        file_id = put(local_file_path)
        assert file_id is not None, "File upload failed."

        # Step 3: Download the file back from MinIO
        output_file = tempfile.NamedTemporaryFile(delete=False)
        output_file.close()  # Close the temporary file before using it

        get(file_id, output_file.name)

        # Step 4: Assert that the content of the file is the same
        with open(output_file.name, 'r') as f:
            downloaded_content = f.read()

        assert downloaded_content == test_content, "Downloaded content does not match uploaded content."
        print("Test successfuly. downloaded_content == test_content")

    finally:
        # Clean up: Delete the local files after the test
        os.remove(local_file_path)
        os.remove(output_file.name)


def assert_env_vars():
    required_env_vars = [
        "MINIO_URI",
        "MINIO_ROOT_USER",
        "MINIO_ROOT_PASSWORD",
    ]
    for var in required_env_vars:
        if var not in os.environ:
            raise EnvironmentError(f"Required environment variable '{var}' is not defined.")
        else:
            print(f"Environment variable '{var}' is defined.")


if __name__ == "__main__":
    assert_env_vars()
    create_bucket_if_does_not_exist()
    test_minio_file_operations()
