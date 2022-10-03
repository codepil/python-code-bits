GCP Logging doesn't retain more than 30 days.
    (see https://cloud.google.com/logging/quotas )
    Logger API doesn't support updating timestamp value of an log entry {not injection friendly}
    ( which means logger APIs have to used inside NDM app, and not when once tests are done)

        To get original timestamp value into the logs --> Improving the python logging by handlers
        JSON logging : https://github.com/thangbn/json-logging-python

so historic analysis of logs with BigQuery, by exporting.

Light weight approach:
https://developers.cloudflare.com/logs/tutorials/analyze-logs-gcp/
(storage -> cloud fn -> big table -> data studio)


Use case 1:  searching for failures across logs (NDM, device) and how often
    Logging search strings like "error" "failed" "testDeviceError" (and walk through log entry semantics, and pick run_number) or "gsutil" or "failed to obtain build"
    (its better to select the test or field from UI and add "show matching entries" )
        failed
        jsonPayload.run_number=75
        jsonPayload.devicelog.timestamp >= "2018-11-17 22:27" OR jsonPayload.ndmlog.timestamp >= "2018-11-17 22:27"
    resource.type="global"  "wrote"

    resource.type="global"  "wrote"
    logName="projects/pavan-test-project-from-test/logs/agatehl1-002c-test_0000_upgrade_to_latest_verified_forced.log"
    jsonPayload.devicelog.command="NDM-M"
    timestamp>="2019-02-21T18:10:06.239632202Z"

Use case 2: plot time taken for perticular NDM device operation
    Say for example AgateHL factory reset
    https://datastudio.google.com/u/0/reporting/1pGOZngfvHvXWD2kWbpI8bbUhZqrUGG2B/page/STzi
    (place the ndm log as 2ndm.log, and agate log, and run inject_log_entries.py file)
    (it logs onto stack driver logging, exported to big query, query results are view in data studio)

https://console.cloud.google.com/logs/viewer?project=pavan-test-project-from-test&minLogLevel=0&expandAll=false&timestamp=2019-03-08T15%3A20%3A02.362000000Z&customFacets=jsonPayload.uuid%2CjsonPayload.line_number%2CjsonPayload.message&limitCustomFacetWidth=false&dateRangeStart=2019-03-07T17%3A11%3A41.951Z&dateRangeEnd=2019-03-07T23%3A11%3A41.951Z&interval=CUSTOM&scrollTimestamp=2019-03-07T18%3A20%3A21.872497312Z&advancedFilter=resource.type%3D%22global%22%0Aresource.labels.project_id%3D%22pavan-test-project-from-test%22%0Atimestamp%3D%222019-03-07T18%3A20%3A18.731251482Z%22%0AinsertId%3D%2217at2yufzof2ub%22

Simple -->

https://console.cloud.google.com/logs/viewer?project=pavan-test-project-from-test&interval=NO_LIMIT&expandAll=true&advancedFilter=resource.type%3D%22global%22%0AinsertId%3D%2217at2yufzof2ub%22