#!/usr/bin/python3

"""
Automates blacklist web request and checking Apache access log against blacklist. 
"""

import requests
import re
import os

#USE REQUEST MODULE TO GET THE BLACKLIST
headers = {"user-agent": "Mozilla/5.0"}
url = 'https://myip.ms/files/blacklist/general/full_blacklist_database.zip'
r = requests.get(url, allow_redirects=True, headers = headers)
open('blacklistzip.zip', 'wb').write(r.content)

#UNZIP THE BLACKLIST ZIP FILE
os.system("unzip -o blacklistzip.zip")

#OPEN THE APACHE LOG AND APPEND THE IPs TO A TEST_LIST
with open("/var/log/apache2/access.log.1") as f:
	lines = f.read()
	test = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", lines)
	test_list = []
	for t in test:
		if t not in test_list:
			test_list.append(t)
	f.close()

#OPEN THE BLACKLIST DATABASE AND CHECK IF ANY IPs IN TEST_LIST ARE IN THE BLACKLIST
with open("/root/Desktop/full_blacklist_database.txt") as g:
	blacklist_lines = g.read().splitlines()
	for ip in test_list:
		for threats in blacklist_lines:
			if ip in threats:
				print("WARNING: apache2 access.log.1 has been accessed by a blacklisted IP: ")
				print(threats)
		else:
			print("No blacklist IPs in apache2 access.log.1")
	g.close()


