#!/usr/bin/env bash

echo "Creating Virtual Environment for log Injection"
log_env="log_env"
if [[ ! -e $log_env ]]; then
    /usr/local/bin/virtualenv "$log_env"
    "$log_env"/bin/python "$log_env"/bin/pip install --upgrade google-cloud-logging
fi

#source "$log_env"/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS="./PavanTestGCPkey.json"

mkdir -p logs
# cp ndm & test logs to ./logs directory
cp demo/logs/*.log logs
"$log_env"/bin/python stackdriver_log_inject.py 123456789 logs
rm -rf logs