from google.cloud import storage
from google.cloud import logging
import json
from datetime import datetime
import time
import pytz

#pip install --upgrade google-cloud-storage
#export GOOGLE_APPLICATION_CREDENTIALS=google.com_home-ci-controller-staging-40d476bc974a.json

def read_blob(bucket_name, source_file_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(source_file_name)

    print('Blob: {}'.format(blob.name))
    print('Metadata: {}'.format(blob.metadata))
    print(blob.metadata['job_name'])

    cloud_client = logging.Client()
    logger = cloud_client.logger(blob.metadata['job_name'])

    for line in blob.download_as_string().splitlines():
        logline = eval(line)
        try:
            ts = logline['timestamp']  # date format 2018-11-17 22:27:21.835757
            ts_pst = pytz.timezone("America/Los_Angeles").localize(datetime.strptime(ts, '%Y-%m-%d %H:%M:%S.%f'))
            ts_utc = ts_pst.astimezone(pytz.utc)
            with logger.batch() as batch:
                batch.log_struct(logline, timestamp=ts_utc)
        except Exception as e:
            print ("Error in injecting line --> ", str(e))
            pass

        print logline


def main():
    # parse args
    read_blob('bedrock-logging', '142b8ec6-6246-11e9-9f11-aa000101b5dd/pinna-00vt-test_1004_get_firmware_version.log')


if __name__ == "__main__":
    main()