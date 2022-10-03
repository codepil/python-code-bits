import os

from google.cloud import storage

#pip install --upgrade google-cloud-storage
#export GOOGLE_APPLICATION_CREDENTIALS=google.com_home-ci-controller-staging-40d476bc974a.json

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob("uuid1/" + destination_blob_name)
    metadata = {'uuid': 'Pink', 'job_name': 'test-regression'}
    blob.metadata = metadata

    blob.upload_from_filename(source_file_name)
    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

def main():
    # parse args
    upload_blob('bedrock-logging', 'ndm.log', 'ndm.log')


if __name__ == "__main__":
    main()