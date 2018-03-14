#!/usr/bin/env python
# Requirements: python-dateutil, numpy, requests

from __future__ import print_function
from collections import defaultdict, namedtuple
import csv
import dateutil.parser
import json
import numpy
import re
import requests
import subprocess
import os
from datetime import datetime

from wpt_common import CUTOFF, QUARTER_START, fetch_all_prs, wpt_git

RUNS_URL='https://wpt.fyi/api/runs?max-count=100'
CSV_FILE = 'wpt-dashboard-latency.csv'

GH_USER = os.environ.get('GH_USER')
GH_TOKEN = os.environ.get('GH_TOKEN')
GH_AUTH = (GH_USER, GH_TOKEN) if (GH_USER and GH_TOKEN) else None
if GH_AUTH is None:
    print('This script will fail without GitHub authentication. Exiting')
    print('Get your token from here: <https://github.com/settings/tokens>')
    exit()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_latencies(prs, runs):
    """For each PR, find the earliest run for each browser that included that PR,
    and calucate the latencies between the PR and the runs."""


    i=0
    for pr in prs:
        #run_time = filter(lambda run: run['revision'] == pr['merge_commit_sha'][0:9], runs)
        foo = pr['merge_commit_sha'][0:10]
        
        for run in runs:
                  
            if run['revision'] == foo:
                #print ('SHA: ' + 'https://wpt.fyi/?sha=' + foo)
                #print (pr['created_at'] - run['created_at'])
                prtime = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
#                prtime = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                runtime = datetime.strptime(run['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                #print (" PR made at: " + prtime.strftime("%Y-%m-%d %H:%M"))
                #print ("Run made at: " + runtime.strftime("%Y-%m-%d %H:%M"))
                age = runtime - prtime
                rounded = round(age.total_seconds() / 3600,2)
                if rounded > 12:
                    print (foo + " " + bcolors.FAIL + str(rounded) + " hours" + bcolors.ENDC)
                else: 
                    print (foo + " " + bcolors.HEADER + str(rounded) + " hours" + bcolors.ENDC)
                    
                
        #cars = [run for run in runs if run['revision'] == foo]

        #print (foo)

        # print (len(cars))

        # for x in cars:
        #     print (x)
        #     for y in cars[x]:
        #         print (y,':',cars[x][y])

        
    #     print (foo)
    #     print (i)
    #     i += 1
    #     #print (', '.join(run_time))


    # for run in runs:
    #     foo = run['revision']
    #     print ("wpt " + foo)
    
    latencies = {}
    return latencies


def main():
    prs = fetch_all_prs()
    runs = requests.get(RUNS_URL).json()
    latencies = get_latencies(prs, runs)
    print(latencies)


if __name__ == '__main__':
    main()
