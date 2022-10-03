# Imports the Google Cloud client library
from google.cloud import logging
from google.cloud.logging.resource import Resource
from random import randint
from datetime import datetime
from datetime import datetime
from pytz import timezone
import time
import os, glob
import yaml, json

# set service account file path to gcloud env
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/bijjalap/PycharmProjects/gcp-logging/PavanTestGCPkey.json"
run_number = randint(0,99)

# Instantiates a client
resource = Resource(type="global", labels={"project_id": "run_number", "region": "yourFunctionLocation"},)
logging_client = logging.Client()

if os.path.isfile('metadata.json'):
    metadata_doc = json.load(open("metadata.json"))
    test_summary = yaml.safe_load_all(open("test_summary.yaml"))
    ndm_remedy_hints = json.load(open("ndm_remedy_hints.json"))

    logger = logging_client.logger("metadata")
    for rec in test_summary:
        rec.update(metadata_doc)
        # update with UUID, 'bedrock' index, URLs, job ..etc. Get Test Bed details if we can
        try:
            if rec["Result"] == "FAIL":
                for key in ndm_remedy_hints:
                    if key in rec["Details"] :
                        rec["failed_pattern"] = key
                        rec["remedy"] = ndm_remedy_hints[key]
                logger.log_struct(rec, severity='ERROR')
            else:
                logger.log_struct(rec)
        except KeyError:
            logger.log_struct(rec)
            pass
else:
    print("not able to find metada file")


for currentFile in glob.glob("*.log"):
    fh = open(currentFile, 'r')

    # Selects the log to write to
    logger = logging_client.logger(currentFile)

    for line in fh:
        line.rstrip('\n')

        if 'agatehl1' in currentFile:
            logline = {'devicelog': {}, 'run_number': run_number}
            # date format 2018-11-17 22:27:21.835757
            logline['devicelog']['timestamp'] = line[1:27]
            logline['devicelog']['command'] = line[29:34]  #optional, no use cases as of now.
            logline['devicelog']['message'] = line[36:].strip()
            # Writes the log entry
            logger.log_struct(logline, resource=resource, severity='ERROR', labels=logline)

        if 'ndm' in currentFile:
            logline = {'ndmlog': {}, 'run_number': run_number}
            # 20181209 20:10:02.353
            logline['ndmlog']['timestamp'] = line[0:21]
            datetime_obj = datetime.strptime(logline['ndmlog']['timestamp'], '%Y%m%d %H:%M:%S.%f')
            datetime_obj_pst = datetime_obj.replace(tzinfo=timezone('US/Pacific'))
            logline['ndmlog']['src_file'] = line[31:49].strip()
            logline['ndmlog']['src_line'] = line[50:54].strip() #can be combined with above
            logline['ndmlog']['message'] = line[54:].strip()
            # Writes the log entry
            logger.log_struct(logline, resource=resource, severity='INFO', timestamp=datetime_obj_pst.astimezone(timezone('UTC')))

        # TODO, include run level details like sponge URL, initiator URL ? or should we have another space for cloudSQL
        # TODO, include test case level (pass/fail, error) details from mobly test logs ? or should we have another space for cloudSQL
        # job logs (cloudSQL) and harness logs (BOT stats) are not required to be parsed

        print (line)

    fh.close()

# alt way

# Use setup helper method which attaches stackdriver logger to python root logger
logging_client.setup_logging()
# import the py standard logging
import logging
log_filename = 'agatehl1-002c-test_0000_upgrade_to_latest_verified_forced.log'
# Use the standard library methods to writes the log entries
logger = logging.getLogger(log_filename)  #FIXME, still logName doesn't change
#TODO, have to modify timestamp for below log lines
logger.info("Info message from py logger")
logger.warn("Warning from py logger!")
logger.error("Error from py logger!!")
logger.critical("Critical msg from py logger. Urgent Action required!!!")


# alt way, via handlers
# this helps inject 'timestamp' value from original log into stack driver

# alt way, via cloud function (invoking this module)
# this helps wrt scalability, keeping bedrock run scripts light

