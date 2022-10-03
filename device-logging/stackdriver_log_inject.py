# Imports the Google Cloud client library
from google.cloud import logging
import os, glob, sys, re

# set service account file path to gcloud env
logging_client = logging.Client()

run_number = sys.argv[1] #should be UUID, from argument 1
log_path = sys.argv[2] + "/*.log"

for currentFile in glob.glob(log_path):
    fh = open(currentFile, 'r')
    # logger name equivalent to bedrock job name
    # 'bedrock' key at index is required to have export filter sink setup purpose
    logger = logging_client.logger("agatehl-ndm-regression")
    for line in fh:
        line.rstrip('\n')
        line_emitted = False

        if 'ndm' in currentFile:
            logline = {'ndmlog': {}, 'uuid': run_number, 'index': 'bedrock'}
            # 20181209 20:10:02.353
            logline['ndmlog']['timestamp'] = line[0:21]
            logline['ndmlog']['src_file'] = line[31:49].strip()
            logline['ndmlog']['src_line'] = line[50:54].strip() #can be combined with above
            logline['ndmlog']['message'] = line[54:].strip()
            # Writes the log entry
            logger.log_struct(logline)
            line_emitted = True

        # TODO format used in each device log is different, below code is for AgateHL device
        if 'agatehl1' in currentFile:
            logline = {'devicelog': {}, 'uuid': run_number, 'index': 'bedrock'}
            # date format 2018-11-17 22:27:21.835757
            logline['devicelog']['timestamp'] = line[1:27]
            logline['devicelog']['command'] = line[29:34]  #can be ignored, no use cases as of now.
            logline['devicelog']['message'] = line[36:].strip()
            logline['devicelog']['log_name'] = currentFile
            logline['devicelog']['device_id'] = ('-'.join(currentFile.split('-', 2)[0:2]))[5:] #remove 'logs/'
            # Writes the log entry
            logger.log_struct(logline)
            line_emitted = True

        if 'test_output' in currentFile:
            if '[Testbed-' in line:
                #[Testbed-One-Agatehl1-01] 02-11 06:13:53.412 INFO Test output folder: ...
                try:
                    if 'bedrock_db_perform_sql' in line:
                        continue
                    logline = {'testlog': {}, 'uuid': run_number, 'index': 'bedrock'}
                    logline['testlog']['timestamp'] = ' '.join(line.split()[1:3])
                    logline['testlog']['testbed_name'] = re.search('\[(.+?)\]', line).group(1)
                    logline['testlog']['message'] = ' '.join(line.split()[4:])
                    # Writes the log entry
                    logger.log_struct(logline)
                    line_emitted = True
                except AttributeError:
                    print ('Error message at line --->', line)
            else:
                logline = {'harnesslog': {}, 'uuid': run_number, 'index': 'bedrock'}
                logline['harnesslog']['message'] = line[0:].strip()
                # TODO, include run level details like sponge URL, initiator URL ? if yes then pass it as arguments
                # also modify swarming code to emit client logs on to a new file
                # Writes the log entry
                logger.log_struct(logline)
                line_emitted = True

        # TODO include job logs i.e. Jenkins console output

        if not line_emitted:
            print (currentFile, "-->", line)

    fh.close()


