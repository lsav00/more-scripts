#!/usr/bin/python3
import subprocess
"""
Stops script after 50,000th attempt (line 32)
"""

#this reads from the wordlist and assigns to variable "plist"
with open("wordlist") as f:
	plist = f.read().splitlines() 


c=0 #this is the counter for iterating the wordlist. 
#At 20000 b/c re-ran script every ~10,000th attempt & reinitialized

for i in plist:  #this loops through each item in the wordlist
	pz=plist[c]	#this assigns each wordlist item to variable "pz" 
	print("Testing",pz)  #prints pz to verify what's being tested
	print("Number of attempts: ", c)  #prints c to verify num of attempts
	#file22 below is the name of the encrypted file
	proc = subprocess.Popen(('openssl', 'aes-256-cbc', '-d', '-in', 'file22','-a','-k', '{}'.format(pz)), stderr=subprocess.PIPE, stdout=subprocess.PIPE)	
#above code runs openssl with decrypt cmd & injects wordlist items ("pz")
#also assigns subprocess output to variables "stderr" and "stdout"
	output = proc.stderr.read()	#assigns STDERR to variable "output"
	output1=proc.stdout.read()	#assigns STDOUT to variable "output1"
	print("STDERR: ", output)	#prints STDERR
	print("STDOUT: ", output1)	#prints STDOUT
	output2 = ''.join(map(chr, output))	#cleans up STDERR & assigns to "output2"
	print("Output2: ", output2)		#prints output2
	print("Output2 length: ", len(output2))	#prints length of output2
	print("STDOUT length: ", len(output1))	#prints length of STDOUT
	print()					#prints a blank line for easier analysis
	if c == 500000:	#stops script after 50,000th attempt
		exit()
	elif (len(output2) == 0) and (len(output1) <= 25): #if STDERR length is 0 and STDOUT length is less than 25, then reached a possible solution & exit.
		exit()
	else:	#if above conditions not met, continue iterating through poss. pw's.
		c+=1
