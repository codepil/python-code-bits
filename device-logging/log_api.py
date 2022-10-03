import pprint
import sys
from apiclient.discovery import build
from google.cloud import logging_v2

api_key = sys.argv[1]

service = build('logging', 'v2', developerKey=api_key)

client = logging_v2.LoggingServiceV2Client()
entries = []
response = client.write_log_entries(entries)