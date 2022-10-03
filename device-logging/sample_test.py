# Imports the Google Cloud client library
from google.cloud import logging
import json
from datetime import datetime
import time
import pytz
from google.cloud import logging_v2
from google.cloud.logging.resource import Resource


_GLOBAL_RESOURCE = Resource(type="global", labels={
            "project_id": "pavan-test-project-from-test",
            "key1": "value1.."
})

logLabels = {"key1": "test....", "key2": "test2...."}
# Add a structured log entry (https://cloud.google.com/logging/docs/structured-logging)
# https://github.com/googleapis/google-cloud-python/issues/7457  --> recomend to use batch class instead of API/protobuf
# 20190226 06:10:27.365
from google.protobuf.struct_pb2 import Struct
logline = Struct()

# Instantiates a client
logging_client = logging.Client()
logger = logging_client.logger(name='my-batch-log')


logline = {}
logline['log'] = {}
logline['log']['message'] = "value1 is really big that goes till end of this line which is 80 charecter length.. blalall"
now = datetime.utcnow()
# 20190226 06:10:27.365  --> %Y
ts = datetime.strptime('20190410 19:31:27.373', '%Y%m%d %H:%M:%S.%f') # --> takes it as UTC and show as PDT(system timezone) in SD
# 2019-02-26 06:10:30.100836
ts = datetime.strptime('2019-04-10 20:10:30.100836', '%Y-%m-%d %H:%M:%S.%f') # --> takes it as UTC and show as PDT(system timezone) in SD
ts_pst = pytz.timezone("America/Los_Angeles").localize(ts)
ts_utc = ts_pst.astimezone(pytz.utc)  #--> after conversion this works, now SD shows as PST
with logger.batch() as batch:
    batch.log_text('Issue Pre-Pavan 2', timestamp=ts_utc)

res = {"type": "global",
       "labels": {
          "project_id": "pavan-test-project-from-test1",
          "key1": "value1.." }}

with logger.batch() as batch:
    batch.commit()

with logger.batch() as batch:
    batch.log_text('Issue Pre-Pavan 3', timestamp=ts_utc)

for x in range(1):
    now = datetime.utcnow()

    with logger.batch() as batch:
        batch.log_text('Issue #7457', timestamp=now)
        batch.log_struct(logline, timestamp=now, resource=_GLOBAL_RESOURCE)

with logger.batch() as batch:
    batch.commit()

entries = []


# Add a plain text log entry
logEntry = {"text_payload": "abc YOUR MESSAGE BLAH"}
entries.append(logEntry)

# write a batch of logs to Stackdriver.
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# The name of the log to write to
log_name = 'my-log'
logger = logging_client.logger(log_name)

# The data to log
text = 'Hello, world!'
json_text = {"key1": "value1"}

# Writes the log entry
logger.log_text(text)
now = datetime.now()
ts = datetime.fromtimestamp(1500000000)
ts_object = time.time()


print('Logged: {}'.format(text))