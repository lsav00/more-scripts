#!/usr/bin/python

#One shot search of entries in apache access.log containing 404. Earliest and latest event times are specified.  The results are printed out.

import splunklib.results as results
import splunklib.client as client

HOST= "localhost"
PORT= 8089
USERNAME = "admin"
PASSWORD= "**************"

# Create a Service instance and log in
service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD
    )

kwargs_oneshot = {"earliest_time": "2018-05-09T10:00:00.000-04:00", "latest_time": "2018-05-09T12:00:00.000-04:00"}
searchquery_oneshot = "search index=main source=/var/log/apache2/access.log 404"

oneshotsearch_results = service.jobs.oneshot(searchquery_oneshot, **kwargs_oneshot)

# Get the results and display them using the ResultsReader
reader = results.ResultsReader(oneshotsearch_results)
counter = 0
for item in reader:
    counter +=1
    print(item, counter)
