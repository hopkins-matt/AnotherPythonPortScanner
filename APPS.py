import socket
import subprocess
import sys
import time
from datetime import datetime

def spinning_cursor():
    while True:
        for cursor in '__==‾‾==':
            yield cursor

spinner = spinning_cursor()

scanFailed = False

#blank screen
subprocess.call('clear', shell=True)

#ask for domain/ip
remoteServer = input("Enter domain/ip to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)

subprocess.call('clear', shell=True)

portRangeCustom = input("Set custom port range? (Default range 1-5000) [y/n] ").lower()

yesResponse = {'y','yes','ye'}

if portRangeCustom in yesResponse:
	portRangeStart = input("Enter start port: ")
	portRangeEnd = input("Enter end port: ")
else:
	portRangeStart = 1
	portRangeEnd = 5000

portScanRange = range(int(portRangeStart), int(portRangeEnd) + 1)

subprocess.call('clear', shell=True)

#shot waiting screen with info
print("-" * 70)
print("Please wait, scanning remote host {} on ports {} to {}".format(remoteServerIP, portRangeStart, portRangeEnd))
print("-" * 70)

#set scan start time
t1 = datetime.now()


try:
	for port in portScanRange:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(0.1)

		sys.stdout.write(next(spinner))
		sys.stdout.flush()
		sys.stdout.write('\b')

		result = sock.connect_ex((remoteServerIP, port))
		if result == 0:
			print("Port {}:    Open".format(port))
		sock.close()

except KeyboardInterrupt:
	scanFailed = True
	print("\nPort Scan stopped by User")
	sys.exit()

except socket.gaierror:
	scanFailed = True
	print("\nHostname could not be resolved... Exiting")
	sys.exit()

except socket.error:
	scanFailed = True
	print("\nCouldn't connect to server... Exiting")
	sys.exit()

#set scan end time
t2 = datetime.now()

totalScanTime = datetime.utcfromtimestamp((t2 - t1).total_seconds())
totalScanTime = totalScanTime.strftime("%H:%M:%S").split(":")

if int(totalScanTime[0]) > 0:
	displayFinalTime = totalScanTime[0] + " hours, " + totalScanTime[1] + " minutes, and " + totalScanTime[2] + " seconds"
elif int(totalScanTime[1]) > 0:
	displayFinalTime = totalScanTime[1] + " minutes, and " + totalScanTime[2] + " seconds"
elif int(totalScanTime[2]) > 0:
	displayFinalTime = totalScanTime[2] + " seconds"
else:
	displayFinalTime = "a few milliseconds"

if scanFailed != True:
	print('Port scan completed in ', displayFinalTime)
else:
	print('Scan Failed')
