import csv
from ciscoconfparse import CiscoConfParse
import os
import sqlite3


#conn = sqlite3.connect(out.db)
#c = conn.cursor()

path = "/home/jp/Documents/Migration_tools/SUNSPEED/CONFIGS/"
dirs = os.listdir( path )

print ("\n .... using Server Audit template \n ..... reading port infomation and findling VLAN tags from config files \n")


#read information from populated audit csv file # 
f = open ('sunspeed_pre_move.csv', 'r')
csv_f = csv.reader(f)
next(csv_f, None)

#output/scratch file with all output data #
sfile = open('new_config_output.txt', 'wa')
 
for row in csv_f:
	servername = row[2]
	serverinterface = row[4]
	configfilename = row[35]
	slotinformation = row[36]
	interfaceinformation = row[37]
	ethinfo = str("interface GigabitEthernet"+slotinformation+"/"+interfaceinformation)
	parse= CiscoConfParse("/home/jp/Documents/Migration_tools/SUNSPEED/CONFIGS/"+configfilename+".inf.uk.cliffordchance.com-Running.config")
	portconfig = parse.find_all_children(ethinfo)
	print (servername+"-"+serverinterface)
	sfile.write("new name is "+servername+"-"+serverinterface +", ") 
# portconfig is a list of all port information found in the config file matched to the interface #
	for line in portconfig:
		if "description" in line:
			desc = line
			print desc
			sfile.write("old name is "+desc+", ")
		if "switchport access" in line:
			vlanid = str(line)
			print str(vlanid)
			sfile.write(vlanid +", ")
		if "speed" in line:
			speed = line
			print speed
			sfile.write(speed +", ")
		if "channel-group" in line:
			channel = line
			print channel
			sfile.write(channel +",")
		if "shutdown" in line:
			shutdown = line
			print "PORT SHUTDOWN"
			sfile.write(" PORT SHUT")
	else:
		sfile.write("\n")
		continue
else:
	print "\n all done - above is the interesting configuration which has been aved to new_config_output.txt "	
	sfile.close()

print "\n Now opening new_config_output.txt file and converting to csv file"

txt_file = r"new_config_output.txt"
csv_file = r"new_config_output.csv"

in_txt = csv.reader(open(txt_file, "rb"), delimiter = ",")
out_csv = csv.writer(open(csv_file, "wb"))

out_csv.writerows(in_txt)

print "\n new file new_config_output.csv has been created with all interesting information"
