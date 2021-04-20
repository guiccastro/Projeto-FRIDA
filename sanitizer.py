# -f -> Filter by bogons
# -F -> Filter by full bogons
# -L:path -> User give a list in path

import os
import pytricia
import sys
import wget
import gzip
import csv
from os import path
from datetime import datetime
import threading

# Get the IP from de line of MRT data
def getIP(data):
    return data[2:data.find("|", 2)]

# Get the route from de line of MRT data
def getRoute(data):
    i = data.find("|", 2) + 1
    return data[i : data.find("|", i)]

# Verifys if the ip is a IPv4
def isIPv4(ip):
    if(ip.find(":") == -1):
        return True
    else:
        return False

# Verify if the list has routes with loopings
def VerifyLoopings(list_route):
    for route in list(list_route):
        if(list_route.count(route) > 1):
            return True
    return False

# Divides the given original_list in n parts and return a list with n list 
def DivideList(original_list,n):
    new_list = []
    
    if((len(original_list) % n) != 0):
        divide = int(len(original_list)/n)
        for i in range(0,n-1):
            new_list.append(original_list[divide*i:divide*i + divide])
        new_list.append(original_list[divide*(n-2) + divide:])
    else:
        divide = int(len(original_list)/n)
        for i in range(0,n):
            new_list.append(original_list[divide*i:divide*i + divide])

    return new_list

# Do the sanitization without a user's list of bogons
def SanitizationWithoutUserList():
    # Get each file of MRT data
    while(len(list_mrt_data) > 0):

        file_mrt = list_mrt_data.pop()

        # Get the date info from the file name and separates into a list [year,month,day]
        date = file_mrt.split(".")[-3]
        date = [date[:4],date[4:6],date[6:]]

        # Initialize the varibales for the file names of the bogons
        bogon_ipv4_file_name = ""
        bogon_ipv6_file_name = ""

        # Variable to check if there is a error in the download 
        error = False

        # Filter by fullbogons
        if(filter_by_fullbogons):
            
            # Download IPv4 fullbogons
            # Url pattern = prefix url + "year-month-day.fullbogons-ipv4.txt.gz"
            url = url_fullbogons_ipv4 + date[0] + "-" + date[1] + "-" + date[2] + ".fullbogons-ipv4.txt.gz"
            try:
                print("\nDownloading the IPv4 fullbogons from '" + url.split("/")[-1] + "'.")
                bogon_ipv4_file_name = wget.download(url, out='Bogons/')
                
            except: # If occurs an error...
                error = True
                # Create a log of an error
                error_log = "Failed to download the IPv4 fullbogons from '" + url.split("/")[-1] + "'."
                print(error_log)
                # Add the log to the list
                error_log_download_fullbogons.append(error_log + "\n")

            # Download IPv6 fullbogons
            url = url_fullbogons_ipv6 + date[0] + "-" + date[1] + "-" + date[2] + ".fullbogons-ipv6.txt.gz"
            try:
                print("\nDownloading the IPv6 fullbogons from '" + url.split("/")[-1] + "'.")
                bogon_ipv6_file_name = wget.download(url, out='Bogons/')
            except: # If occurs an error...
                error = True
                # Create a log of an error
                error_log = "Failed to download the IPv6 fullbogons from '" + url.split("/")[-1] + "'." 
                print(error_log)
                # Add the log to the list
                error_log_download_fullbogons.append(error_log + "\n")
        else:
            # Download IPv4 bogons
            # Url pattern = prefix url + "year-month-day.bogon-bn-agg.txt.gz"
            url = url_bogons_ipv4 + date[0] + "-" + date[1] + "-" + date[2] + ".bogon-bn-agg.txt.gz"
            try:
                print("\nDownloading the IPv4 bogons from '" + url.split("/")[-1] + "'.")
                bogon_ipv4_file_name = wget.download(url, out='Bogons/')
            except:
                error = True
                error_log = "Failed to download the IPv4 bogons from '" + url.split("/")[-1] + "'."
                print(error_log)
                error_log_download_bogons.append(error_log + "\n")

            # Download IPv6 bogons (there is no bogon list for IPv6, that is why we download the fullbogons list anyway)
            url = url_fullbogons_ipv6 + date[0] + "-" + date[1] + "-" + date[2] + ".fullbogons-ipv6.txt.gz"
            try:
                print("\nDownloading the IPv6 fullbogons from '" + url.split("/")[-1] + "'.")
                bogon_ipv6_file_name = wget.download(url, out='Bogons/')
            except: # If occurs an error...
                error = True
                # Create a log of an error
                error_log = "Failed to download the IPv6 fullbogons from '" + url.split("/")[-1] + "'." 
                print(error_log)
                # Add the log to the list
                error_log_download_fullbogons.append(error_log + "\n")

        # Variables for the filter information
        invalid_ip_count = 0
        invalid_ipv4_count = 0
        invalid_ipv6_count = 0
        invalid_route_count = 0
        ipv4_data_count = 0
        ipv6_data_count = 0

        # Verifys if there is no error in the download
        if(not error):
            print("Reading bogons for file '" + file_mrt + "'.")

            # Get the name of the bogon file related to the MRT data file
            bogon_ipv4_file_name = bogon_ipv4_file_name.split("/")[-1]
            bogon_ipv6_file_name = bogon_ipv6_file_name.split("/")[-1]

            # Open the file and read its information
            file_bogons_ipv4 = gzip.open("Bogons/" + bogon_ipv4_file_name,"r")
            bogons_ipv4 = file_bogons_ipv4.read().decode("utf-8").split("\n")[1:-1]
            file_bogons_ipv4.close()

            # Open the file and read its information
            file_bogons_ipv6 = gzip.open("Bogons/" + bogon_ipv6_file_name,"r")
            bogons_ipv6 = file_bogons_ipv6.read().decode("utf-8").split("\n")[1:-1]
            file_bogons_ipv6.close()

            # Create the Pytricia
            pyt_ipv4 = pytricia.PyTricia()
            for bogon_ipv4 in list(bogons_ipv4):
                pyt_ipv4.insert(bogon_ipv4, "")
            print("DONE CREATING PYTRICIA IPv4")
            del bogons_ipv4

            # Create the Pytricia
            pyt_ipv6 = pytricia.PyTricia()
            for bogon_ipv6 in list(bogons_ipv6):
                pyt_ipv6.insert(bogon_ipv6, "")
            print("DONE CREATING PYTRICIA IPv6")
            del bogons_ipv6

            #Open MRT data and read it into a list (already without the prefixes with loopings, using the parameter '-L')
            mrt_data = os.popen("bgpscanner -L Data/" + file_mrt).readlines()
            print("Done reading MRT data")

            # Initialize the variable to save the sanitized data
            sanitized_data = []

            #For each line from the MRT data...
            for line_data in list(mrt_data):
                #...get de IP
                ip = getIP(line_data)

                #Verify if is an IPv4
                if(isIPv4(ip)):

                    # Update the filter information
                    ipv4_data_count += 1       

                    # Try to access the IP in the Pytricia, if it can access, than the IP is invalid 
                    try:
                        pyt_ipv4[ip]

                        # Update the filter information
                        invalid_ip_count += 1
                        invalid_ipv4_count += 1

                    except KeyError: 
                        
                        # Verify if the IP has parents that are invalid, if has, than the IP is invalid too
                        try: 
                            pyt_ipv4.parent(ip)

                            # Update the filter information
                            invalid_ip_count += 1
                            invalid_ipv4_count += 1

                        except KeyError: # If an error occurs, than the IP is valid

                            #...get the route
                            #route = getRoute(line_data).split(" ")

                            #Verfify loopings
                            #if(VerifyLoopings(route)):
                                #Has loopings, invalid route
                            #    invalid_route_count += 1
                            #else:
                                #Verify invalid routes

                            # The line of the MRT data is fully correct, than it can be added to the list of sanitized data
                            # The .encode() function is to the data to be write correctly in the final file
                            sanitized_data.append(line_data.encode())
                
                # Is an IPv6        
                else:
                    # Update the filter information
                    ipv6_data_count += 1  

                    # Try to access the IP in the Pytricia, if it can access, than the IP is invalid      
                    try:
                        pyt_ipv6[ip]

                        # Update the filter information
                        invalid_ip_count += 1
                        invalid_ipv6_count += 1

                    except KeyError: 

                        # Verify if the IP has parents that are invalid, if has, than the IP is invalid too
                        try:
                            pyt_ipv6.parent(ip)

                            # Update the filter information
                            invalid_ip_count += 1
                            invalid_ipv6_count += 1

                        except KeyError: # If an error occurs, than the IP is valid

                            #...get the route
                            #route = getRoute(line_data).split(" ")

                            #Verfify loopings
                            #if(VerifyLoopings(route)):
                                #Has loopings, invalid route
                            #    invalid_route_count += 1
                            #else:
                                #Verify invalid routes

                            # The line of the MRT data is fully correct, than it can be added to the list of sanitized data
                            # The .encode() function is to the data to be write correctly in the final file
                            sanitized_data.append(line_data.encode())

            # As the MRT data can be a large file, clear the memory to open space
            del mrt_data 

        # There was an error in the download of bogons. As there is no invalid IP's to verify, the sanitization only occurs with the looping routes
        else: 
            sanitized_data = os.popen("bgpscanner -L Data/" + file_mrt).readlines()
            # The .encode() function is to the data to be write correctly in the final file
            sanitized_data = sanitized_data.encode()
            print("Done reading MRT data")

        print("Sanitization from file " + file_mrt + " is complete.")

        # Create a .gz file to save the .csv file where the sanitized data will be written
        # The final file will have the same file name of the original MRT data file
        sanitized_file = gzip.open("SanitizedData/" + file_mrt[:-3] + "csv.gz","wb")
        sanitized_file.writelines(sanitized_data)
        sanitized_file.close()

        # As the MRT data sanitized can be a little large, clear the memory to open space
        del sanitized_data

        # Create the data for the sanitization info
        sanitization_info = []
        sanitization_info.append("Original IP's: " + str(ipv4_data_count + ipv6_data_count) + "\n")
        sanitization_info.append("Original IPv4's: " + str(ipv4_data_count) + "\n")
        sanitization_info.append("Original IPv6's: " + str(ipv6_data_count) + "\n")
        sanitization_info.append("Invalid IP's: " + str(invalid_ip_count) + "\n")
        sanitization_info.append("Invalid IPv4's: " + str(invalid_ipv4_count) + "\n")
        sanitization_info.append("Invalid IPv6's: " + str(invalid_ipv6_count) + "\n")
        sanitization_info.append("Invalid routes: " + str(invalid_route_count) + "\n")

        # Create a .txt file to save the sanitization info
        # The file will have the same file name of the original MRT data file with 'Sanitization_Info_' prefix
        sanitization_info_file = open ("SanitizedData/Sanitization_Info_" + file_mrt[:-3] + "txt", "w")
        sanitization_info_file.writelines(sanitization_info)
        sanitization_info_file.close()
   
# Do the sanitization with a user's list of bogons
def SanitizationWithUserList():
    # Get each file of MRT data
    while(len(list_mrt_data) > 0):

        file_mrt = list_mrt_data.pop()

        #Open MRT data and read it into a list (already without the prefixes with loopings, using the parameter '-L')
        mrt_data = os.popen("bgpscanner -L Data/" + file_mrt).readlines()
        print("Done reading MRT data")

        # Initialize the variable to save the sanitized data
        sanitized_data = []

        # Variables for the filter information
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

            #Verify if is an IPv4
            if(isIPv4(ip)):

                # Update the filter information
                ipv4_data_count += 1 

                # Try to access the IP in the Pytricia, if it can access, than the IP is invalid    
                try:
                    pyt_ipv4[ip]

                    # Update the filter information
                    invalid_ip_count += 1
                    invalid_ipv4_count += 1

                except KeyError: 

                    # Verify if the IP has parents that are invalid, if has, than the IP is invalid too
                    try:
                        pyt_ipv4.parent(ip)

                        # Update the filter information
                        invalid_ip_count += 1
                        invalid_ipv4_count += 1

                    except KeyError: # If an error occurs, than the IP is valid

                        #...get the route
                        #route = getRoute(line_data).split(" ")

                        #Verfify loopings
                        #if(VerifyLoopings(route)):
                            #Has loopings, invalid route
                        #    invalid_route_count += 1
                        #else:
                            #Verify invalid routes

                        # The line of the MRT data is fully correct, than it can be added to the list of sanitized data
                        # The .encode() function is to the data to be write correctly in the final file
                        sanitized_data.append(line_data.encode())

            # Is an IPv6               
            else:

                # Update the filter information
                ipv6_data_count += 1

                # Try to access the IP in the Pytricia, if it can access, than the IP is invalid
                try:
                    pyt_ipv6[ip]

                    # Update the filter information
                    invalid_ip_count += 1
                    invalid_ipv6_count += 1
                
                except KeyError: 
                    
                    # Verify if the IP has parents that are invalid, if has, than the IP is invalid too
                    try:
                        pyt_ipv6.parent(ip)

                        # Update the filter information
                        invalid_ip_count += 1
                        invalid_ipv6_count += 1

                    except KeyError: # If an error occurs, than the IP is valid

                        #...get the route
                        #route = getRoute(line_data).split(" ")

                        #Verfify loopings
                        #if(VerifyLoopings(route)):
                            #Has loopings, invalid route
                        #    invalid_route_count += 1
                        #else:
                            #Verify invalid routes

                        # The line of the MRT data is fully correct, than it can be added to the list of sanitized data
                        # The .encode() function is to the data to be write correctly in the final file
                        sanitized_data.append(line_data.encode())

        # As the MRT data can be a large file, clear the memory to open space
        del mrt_data 

        print("Sanitization from file " + file_mrt + " is complete.")

        # Create a .gz file to save the .csv file where the sanitized data will be written
        # The final file will have the same file name of the original MRT data file
        sanitized_file = gzip.open("SanitizedData/" + file_mrt[:-3] + "csv.gz","wb")
        sanitized_file.writelines(sanitized_data)
        sanitized_file.close()

        # As the MRT data sanitized can be a little large, clear the memory to open space
        del sanitized_data

        # Create the data for the sanitization info
        sanitization_info = []
        sanitization_info.append("Original IP's: " + str(ipv4_data_count + ipv6_data_count) + "\n")
        sanitization_info.append("Original IPv4's: " + str(ipv4_data_count) + "\n")
        sanitization_info.append("Original IPv6's: " + str(ipv6_data_count) + "\n")
        sanitization_info.append("Invalid IP's: " + str(invalid_ip_count) + "\n")
        sanitization_info.append("Invalid IPv4's: " + str(invalid_ipv4_count) + "\n")
        sanitization_info.append("Invalid IPv6's: " + str(invalid_ipv6_count) + "\n")
        sanitization_info.append("Invalid routes: " + str(invalid_route_count) + "\n")

        # Create a .txt file to save the sanitization info
        # The file will have the same file name of the original MRT data file with 'Sanitization_Info_' prefix
        sanitization_info_file = open ("SanitizedData/Sanitization_Info_" + file_mrt[:-3] + "txt", "w")
        sanitization_info_file.writelines(sanitization_info)
        sanitization_info_file.close()


###### PARAMETER VARIABLES ######

filter_by_bogons = False
filter_by_fullbogons = False

user_list_path = ""

###### READING THE PARAMETERS ######

# Read parameters from terminal
parameters = sys.argv[1:]

# Variable to check if there is a error in the parameters
error = False

for parameter in list(parameters):

    # Every parameter must start with '-'
    if(parameter[0] != "-"):
        print("ERROR: Character '-' is missing.")
    else:
        # Get the letter from the parameter 
        argument_type = parameter[1]

        # Filter by bogons
        if(argument_type == "f"):
            filter_by_bogons = True

        # Filter by fullbogons
        elif(argument_type == "F"):
            filter_by_fullbogons = True

        # Filter by a list given by the user
        elif(argument_type == "L"):

            # Verifys if the parameter is write correctly
            if(len(parameter) > 3 and parameter[2] == ":"):
                user_list_path = parameter[3:]
            else:
                print("ERROR: Parameter '-L' is wrong.")
                error = True
        else:
            print("ERROR: Parameter '" + argument_type + "' is invalid.")
            error = True

###### FILTER DATA ######

# Number of threads to be created
parallel_sanitization = 2

# Verifys if there is no error in the paramenters
if(not(error)):

    # Get a list of the files inside the "Data" directorie
    list_mrt_data = os.listdir("Data")

    # Verifys if the directorie SanitizedData exists
    if(not path.exists("SanitizedData/")):
        # If not, create one
        os.mkdir("SanitizedData")

    # Verifys if a list given by the user mus be used
    if(user_list_path == ""):

        # The list was not given, then the bogons must be downloaded from the internet
        print("Reading bogons from internet...")

        # URL prefixes for the IPv4 and IPv6 fullbogons
        url_fullbogons_ipv4 = "https://publicdata.caida.org/datasets/bogon/fullbogons-ipv4/"
        url_fullbogons_ipv6 = "https://publicdata.caida.org/datasets/bogon/fullbogons-ipv6/"
        
        # URL prefixes for the IPv4 and IPv6 bogons
        url_bogons_ipv4 = "https://publicdata.caida.org/datasets/bogon/bogon-bn-agg/"
        #url_bogons_ipv6 = ""

        # Initializes the list for the logs of the bogons and fullbogons
        error_log_download_fullbogons = []
        error_log_download_bogons = []

        # Create a list for the threads
        threads = []

        # Create n number of threads (n = parallel_sanitization)
        for thread_index in range(0,parallel_sanitization):
            # Create the thread initializing the SanitizationWithoutUserList function
            threads.append(threading.Thread(target=SanitizationWithoutUserList, args=()))
            # Start the thread
            threads[thread_index].start()
    
    # A list was given by the user
    else:
        print("Reading bogons from user...")

        # Read the file given by the user
        file_bogons = open(user_list_path,"r")
        bogons = file_bogons.read().split("\n")[:-1]
        file_bogons.close()
        print("Done reading bogons from '" + user_list_path + "'")

        # Initialize a list for the IPv4 and IPv6 bogons, to separate this IP's from the list given by the user
        bogons_ipv4 = []
        bogons_ipv6 = []

        # For each bogon in the list of bogons
        for bogon in list(bogons):

            # Verfifys if is an IPv4...
            if(isIPv4(bogon)):
                bogons_ipv4.append(bogon)
            else: # ... or and IPv6
                bogons_ipv6.append(bogon)
        
        # Create the Pytricia
        pyt_ipv4 = pytricia.PyTricia()
        for bogon_ipv4 in list(bogons_ipv4):
            pyt_ipv4.insert(bogon_ipv4, "a")
        print("DONE CREATING PYTRICIA IPv4")
        del bogons_ipv4

        # Create the Pytricia
        pyt_ipv6 = pytricia.PyTricia()
        for bogon_ipv6 in list(bogons_ipv6):
            pyt_ipv6.insert(bogon_ipv6, "")
        print("DONE CREATING PYTRICIA IPv6")
        del bogons_ipv6

        # Create a list for the threads
        threads = []

        # Create n number of threads (n = parallel_sanitization)
        for thread_index in range(0,parallel_sanitization):
            # Create the thread initializing the SanitizationWithUserList function
            threads.append(threading.Thread(target=SanitizationWithUserList, args=()))
            # Start the thread
            threads[thread_index].start()


    ###### CREATING THE LOG ERROR FILES ######

    # Wait for all the threads to finish
    for thread_index in range(0,parallel_sanitization):
        threads[thread_index].join()

    # Verifys if a directory for the logs exists
    if(not path.exists("ErrorLogs/")):
        # If not, create one
        os.mkdir("ErrorLogs")

    # Verifys if a directory for the logs exists
    if(not path.exists("ErrorLogs/Sanitizer/")):
        # If not, create one
        os.mkdir("ErrorLogs/Sanitizer")

    # Gets the current date and time
    now = datetime.now()

    # Verifys if there is logs for fullbogons
    if(len(error_log_download_fullbogons) > 0):
        # Create the file inside de correct directory, with the current date and time in the file name
        error_log_file = open ("ErrorLogs/Sanitizer/ErrorLog_Fullbogons_" + now.strftime("%Y-%m-%d_%H:%M:%S") + ".txt", "w")
        # Write the logs in the file
        error_log_file.writelines(error_log_download_fullbogons)
        # Close the file
        error_log_file.close()

    # Verifys if there is logs for bogons
    if(len(error_log_download_bogons) > 0):
        # Create the file inside de correct directory, with the current date and time in the file name
        error_log_file = open ("ErrorLogs/Sanitizer/ErrorLog_Bogons_" + now.strftime("%Y-%m-%d_%H:%M:%S") + ".txt", "w")
        # Write the logs in the file
        error_log_file.writelines(error_log_download_bogons)
        # Close the file
        error_log_file.close()