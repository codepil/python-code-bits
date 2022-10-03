
import json
import os


def get_uuid(log_path):
    uuid = None
    if (os.path.isfile(log_path + '/steps_log.json')):
        lines = open(log_path + '/steps_log.json').readlines()
        for line in lines:
            doc = json.loads(line)
            if doc['step_id'] == "uuid":
                uuid = doc['info']
                break
    return uuid

def parse_harness_result_file(log_path="."):
    # parse harness results json for hostname
    metadata_doc = {}
    if (os.path.isfile(log_path + '/results.json')):
        doc = json.load(open(log_path + '/results.json'))
        # extract entries required
        for item in doc.values()[0]["results"]["bot_dimensions"]:
            #print item
            if item["key"] == "hostname":
                metadata_doc["lab_server_machine_name"] = item["value"][0]

    # extract ndm version
    if (os.path.isfile(log_path + '/ndm_version.txt')):
        metadata_doc['ndm_version'] = open(log_path + '/ndm_version.txt').readline().rstrip('\n')


    metadata_doc['uuid'] = get_uuid(".")

    return metadata_doc

if __name__ == "__main__":
    print(parse_harness_result_file())
