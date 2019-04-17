#!/usr/bin/env python3

import sys
import os
import argparse
import netifaces as ni
import socket
import re
import subprocess
import colorama
from colorama import Fore, Back, Style


# Python Script that will be an all-in-one network and system tool
#
# Features
# -Networking: IPv4&6 IP addr (priv,public), mac, broadcast, interfaces, cidr, routing, RX and TX packets
# -System: Hostname, CPU, RAM, Disk Space, OS, Kernel, uptime
#


#REGEX
ip6regex = r"(?:^|(?<=\s))(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))(?=\s|$ )"
ipregex = r"inet\s\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
macregex = r"link/ether\s[a-fA-F0-9:]{17}|[a-fA-F0-9]{12}$"
inet4regex = r"^\s\s\s\sinet\s.*"
inet6regex = r"^\s\s\s\sinet6\s.*"
cidrregex = r"/\d{1,3}"
broadcastregex = r"brd\s\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
quitwords = ["quit", "q", "Q", "Quit"]



def main():

	parser = argparse.ArgumentParser(description='Script to display networking and host information')

	parser.add_argument("-c","--credits",
						 help='Display Credits',
						 required=False,
						 action='store_true'
						 )


	parser.add_argument("-a","--allnetworking",
						 help='Display general networking info',
						 required=False,
						 action='store_true'
						 )


	parser.add_argument("-s","--networkstats",
						 help='Display networking stats',
						 required=False,
						 action='store_true'
						 )

	parser.add_argument("-sc","--subnetchart",
						 help='Display subnets chart',
						 required=False,
						 action='store_true'
						 )

	parser.add_argument("-i","--sysinfo",
						 help='Display host info with screenfetch',
						 required=False,
						 action='store_true'
						 )

	parser.add_argument("-r","--routing",
						 help='Display routing table',
						 required=False,
						 action='store_true'
						 )

	parser.add_argument("-e","--everything",
						 help='Displays all Information',
						 required=False,
						 action='store_true'
						 )


	args = parser.parse_args()

	if args.credits:
		Credits()
		sys.exit(0)

	if args.allnetworking:
		Networking()
		sys.exit(0)

	if args.networkstats:
		NetworkStats()
		sys.exit(0)

	if args.subnetchart:
		SubnetChart()
		sys.exit(0)

	if args.sysinfo:
		SysInfo()
		sys.exit(0)

	if args.routing:
		RoutingTable()
		sys.exit(0)

	if args.everything:
		Credits()
		Networking()
		RoutingTable()
		SubnetChart()
		NetworkStats()
		SysInfo()
		sys.exit(0)

	else:
		Credits()
		sys.exit(0)	



def Credits():

	title = ("""

   _____  _            _      _   _   _        _                          _     
  / ____|| |          (_)    ( ) | \ | |      | |                        | |     
 | |     | |__   _ __  _  ___|/  |  \| |  ___ | |_ __      __ ___   _ __ | | __  
 | |     | '_ \ | '__|| |/ __|   | . ` | / _ \| __|\ \ /\ / // _ \ | '__|| |/ /  
 | |____ | | | || |   | |\__ \   | |\  ||  __/| |_  \ V  V /| (_) || |   |   <   
  \_____||_| |_||_|   |_||___/   |_| \_| \___| \__|  \_/\_/  \___/ |_|   |_|\_\  
  _______             _  _                                                      
 |__   __|           | || |                                                     
    | |  ___    ___  | || |__    ___ __  __                                     
    | | / _ \  / _ \ | || '_ \  / _ \\ \/ /                                      
    | || (_) || (_) || || |_) || (_) |>  <                                       
    |_| \___/  \___/ |_||_.__/  \___//_/\_\                                      
                                                                                
                                                                               
""")

	params = ("""
-c, --credits        Display Credits
-a, --allnetworking  Display general networking info
-s, --networkstats   Display networking stats
-sc,--subnetchart    Display subnets chart
-i, --sysinfo        Display host info with screenfetch
-r, --routing        Display routing table
-e, --everything     Displays all Information


		""")


	print(Style.BRIGHT+ Fore.CYAN + title + Style.RESET_ALL)


	print("Made by Chris Morris")
	print("github.com/chriswmorris")
	print()
	print("Displays stats and information about:")
	print()
	hostname = socket.gethostname()
	print("---->  " + Style.BRIGHT + Fore.BLUE + hostname + Style.RESET_ALL + "  <----" )
	print()
	print()
	print(Style.BRIGHT + "Possible Parameters" + Style.RESET_ALL)
	print(params)



def Networking():


	networkingtitle= (
	"""
  _  _       _                      _    _             
 | \| | ___ | |_ __ __ __ ___  _ _ | |__(_) _ _   __ _ 
 | .` |/ -_)|  _|\ V  V // _ \| '_|| / /| || ' \ / _` |
 |_|\_|\___| \__| \_/\_/ \___/|_|  |_\_\|_||_||_|\__, |
                                                 |___/ 
"""
)

	print(Style.BRIGHT + Fore.GREEN + networkingtitle + Style.RESET_ALL)

	#Public IPv4 address
	try:
		print()
		pubipv4 = subprocess.Popen(['/usr/bin/dig','+short', 'myip.opendns.com','@resolver1.opendns.com'], stdout=subprocess.PIPE).communicate()[0]
		pubipv4 = pubipv4.decode('utf-8')
		pubipv4 = ''.join(pubipv4)
		print(Style.BRIGHT + "Public IPv4 Address" + Style.RESET_ALL)
		print(Fore.GREEN + pubipv4 + Style.RESET_ALL)

	except:
		pass

	for interface in ni.interfaces():

		print("")
		linkstate = subprocess.Popen(['/bin/ip','link','show', interface], stdout=subprocess.PIPE).communicate()[0]
		linkstate = linkstate.decode('utf-8')


		if not "state DOWN" in linkstate:

			if interface == "lo":
				pass
			
			else:
				
				print(Style.BRIGHT + Fore.GREEN + interface + " | Status: UP" + Style.RESET_ALL)
				

			#IPV4
			try:
				if interface == "lo":
					pass

				else:
					ifconfigs = subprocess.Popen(['/bin/ip','address','show', interface], stdout=subprocess.PIPE).communicate()[0]
					ifconfigs = ifconfigs.decode('utf-8')
					ipaddrs = re.findall(ipregex, ifconfigs)
					ipaddrs = ''.join(ipaddrs)
					ipaddrs = ipaddrs.replace("inet ", "")
					print("    IPV4 Address: " + Style.BRIGHT + ipaddrs + Style.RESET_ALL)

			except:
				pass

			#IPv4 CIDR and Subnet Masks
			try:	
				if interface == "lo":
					pass

				else:
					cidrs = subprocess.Popen(['/bin/ip','address','show', interface], stdout=subprocess.PIPE).communicate()[0]
					cidrs = cidrs.decode('utf-8')
					cidredit = re.sub(inet6regex,"",cidrs, flags=re.MULTILINE)
					inet4cidr = re.findall(cidrregex, cidredit)
					inet4cidr = ''.join(inet4cidr)
					print("    IPV4 CIDR: " +  Style.BRIGHT + inet4cidr + Style.RESET_ALL)

			except:
				pass


			try:
				if interface == "lo":
					pass

				else:	
					broadcast = subprocess.Popen(['/bin/ip','address','show', interface], stdout=subprocess.PIPE).communicate()[0]	
					broadcast = broadcast.decode('utf-8')
					brdcastaddr = re.findall(broadcastregex, broadcast)
					brdcastaddr = ''.join(brdcastaddr)
					brdcastaddr = brdcastaddr.replace("brd ", "")
					print("    Broadcast Address: " +  Style.BRIGHT + brdcastaddr + Style.RESET_ALL)

			except:
				pass

			#IPV6
			try:
				if interface == "lo":
					pass

				else:	
					if6configs = subprocess.Popen(['/bin/ip','address','show', interface], stdout=subprocess.PIPE).communicate()[0]
					if6configs = if6configs.decode('utf-8')
					if6configsedit = if6configs.replace("/", " ")
					ip6addrs = re.search(ip6regex, if6configsedit)
					print("    IPV6 Address: " +  Style.BRIGHT + ip6addrs.group() + Style.RESET_ALL)

			except:
				pass

			#IPV6 CIDR and Subnet Masks

			try:
				if interface == "lo":
					pass

				else:
					cidrs6 = subprocess.Popen(['/bin/ip','address','show', interface], stdout=subprocess.PIPE).communicate()[0]
					cidrs6 = cidrs6.decode('utf-8')
					cidr6edit = re.sub(inet4regex,"",cidrs6, flags=re.MULTILINE)
					inet6cidr = re.findall(cidrregex, cidr6edit)
					inet6cidr = ''.join(inet6cidr)
					print("    IPV6 CIDR: " + Style.BRIGHT + inet6cidr + Style.RESET_ALL)
		
			except:
				pass

		else:
			print(Fore.RED + "Interface: " + interface + " is down" + Style.RESET_ALL)
			
		#MAC Addresses
		try:
			if interface == "lo":
				pass


			else:
				macaddr = subprocess.Popen(['/bin/ip','link','show', interface], stdout=subprocess.PIPE).communicate()[0]
				macaddr = macaddr.decode('utf-8')
				macs = re.findall(macregex, macaddr)
				macs = ''.join(macs)
				macs = macs.replace("link/ether ", "")
				print("    MAC Address: " + Style.BRIGHT + macs + Style.RESET_ALL)
				print()

		except:
			print("Could not find a MAC address for: " + interface)
			pass




def NetworkStats():

	statstitle=("""
   _____  _          _    _       _    _            
  / ____|| |        | |  (_)     | |  (_)           
 | (___  | |_  __ _ | |_  _  ___ | |_  _   ___  ___ 
  \___ \ | __|/ _` || __|| |/ __|| __|| | / __|/ __| 
  ____) || |_| (_| || |_ | |\__ \| |_ | || (__ \__ \ 
 |_____/  \__|\__,_| \__||_||___/ \__||_| \___||___/ 
                                                    
		""")


	maindir = "/sys/class/net/"

	print(Style.BRIGHT + Fore.BLUE + statstitle + Style.RESET_ALL)
	print()

	#Rx, Tx, and other network stats in the /sys/class directory
	for interface in ni.interfaces():
		print()
		print("============================================")
		print(Fore.GREEN + interface + Style.RESET_ALL)
		print()

		try:
			collisions = maindir + interface + "/statistics/collisions" 
			collisionscmd = subprocess.getoutput("cat " + collisions)
			print("Collisions: " + collisionscmd) 

		except:
			pass

		try:	
			multicast = maindir + interface + "/statistics/multicast" 
			multicastcmd = subprocess.getoutput("cat " + multicast)
			print("Multicast: " + multicastcmd) 

		except:
			pass

		print()
		print(Fore.CYAN + "Recieved Packets (RX)" + Style.RESET_ALL)

		try:
			rx_bytes = maindir + interface + "/statistics/rx_bytes" 
			rx_bytescmd = subprocess.getoutput("cat " + rx_bytes)
			print("rx_bytes: " + rx_bytescmd) 

		except:
			pass

		try:
			rx_compressed = maindir + interface + "/statistics/rx_compressed" 
			rx_compressedcmd = subprocess.getoutput("cat " + rx_compressed)
			print("rx_compressed: " + rx_compressedcmd) 
		except:
			pass

		try:
			rx_crc_errors = maindir + interface + "/statistics/rx_crc_errors" 
			rx_crc_errorscmd = subprocess.getoutput("cat " + rx_crc_errors)
			print("rx_crc_errors: " + rx_crc_errorscmd) 

		except:
			pass

		try:
			rx_dropped = maindir + interface + "/statistics/rx_dropped" 
			rx_droppedcmd = subprocess.getoutput("cat " + rx_dropped)
			print("rx_dropped: " + rx_droppedcmd) 
		
		except:
			pass
		
		try:
			rx_errors = maindir + interface + "/statistics/rx_errors" 
			rx_errorscmd = subprocess.getoutput("cat " + rx_errors)
			print("rx_errors: " + rx_errorscmd) 
		
		except:
			pass
		
		try:
			rx_fifo_errors = maindir + interface + "/statistics/rx_fifo_errors" 
			rx_fifo_errorscmd = subprocess.getoutput("cat " + rx_fifo_errors)
			print("rx_fifo_errors: " + rx_fifo_errorscmd) 

		except:
			pass

		try:
			rx_frame_errors = maindir + interface + "/statistics/rx_frame_errors" 
			rx_frame_errorscmd = subprocess.getoutput("cat " + rx_frame_errors)
			print("rx_frame_errors: " + rx_frame_errorscmd) 
		
		except:
			pass
		
		try:
			rx_length_errors = maindir + interface + "/statistics/rx_length_errors" 
			rx_length_errorscmd = subprocess.getoutput("cat " + rx_length_errors)
			print("rx_length_errors: " + rx_length_errorscmd) 

		except:
			pass

		try:
			rx_missed_errors = maindir + interface + "/statistics/rx_missed_errors" 
			rx_missed_errorscmd = subprocess.getoutput("cat " + rx_missed_errors)
			print("rx_missed_errors: " + rx_missed_errorscmd) 

		except:
			pass

		try:
			rx_nohandler = maindir + interface + "/statistics/rx_nohandler" 
			rx_nohandlercmd = subprocess.getoutput("cat " + rx_nohandler)
			print("rx_nohandler: " + rx_nohandlercmd) 

		except:
			pass

		try:
			rx_over_errors = maindir + interface + "/statistics/rx_over_errors" 
			rx_over_errorscmd = subprocess.getoutput("cat " + rx_over_errors)
			print("rx_over_errors: " + rx_over_errorscmd) 

		except:
			pass

		try:
			rx_packets = maindir + interface + "/statistics/rx_packets" 
			rx_packetscmd = subprocess.getoutput("cat " + rx_packets)
			print("rx_packets: " + rx_packetscmd) 
		
		except:
			pass

		print()
		print(Fore.MAGENTA + "Transmitted Packets (TX)" + Style.RESET_ALL)

		try:
			tx_aborted_errors = maindir + interface + "/statistics/tx_aborted_errors" 
			tx_aborted_errorscmd = subprocess.getoutput("cat " + tx_aborted_errors)
			print("tx_aborted_errors: " + tx_aborted_errorscmd) 

		except:
			pass

		try:
			tx_bytes = maindir + interface + "/statistics/tx_bytes" 
			tx_bytescmd = subprocess.getoutput("cat " + tx_bytes)
			print("tx_bytes: " + tx_bytescmd) 

		except:
			pass

		try:
			tx_carrier_errors = maindir + interface + "/statistics/tx_carrier_errors" 
			tx_carrier_errorscmd = subprocess.getoutput("cat " + tx_carrier_errors)
			print("tx_carrier_errors: " + tx_carrier_errorscmd) 

		except:
			pass

		try:
			tx_compressed = maindir + interface + "/statistics/tx_compressed" 
			tx_compressedcmd = subprocess.getoutput("cat " + tx_compressed)
			print("tx_compressed: " + tx_compressedcmd) 

		except:
			pass

		try:
			tx_dropped = maindir + interface + "/statistics/tx_dropped" 
			tx_droppedcmd = subprocess.getoutput("cat " + tx_dropped)
			print("tx_dropped: " + tx_droppedcmd) 

		except:
			pass

		try:
			tx_errors = maindir + interface + "/statistics/tx_errors" 
			tx_errorscmd = subprocess.getoutput("cat " + tx_errors)
			print("tx_errors: " + tx_errorscmd) 

		except:
			pass

		try:
			tx_fifo_errors = maindir + interface + "/statistics/tx_fifo_errors" 
			tx_fifo_errorscmd = subprocess.getoutput("cat " + tx_fifo_errors)
			print("tx_fifo_errors: " + tx_fifo_errorscmd) 

		except:
			pass

		try:
			tx_heartbeat_errors = maindir + interface + "/statistics/tx_heartbeat_errors" 
			tx_heartbeat_errorscmd = subprocess.getoutput("cat " + tx_heartbeat_errors)
			print("tx_heartbeat_errors: " + tx_heartbeat_errorscmd) 

		except:
			pass

		try:
			tx_packets = maindir + interface + "/statistics/tx_packets" 
			tx_packetscmd = subprocess.getoutput("cat " + tx_packets)
			print("tx_packets: " + tx_packetscmd) 

		except:
			pass

		try:
			tx_window_errors = maindir + interface + "/statistics/tx_window_errors" 
			tx_window_errorscmd = subprocess.getoutput("cat " + tx_window_errors)
			print("tx_window_errors: " + tx_window_errorscmd) 

		except:
			pass

	print("")		



def SubnetChart():

	title=("""

   _____         _                   _      _____  _                   _   
  / ____|       | |                 | |    / ____|| |                 | |  
 | (___   _   _ | |__   _ __    ___ | |_  | |     | |__    __ _  _ __ | |_ 
  \___ \ | | | || '_ \ | '_ \  / _ \| __| | |     | '_ \  / _` || '__|| __|
  ____) || |_| || |_) || | | ||  __/| |_  | |____ | | | || (_| || |   | |_ 
 |_____/  \__,_||_.__/ |_| |_| \___| \__|  \_____||_| |_| \__,_||_|    \__|
                                                                                                                                                      

		""")


	chart = ("""
	/8	    255.0.0.0
	/9	    255.128.0.0
	/10	    255.192.0.0
	/11	    255.224.0.0
	/12	    255.240.0.0
	/13	    255.248.0.0
	/14	    255.252.0.0
	/15	    255.254.0.0
	/16	    255.255.0.0
	/17	    255.255.128.0
	/18	    255.255.192.0
	/19	    255.255.224.0
	/20	    255.255.240.0
	/21	    255.255.248.0
	/22	    255.255.252.0
	/23	    255.255.254.0
	/24	    255.255.255.0
	/25	    255.255.255.128
	/26	    255.255.255.192
	/27	    255.255.255.224
	/28	    255.255.255.240
	/29	    255.255.255.248
	/30	    255.255.255.252
	/31 	    255.255.255.254

	""")

	print(Style.BRIGHT + Fore.YELLOW + title + Style.RESET_ALL)
	print(chart)

def RoutingTable():

	routingtabletitle=("""

  _____                _    _                 _______      _      _        
 |  __ \              | |  (_)               |__   __|    | |    | |      
 | |__) | ___   _   _ | |_  _  _ __    __ _     | |  __ _ | |__  | |  ___   
 |  _  / / _ \ | | | || __|| || '_ \  / _` |    | | / _` || '_ \ | | / _ \   
 | | \ \| (_) || |_| || |_ | || | | || (_| |    | || (_| || |_) || ||  __/   
 |_|  \_ \\___/  \__,_| \__||_||_| |_| \__, |    |_| \__,_||_.__/ |_| \___|  
                                       __/ |                               
                                      |___/                                
		""")

	#Routing
	print(Style.BRIGHT + Fore.MAGENTA + routingtabletitle + Style.RESET_ALL)
	print()
	command = "netstat -rn"
	routingtable = subprocess.getoutput(command)
	print(routingtable)
	print("")		
	

def SysInfo():

	sysinfotitle =(""" 
 
   _____              _                     _____          __       
  / ____|            | |                   |_   _|        / _|       
 | (___   _   _  ___ | |_  ___  _ __ ___     | |   _ __  | |_  ___   
  \___ \ | | | |/ __|| __|/ _ \| '_ ` _ \    | |  | '_ \ |  _|/ _ \  
  ____) || |_| |\__ \| |_|  __/| | | | | |  _| |_ | | | || | | (_) | 
 |_____/  \__, ||___/ \__|\___||_| |_| |_| |_____||_| |_||_|  \___/  
           __/ |                                                    
          |___/                                                     

          """)


	print(Style.BRIGHT + Fore.RED + sysinfotitle + Style.RESET_ALL)
	hostinfo= subprocess.getoutput("screenfetch")
	print(hostinfo) 
	print()


def Report():
	command = "python3 ChrisToolbox.py -e > Report.txt"
	report= subprocess.getoutput(command)






if __name__ == '__main__':
	main()