#!/bin/bash

#This script makes a copy of user-specified files and appends "bak- 'date & time'" to filenames. Can be a data exfiltration tool. 


x=$(date)					#assign date & time to x
echo "Current time: $x"
echo -n "What file do you want to back up?"	#prompt user input
read filename					#read input & assign to filename
path=$(find $HOME -name $filename)		#finds the file & assigns to path
if [ -e "$path" ]				#checks if file exists
then
	echo "That file exists.  Now backing up $path into Backups."
	if [ ! -x "$HOME/Desktop/Backups" ] 	#if Backups dir doesn't exist
	then 
		mkdir "$HOME/Desktop/Backups"	#...make a Backups dir
		cp "$path" "$HOME/Desktop/Backups/$filename(bak-$x)"	#...and copies file to Backups dir, appending "bak with x to the filename
	else					#if Backups exists, copy file same as above
		cp "$path" "$HOME/Desktop/Backups/$filename(bak-$x)"
	fi					#closes the child condition
else						#if file doesn't exist, display message to user
		echo "That file does not exist."
fi						#closes the parent condition
exit
