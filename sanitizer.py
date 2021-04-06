# -f -> Filter by bogons
# -F -> Filter by full bogons
# -L:path -> User give a list in path

import os
import pytricia

#Get the IP from de line of MRT data
def getIP(data):
    return data[2:data.find("|", 2)]

def getRoute(data):
    i = data.find("|", 2) + 1
    return data[i : data.find("|", i)]

def isIPv4(ip):
    if(ip.find(":") == -1):
        return True
    else:
        return False

def VerifyLoopings(list_route):
    for route in list(list_route):
        if(list_route.count(route) > 1):
            return True
    return False

parameters = sys.argv[1:]

user_list_path = ""

for argument in list(parameters):
    if(argument == "-f"):
        filter_full_bogons = False
    elif(argument == "-F"):
        filter_full_bogons = True
    elif(argument[:2] == "-L" and argument[2] == ":" and len(argument) > 3):
        user_list_path = argument[3:]


if(user_list_path == ""):
    file_bogons_ipv4 = open("fullbogons-ipv4.txt","r")
    bogons_ipv4 = file_bogons_ipv4.read().split("\n")[1:-1]
    print("DONE READING BOGONS IPv4")

    file_bogons_ipv6 = open("fullbogons-ipv6.txt","r")
    bogons_ipv6 = file_bogons_ipv6.read().split("\n")[1:-1]
    print("DONE READING BOGONS IPv6")

    pyt_ipv4 = pytricia.PyTricia()
    for bogon_ipv4 in list(bogons_ipv4):
        pyt_ipv4.insert(bogon_ipv4, "")
    print("DONE CREATING PYTRICIA IPv4")

    pyt_ipv6 = pytricia.PyTricia()
    for bogon_ipv6 in list(bogons_ipv6):
        pyt_ipv6.insert(bogon_ipv6, "")
    print("DONE CREATING PYTRICIA IPv6")
else:
    file_bogons = open(user_list_path,"r")
    bogons = file_bogons.read().split("\n")

#Open MRT data and read it into a list
mrt_data = os.popen("bgpscanner -L rib.20210301.0000.bz2").readlines()
print("DONE READING DATA")

sanitized_data = []
invalid_ip_count = 0
invalid_ipv4_count = 0
invalid_ipv6_count = 0
invalid_route_count = 0
ipv4_data_count = 0
ipv6_data_count = 0

#For each line from the MRT data...
for line_data in list(mrt_data):
    #...get de IP
    ip = getIP(line_data)

    #Verify if the IP is invalid
    if(isIPv4(ip)):
        ipv4_data_count += 1
        if(ip == "0.0.0.0/8"):
            invalid_ip_count += 1
            invalid_ipv4_count += 1
        else:        
            try:
                pyt_ipv4[ip]
                invalid_ip_count += 1
                invalid_ipv4_count += 1
                #Invalid IP
            except KeyError:
                #Valid IP
                #...get the route
                route = getRoute(line_data).split(" ")

                #Verfify loopings
                if(VerifyLoopings(route)):
                    #Has loopings, invalid route
                    invalid_route_count += 1
                else:
                    #Verify invalid routes

                    sanitized_data.append(line_data)
    else:
        ipv6_data_count += 1
        if(ip == "::/8"):
            invalid_ip_count += 1
            invalid_ipv6_count += 1
        else:        
            try:
                pyt_ipv6[ip]
                invalid_ip_count += 1
                invalid_ipv6_count += 1
                #Invalid IP
            except KeyError:
                #Valid IP
                #...get the route
                route = getRoute(line_data).split(" ")

                #Verfify loopings
                if(VerifyLoopings(route)):
                    #Has loopings, invalid route
                    invalid_route_count += 1
                else:
                    #Verify invalid routes

                    sanitized_data.append(line_data)


#Criar arquivo final
        

print("DONE SANITIZATION")
print("ORIGINAL DATA: " + str(len(mrt_data)))
print("IPv4 DATA: " + str(ipv4_data_count))
print("IPv6 DATA: " + str(ipv6_data_count))
print("SANITIZED DATA: " + str(len(sanitized_data)))
print("INVALID IP COUNT: " + str(invalid_ip_count))
print("INVALID IPv4 COUNT: " + str(invalid_ipv4_count))
print("INVALID IPv6 COUNT: " + str(invalid_ipv6_count))
print("INVALID ROUTE COUNT: " + str(invalid_route_count))




