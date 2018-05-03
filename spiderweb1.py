#!/usr/bin/python3

import requests
import re
import csv

def strip_proto(url):
	if "http" in url:		#REMOVE HTTP IF IT EXISTS
		url1 = url[7:]
	if "https" in url:		#REMOVE HTTPS IF IT EXISTS
		url1 = url[8:]
	if "www." in url1:		#REMOVE WWW IF IT EXISTS
		url1 = url1[4:]
	return url1	

def start_spider(website):
	headers = {"user-agent": "Mozilla/5.0"}	#HEADERS GET REQ PAST FIREWALLS
	r = requests.get('{}'.format(website), headers = headers)	
	content = r.text
	urls = re.findall('href="*.+?"', content)	#REGEX SEARCH FOR URLS
	return urls

def fix_proto(sites):
	full_url = []
	for site in sites:
		site = site[6:-1] #REMOVE HREF AND LAST "
		if "http" not in site:
			if (len(site) > 0) and (site[0] != "/"):
				site = "/" + site 
			if (len(site) > 1) and (site[1] != "/"):
				site = "http://www." + domain1 + site
				full_url.append(site)
			if (len(site) > 1) and (site[1] == "/"):
				site = "http:" + site
				full_url.append(site)
		else:
			full_url.append(site)
	return full_url

def remove_slash(with_slashes):
	no_slash = []
	for s in with_slashes:
		slash_len = len(s)
		if s[slash_len-1] == "/":
			s = s[:-1]
		no_slash.append(s)
	return no_slash

def remove_dups(dups):
	no_dup = []
	for not_dup in dups:
		if not_dup not in no_dup:
			no_dup.append(not_dup)
	return(no_dup)

def remove_anchors(has_anchors):
	no_anchors = []
	for anchor in has_anchors:
		if ("#" not in anchor):
			no_anchors.append(anchor)
	return no_anchors


def remove_outdomain(all_domains, my_domain):
	my_domains = []
	for the_domain in all_domains:
		if my_domain in the_domain:
			my_domains.append(the_domain)
	return my_domains

######################################################################################

domain = input("What domain do you want to spider? Include the protocol and make sure you have the correct address, please: ")

domain1 = strip_proto(domain)
all_urls = start_spider(domain)
full_urls = fix_proto(all_urls) #THIS WILL PUT THE URL IN CORRECT FORMAT FOR REQUESTS MODULE
noslash_urls = remove_slash(full_urls) #THIS HELPS PREVENT DUPLICATE URLS
nodup_urls = remove_dups(noslash_urls) #THIS REMOVES DUPLICATE URLS
noanchor_urls = remove_anchors(nodup_urls) #THIS REMOVES THE ANCHOR URLS
my_urls = remove_outdomain(noanchor_urls, domain1) #REMOVES URLS THAT ARE OUTSIDE THE DOMAIN

counter = 0
for x in my_urls:
	counter += 1
	print("{}.".format(counter), x)


#THIS ADDS THE URL LIST TO A MASTERLIST
masterlist = my_urls
list_length = len(masterlist)	#ASSIGNS LENGTH OF MASTER LIST TO LIST_LENGTH


print("##################################################################")
print("The above URLs are the URLs found on the first page of the domain")
print("There are {} URLs".format(list_length))
input("Hit enter to spider each URL.")

#THIS SPIDERS THE URLS IN THE MASTERLIST. SAME PROCESS AS ABOVE
list_count = 0
templist = []
for parent in masterlist:
	list_count += 1
	print ("Testing {}.".format(list_count), parent, "...")
	print("We're {0:.2f}% done...".format(list_count/list_length))
	kids = start_spider(parent)
	kids1 = fix_proto(kids)
	kids2 = remove_slash(kids1)
	kids3 = remove_dups(kids2)
	kids4 = remove_outdomain(kids3, domain1)
	kids5 = remove_anchors(kids4)
	for x6 in kids5:			#THIS FOR STATEMENT INSERTS THE UNIQUE URLS INTO A TEMPORARY LIST 
		if x6 not in masterlist:
			templist.append(x6)


masterlist = masterlist + templist	#THIS COMBINES TEMPLIST & MASTERLIST
list_length = len(masterlist)

#THIS WRITES THE MASTERLIST TO A CSV
with open("masterfile.csv", "w") as myfile:
    	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    	wr.writerow(masterlist)


input("The masterlist now contains {} URLs. Do you want to spider all those entries?".format(list_length))
print("You're crazy... No way!")