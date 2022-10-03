"""
Create the script to start the swarming bots.
This reads the yaml testbed config to pull all the needed info.
"""

import argparse
import collections
import os
import glob
import json
import yaml

def get_yml_files(config_dir):
  dir_path = os.path.abspath(config_dir)
  p = dir_path + "/*.yml"
  file_list = glob.glob(p)
  return file_list



def convert_files_to_dict(file_list):
  configs={}
  for f in file_list:
    with open(f, "r") as j:
      data = yaml.safe_load(j)
      configs[f] = data
  return configs


def convert_to_bot_dir_name(testbed):
  return testbed + '-bot'


def _get_device_ids(config_list):
  """Read the yaml file, and return a python dict
  {'Testbed-One-Pinna1-01': ['pinna-00vc','pinna-002'}
  """
  devices_list = {}
  assert isinstance(config_list, collections.Sequence), ' yaml config not a list'
  for config in config_list:
    if not {'testBrilloDevice', 'testDevice'} & set(config['Controllers'].keys()):
      raise KeyError('testDevice or testBrilloDevice not found in test yaml config file')
    name = config['Name']
    devices_list[name] = []
    for key, controller_list in config['Controllers'].iteritems():
      if key in ['testBrilloDevice', 'testDevice']:
        for entry in controller_list:
          if isinstance(entry, dict):
            entry = entry['id']
          devices_list[name].append(entry)
  return devices_list

def convert_files_to_dict(file_list):
  configs={}
  for f in file_list:
    with open(f, "r") as j:
      data = yaml.safe_load(j)
      configs[f] = data
  return configs


def convert_to_bot_dir_name(testbed):
  return testbed + '-bot'


def _get_device_ids(config_list):
  """Read the yaml file, and return a python dict
  {'Testbed-One-Pinna1-01': ['pinna-00vc','pinna-002'}
  """
  devices_list = {}
  assert isinstance(config_list, collections.Sequence), ' yaml config not a list'
  for config in config_list:
    if not {'testBrilloDevice', 'testDevice'} & set(config['Controllers'].keys()):
      raise KeyError('testDevice or testBrilloDevice not found in test yaml config file')
    name = config['Name']
    devices_list[name] = []
    for key, controller_list in config['Controllers'].iteritems():
      if key in ['testBrilloDevice', 'testDevice']:
        for entry in controller_list:
          if isinstance(entry, dict):
            entry = entry['id']
          devices_list[name].append(entry)
  return devices_list


def common_env_vars():
    lines = list()
    lines.append('')
    lines.append("HOSTNAME=`hostname`")
    lines.append("export IP_ADDR=`hostname -I`")
    lines.append("export CHECK_TESTBED_NAME_IN_BOT_ID='true'")
    lines.append("export CHECK_TESTBED_TYPE_IN_BOT_ID='true'")
    lines.append("export TESTBED_HEALTH_CHECK='true'")
    lines.append("export TESTBED_HEALTH_CHECK_VERBOSE='true'")
    lines.append(
        """export EXTRA_BOT_DIMS='"ip_addr": ["'${IP_ADDR::50}'"], "hostname": ["'${HOSTNAME::128}'"] , "team": [ "NEP" ], "deployment_stage": [ "canary" ]' """)
    lines.append('')
    return lines


def convert_yml_dict_to_bash(yml_file_name, configs):
    # Convert the OnePinna.yml dict to the env vars
    all_lines = list()
    for config in configs:
        lines = list()
        lines.append("# from yaml file : {0}".format(yml_file_name))
        testbed_name = config['Name']
        lines.append('cd ' + convert_to_bot_dir_name(testbed_name))
        lines.append('export TESTBED_NAME={0}'.format(testbed_name))

        ids = _get_device_ids([config])
        assert len(ids.keys()) == 1
        ids_list = ids.values()[0]
        ids_str = json.dumps(ids_list)
        testbed_type = os.path.splitext(os.path.basename(yml_file_name))[0]
        lines.append('export SWARMING_BOT_ID=$HOSTNAME-' + config['Name'])
        lines.append(
            """export BOT_DIMENSIONS='{'${EXTRA_BOT_DIMS}', "testbed_type": [\"""" + testbed_type + """\"] }'""")
        lines.append("export TESTBED_HEALTH_CHECK_DEVICE_IDS=\'" + ids_str + "\'")
        lines.append("nohup python swarming_bot.zip > ../" + config['Name'] + "-bot.log &")
        lines.append('cd ..')
        lines.append('')
        # export SWARMING_BOT_ID=bedrock-prod-experimental1-$TESTBED_NAME
        all_lines.extend(lines)

    return all_lines

def main():
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("yml_config_dir")
    parser.add_argument("output_file")
    args = parser.parse_args()

    files = get_yml_files(args.yml_config_dir)

    bash_script = []
    testbed_names = []
    bash_script.extend(common_env_vars())

    ymls = convert_files_to_dict(files)
    # Read each testbed in each yaml file, convert to bash
    for yml_file_name, configs in ymls.iteritems():
        bash_script.extend(convert_yml_dict_to_bash(yml_file_name, configs))
        # Could have many testbeds in one file
        for config in configs:
            testbed_names.append(config['Name'])

    # Add code to create the bot dir to the top of the file
    for testbed_name in testbed_names:
        bash_script.insert(0, '# cp -r base_bot ' + convert_to_bot_dir_name(testbed_name))
    bash_script.insert(0, '# Follow bootstrapping notes to create base_bot https://cast-swarming.appspot.com ')
    bash_script.insert(0, '# Run by hand to create the bot dirs, one per bot is needed')

    # Write to the file
    with open(args.output_file, 'w') as f:
        f.write('\n'.join(bash_script))


if __name__ == "__main__":
    main()