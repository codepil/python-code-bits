from google.cloud import logging
import json
from datetime import datetime
import time
import pytz
from google.cloud import logging_v2
from google.cloud.logging.resource import Resource

# https://cloud.google.com/logging/docs/api/v2/resource-list
# generic_task works
_BEDROCK_RESOURCE = Resource(type="generic_task", labels={
            "project_id": "bedrock",
            "job": "job.value1..",
            "namespace": "ndm.log",
            "location": "any ..",
            "task_id": "uuid1.."},)

_GLOBAL_RESOURCE = Resource(type="global", labels={
            "project_id": "pavan-test-project-from-test",
            "key1": "value1.." },)

logLabels = {"key1": "test....", "key2": "test2...."}

logging_client = logging.Client()
logger = logging_client.logger(name='my-batch-log')


logline = {}
logline['log'] = {}
logline['log']['message'] = "value1 is really big that goes till end of this line which is 80 charecter length.. blalall"
now = datetime.utcnow()

# indexed fields
# https://cloud.google.com/logging/docs/view/advanced-filters#indexed-fields
with logger.batch() as batch:
    batch.log_text('Issue #7457', timestamp=now)
    batch.log_struct(logline, timestamp=now, resource=_BEDROCK_RESOURCE, labels=logLabels)
