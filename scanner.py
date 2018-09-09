#!/usr/bin/python3
import subprocess  	#to run ping
import time		#to wait for pings to process
import os		#to write ping results to txt file
import re		#to match IPs written to text file
import socket		#to scan for open ports

os.system("echo ''> stdout.txt")  #this writes blank over stdout.txt, for fresh ping results
s=""	#s = empty string to concat successful ping results
l=[]	#l = empty list to append successful port results

def scan(a,b):	#"scan" function passes IP & port to socket method
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((a,b))
    if result == 0:	#if socket return 0, port is open
        l.append(b)	#append open port to l (el) list


net=input("Enter an IP: ") #net=input, ex. 192.168.1.1
r=input("Octet 1 2 3 4: ") #r= octet number to cycle thru 1-254
input("You chose {}. Are you sure?".format(r)) #to help against scanning public IPs
jes=[substring.strip() for substring in net.split('.')] #jes splits IP by with "." delimiters into a list
host=1	#host=number b/w 1-254 we're gonna cycling thru

if r=="1":  #if user cycles thru 1st octet...
    for i in range(255):   #for every num(i) in range from 1-254... create an IP with... 
        ip = "{}.{}.{}.{}".format(host, jes[1], jes[2], jes[3])  #...the new host num b/w 1 & 254 in selected octet
        with open("stdout.txt","a+") as stdout:  #open stdout text and append ping results (2 pings)...
            subprocess.Popen("ping -c 2 {}".format(ip), cwd="/root/Desktop/", shell=True, stdout=stdout, stderr=stdout)
        host+=1  #and increment the host number

if r=="2":  #same as above, but for octet 2
    for i in range(255):
        ip = "{}.{}.{}.{}".format(jes[0], host, jes[2], jes[3])
        with open("stdout.txt","a+") as stdout:        
            subprocess.Popen("ping -c 2 {}".format(ip), cwd="/root/Desktop/", shell=True, stdout=stdout, stderr=stdout)
        host+=1

if r=="3":   #same as above but for octet 3
    for i in range(255):
        ip = "{}.{}.{}.{}".format(jes[0], jes[1], host, jes[3])
        with open("stdout.txt","a+") as stdout:        
            subprocess.Popen("ping -c 2 {}".format(ip), cwd="/root/Desktop/", shell=True, stdout=stdout, stderr=stdout)
        host+=1


if r=="4":  #same as above but for octet 4 (hopefully use this one the most)
    for i in range(255):
        ip = "{}.{}.{}.{}".format(jes[0], jes[1], jes[2], host)
        with open("stdout.txt","a+") as stdout:        
            subprocess.Popen("ping -c 2 {}".format(ip), cwd="/root/Desktop/", shell=True, stdout=stdout, stderr=stdout)
        host+=1

#######################

time.sleep(8)   	#sleep 8 seconds for pings to finish

filename="stdout.txt"  		#assign stdout.txt to filename
with open(filename, "r") as f:  #assign filename for reading to f
    for line in f:  		#for every line in f...
        if "64 bytes" in line:	#if line contains "64 bytes"...
            s+=line		#cat the line to s

#this grabs all the IPs that had successful pings... 
#assign regex IP matches in s to grab
grab = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", s)  
grab_list=[]	#grab_list=empty list to append regex matches
for m in grab:			#for every match (m) in grab...
    if m not in grab_list:	#if m not in grab_list...
        grab_list.append(m)	#append m to grab_list
for w in grab_list:		#for every IP (w for winner) in grab_list...
    print(w)			#print winning IP

#this lets user choose IP to port-scan...
ip = input("Type IP to scan ports: ")
#...and which ports to scan
port1= input("Type port range to scan. First port: ") #assign 1st port to scan to port1
port2= input("Type last port: ")  #assign last port to port2
#convert port1 & port2 to ints
port1n=int(port1)
port2n=int(port2)
#send n (port num) b/w port1 & port2...
for n in range(port1n,port2n):  
	scan(ip, n) #to scan function, passing in ip & port number(n)

#the scan function creates a list(l) of open ports
for o in l:  #for every open port(o) in l...
    print(o)	#print the open port