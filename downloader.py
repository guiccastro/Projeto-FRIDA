### DATA TYPE ### (You must pass one of the parameters, otherwise the code will not generate any URL)
# -t -> download only RIBs data
# -T -> download only UPDATE data

### BEGIN AND END DATE ###
# -B:year/month/day,hour:minute
# -E:year/month/day,hour:minute

### FREQUENCY ###
# -Fh:n
# -Fd:n (not implemented yet)
# -Fm:n (not implemented yet)

### PROJECT ###
# -I -> download data from Isolario
# -V -> download data from RouteViews
# -R -> download data from RIPE

### COLLECTOR ###
# -I:a,b,c
# -V:a,b,c
# -R:a,b,c
# To download from all collectors from a project you just need to pass none collector in the parameter (e.g., to download from all collectors from Isolario, pass the parameter like '-I')

### NUMBER OF PARALLEL DOWNLOADS ### (If not passed, the code will download all files linearly)
# -P:n

### PATH TO SAVE FILE ### (If not passed, the default path is "Data/". The path doesn't need to exist, because the code will create the directioe if not, but the path must be in the same directory as this code, otherwise wget will not download the file)
# -S:path

import wget
import sys
import os
import calendar
from datetime import datetime
from os import path
import threading
import ssl

# Function to assist the ListDays function. Return the given list of days without the '0' days 
def CreatListFromIterator(iterator):
    list_days = []
    for day in iterator:
        if(day != 0):
            list_days.append(day)
    
    return list_days

# Create a list of days (year, month and day) that exists between the beggining date and the end date
def ListDays(b_year,b_month,b_day,e_year,e_month,e_day):

    #obj_calendar = calendar.Calendar(6)

    date_list = []

    current_year = b_year
    current_month = b_month

    if(current_year == e_year and current_month == e_month):

        days_list = CreatListFromIterator(obj_calendar.itermonthdays(current_year, current_month))

        days_list = days_list[days_list.index(b_day):]
        days_list = days_list[:days_list.index(e_day)+1]

        for day in list(days_list):
            current_date = [current_year,current_month,day]
            date_list.append(current_date)

    else:

        #First month iteraction
        days_list = CreatListFromIterator(obj_calendar.itermonthdays(current_year, current_month))

        #days_list = list(map(int, days_list))
        days_list = days_list[days_list.index(b_day):]

        for day in list(days_list):
            current_date = [current_year,current_month,day]
            date_list.append(current_date)

        if(current_month == 12):
            current_month = 0
            current_year += 1
        else:
            current_month += 1    

        # Looping iteraction 
        while(not(current_year == e_year and current_month == e_month)):
            days_list = CreatListFromIterator(obj_calendar.itermonthdays(current_year, current_month))

            for day in list(days_list):
                current_date = [current_year,current_month,day]
                date_list.append(current_date)

            if(current_month == 12):
                current_month = 0
                current_year += 1
            else:
                current_month += 1  

        #Last month iteraction
        days_list = CreatListFromIterator(obj_calendar.itermonthdays(current_year, current_month))

        days_list = days_list[:days_list.index(e_day)+1]

        for day in list(days_list):
            current_date = [current_year,current_month,day]
            date_list.append(current_date)

    return date_list

# The number in the style 0,1,2,...,9 must be in the style 00,01,02,...,09
def AdjustNumberString(number_int):
    if(number_int < 10):
        return "0" + str(number_int)
    else:
        return str(number_int)

# Add the hour and minute to each date on the date list based on the beggining time, ending time and frequency of hour
def ListHourAndMinute(list_date,b_hour,b_minute,e_hour,e_minute,frequency_hour):
    current_hour = int(b_hour)
    current_minute = int(b_minute)

    new_date_list = []

    for date in list_date[:-1]:
        new_date = date[:]
        new_date.append(AdjustNumberString(current_hour))
        new_date.append(AdjustNumberString(current_minute))

        new_date_list.append(new_date)
        new_date = date[:]

        current_hour += frequency_hour

        while(current_hour < 24):
            new_date.append(AdjustNumberString(current_hour))
            new_date.append(AdjustNumberString(current_minute))
            new_date_list.append(new_date)
            new_date = date[:]
            current_hour += frequency_hour
        
        current_hour -= 24

    while(current_hour < e_hour):
        new_date = list_date[-1][:]
        new_date.append(AdjustNumberString(current_hour))
        new_date.append(AdjustNumberString(current_minute))

        new_date_list.append(new_date)

        current_hour += frequency_hour

    
    current_hour = e_hour

    new_date = list_date[-1][:]
    new_date.append(AdjustNumberString(current_hour))
    new_date.append(AdjustNumberString(current_minute))

    new_date_list.append(new_date)
    
    return new_date_list


#def GetDateFromFrequencyDay(list_date,frequency_day):
#    index = 0
#    new_date_list = []
#    while(index < len(list_date)):
#        new_date_list.append(list_date[index])
#        index += frequency_day
#
#    if(new_date_list[-1] != list_date[-1]):
#        new_date_list.append(list_date[-1])
#
#    return new_date_list

# Divides the given original_list in n parts and return a list with n list 
#def DivideList(original_list,n):
#    new_list = []
#    
#    if((len(original_list) % n) != 0):
#        divide = int(len(original_list)/n)
#        for i in range(0,n-1):
#            new_list.append(original_list[divide*i:divide*i + divide])
#        new_list.append(original_list[divide*(n-2) + divide:])
#    else:
#        divide = int(len(original_list)/n)
#        for i in range(0,n):
#            new_list.append(original_list[divide*i:divide*i + divide])
#
#    return new_list

# Function to download data in diferent threads
#def DownloadURLs(list_urls,project):
#
#    # For each url in the list
#    for url in list_urls:
#
#        # Try to download from the URL
#        try: 
#            print("\nDownloading the file '" + url.split("/")[-1] + "'.")
#            # Download from the URL and save in the directory 'Data'
#            wget.download(url, out='Data/')
#        except: # If occurs an error...
#
#            # Create a log for the error
#            error_log = "Failed to download the file '" + url.split("/")[-1] + "'."
#            print("\n" + error_log)
#
#            # Save the log into the list of logs of the correct project
#            if(project == "Isolario"):
#                error_log_Isolario.append(error_log + "\n")
#            elif(project == "RouteViews"):
#                error_log_RouteViews.append(error_log + "\n")
#            else:
#                error_log_RIPE.append(error_log + "\n")

def CreateFileNameFromRouteViews(url):
    url_aux = url.split("/")
    url_aux = url_aux[:-4]

    file_name = "RouteViews-"

    if("route-views" in url_aux[-1]):
        url_aux = url_aux[-1].split(".")

        if(len(url_aux) == 1):
            return "RouteViews-" + url_aux[0] + "-" + url.split("/")[-1]
        else:
            return "RouteViews-" + url_aux[1] + "-" + url.split("/")[-1]

    else:
        return "RouteViews-route-views2-" + url.split("/")[-1]


# Function to download data in diferent threads from Isolario
def DownloadFromIsolario():

    while(len(url_list_Isolario) > 0):

        url = url_list_Isolario.pop()
    
        # Try to download from the URL
        try: 
            print("\nDownloading the file '" + url.split("/")[-1] + "' from Isolario.")

            file_name = "Isolario-" + url.split("/")[-3] + "-" + url.split("/")[-1]
            file_type = url.split("/")[-1].split(".")[0].upper()

            if(file_type == "RIB"):
                file_type += "S"

            file_type += "/"

            # Download from the URL and save in the directory 'save_file_path/RIBS'
            wget.download(url, out=save_file_path + file_type + file_name)
            
        except: # If occurs an error...

            # Create a log for the error
            error_log = "Failed to download the file '" + url.split("/")[-1] + "'."
            print("\n" + error_log)

            # Save the log into the list of logs
            error_log_Isolario.append(error_log + "\n")

# Function to download data in diferent threads from RouteViews
def DownloadFromRouteViews():

    while(len(url_list_RouteViews) > 0):

        url = url_list_RouteViews.pop()
    
        # Try to download from the URL
        try: 
            print("\nDownloading the file '" + url.split("/")[-1] + "' from RouteViews.")

            file_name = CreateFileNameFromRouteViews(url)
            file_type = url.split("/")[-1].split(".")[0].upper()

            if(file_type == "RIB"):
                file_type += "S"

            file_type += "/"

            # Download from the URL and save in the directory 'save_file_path/RIBS'
            wget.download(url, out=save_file_path + file_type + file_name)

        except: # If occurs an error...

            # Create a log for the error
            error_log = "Failed to download the file '" + url.split("/")[-1] + "'."
            print("\n" + error_log)

            # Save the log into the list of logs
            error_log_RouteViews.append(error_log + "\n")


# Function to download data in diferent threads from RIPE
def DownloadFromRIPE():

    while(len(url_list_RIPE) > 0):

        url = url_list_RIPE.pop()
        print(url)
    
        # Try to download from the URL
        try: 
            print("\nDownloading the file '" + url.split("/")[-1] + "' from RIPE.")

            file_name = "RIPE-" + url.split("/")[-3] + "-" + url.split("/")[-1]
            file_type = url.split("/")[-1].split(".")[0].upper()

            if(file_type == "BVIEW"):
                file_type = "RIBS"

            file_type += "/"

            # Download from the URL and save in the directory 'save_file_path/RIBS'
            wget.download(url, out=save_file_path + file_type + file_name)
            
        except: # If occurs an error...

            # Create a log for the error
            error_log = "Failed to download the file '" + url.split("/")[-1] + "'."
            print("\n" + error_log)

            # Save the log into the list of logs
            error_log_RIPE.append(error_log + "\n")

###### PROJECT PATTERNS ######

### ISOLARIO PATTERN URL ### 
# https://isolario.it/Isolario_MRT_data/collector/year_month/(rib or updates).yearmonthday.hourminute.bz2

url_prefix_Isolario = "https://isolario.it/Isolario_MRT_data/"
collectors_Isolario = ["Alderaan","Dagobah","Korriban","Naboo","Taris"]

### RIPE PATTERN URL ###
# http://archive.routeviews.org/route-viewsnumber.collector/bgpdata/year.month/(RIBS or UPDATES)/(rib or updates).yearmonthday.hourminute.bz2
# routeviews_number = ["","2","3","4"] 
# The number "2" only works to call the 2nd São Paulo collector
# To call the route-views2 collector, the url is:
# http://archive.routeviews.org/bgpdata/year.month/(RIBS or UPDATES)/(rib or updates).yearmonthday.hourminute.bz2

url_prefix_RouteViews = "http://archive.routeviews.org/"
collectors_RouteViews = ["amsix","chicago","chile","eqix","flix","gorex","isc","kixp","jinx","linx","napafrica","nwax","phoix","telxatl","wide","sydney","saopaulo","saopaulo2","sg","perth","sfmix","soxrs","mwix","rio","fortaleza","gixa"]
# "saopaulo2" is to call the 2nd collector from São Paulo
routeviews_specials = ["route-views2","route-views3","route-views4"]

### RIPE PATTERN URL ###
# http://data.ris.ripe.net/collector/year.month/(bview or updates).yearmonthday.hourminute.gz

url_prefix_RIPE = "http://data.ris.ripe.net/"
collectors_RIPE = ["rrc00","rrc01","rrc02","rrc03","rrc04","rrc05","rrc06","rrc07","rrc08","rrc09","rrc10","rrc11","rrc12","rrc13","rrc14","rrc15","rrc16","rrc17","rrc18","rrc19","rrc20","rrc21","rrc22","rrc23","rrc24"]



###### PARAMETER VARIABLES ######

download_RIBS = False
download_UPDATES = False

begin_year = ""
begin_month = ""
begin_day = ""
begin_hour = ""
begin_minute = ""

end_year = ""
end_month = ""
end_day = ""
end_hour = ""
end_minute = ""

frequency_hour = ""
frequency_day = ""
frequency_month = ""

download_from_Isolario = False
download_from_RouteViews = False
download_from_RIPE = False

chosen_collectors_Isolario = []
chosen_collectors_RouteViews = []
chosen_collectors_RIPE = []

parallels_downloads = 1

save_file_path = ""

###### READING THE PARAMETERS ######

# Read parameters from terminal
parameters = sys.argv[1:]

# Variable to check if there is a error in the parameters
error = False

for parameter in list(parameters):
    # Every parameter must start with '-'
    if(parameter[0] != "-"):
        print("ERROR: Character '-' is missing.")
        error = True
    else:
        # Get the letter from the parameter 
        argument_type = parameter[1]

        # Download only RIBs data
        if(argument_type == "t"):
            download_RIBS = True

        # Download only UPDATE data
        elif(argument_type == "T"):
            download_UPDATES = True

        # Begin date and time
        elif(argument_type == "B"):

            # Verifys if the parameter is write correctly
            if(len(parameter) > 2 and parameter[2] == ":" and parameter[3:].count(":") == 1 and parameter[3:].count("/") == 2 and parameter[3:].count(",") == 1):

                # Get year,month and day from the parameter
                date = parameter[3:].split(",")[0].split("/")

                # Get hour and minute from the parameter
                hour_minute = parameter[3:].split(",")[1].split(":")

                # Verifys if the date is write correctly
                if(len(date) == 3 and date[0].isnumeric() and date[1].isnumeric() and date[2].isnumeric() and int(date[0]) > 0 and int(date[0]) <= datetime.now().year and int(date[1]) > 0 and int(date[1]) <= 12 and int(date[2]) > 0 and int(date[2]) <= 31):
                    begin_year = date[0]
                    begin_month = date[1]
                    begin_day = date[2]
                else:
                    print("ERROR: The date from parameter '-B' is wrong.")
                    error = True
                
                # Verifys if the time is write correctly
                if(len(hour_minute) == 2 and hour_minute[0].isnumeric() and hour_minute[1].isnumeric() and int(hour_minute[0]) >= 0 and int(hour_minute[0]) < 24 and int(hour_minute[1]) >= 0 and int(hour_minute[1]) < 60):
                    begin_hour = hour_minute[0]
                    begin_minute = hour_minute[1]
                else:
                    print("ERROR: The hour or minute from parameter '-B' is wrong.")
                    error = True
            else:
                print("ERROR: Parameter '-B' is wrong.")
                error = True

        # End date and time
        elif(argument_type == "E"):

            # Verifys if the parameter is write correctly
            if(len(parameter) > 2 and parameter[2] == ":" and parameter[3:].count(":") == 1 and parameter[3:].count("/") == 2 and parameter[3:].count(",") == 1):

                # Get year,month and day from the parameter
                date = parameter[3:].split(",")[0].split("/")

                # Get hour and minute from the parameter
                hour_minute = parameter[3:].split(",")[1].split(":")

                # Verifys if the date is write correctly
                if(len(date) == 3 and date[0].isnumeric() and date[1].isnumeric() and date[2].isnumeric() and int(date[0]) > 0 and int(date[0]) <= datetime.now().year and int(date[1]) > 0 and int(date[1]) <= 12 and int(date[2]) > 0 and int(date[2]) <= 31):
                    end_year = date[0]
                    end_month = date[1]
                    end_day = date[2]
                else:
                    print("ERROR: The date from parameter '-E' is wrong.")
                    error = True
                
                # Verifys if the time is write correctly
                if(len(hour_minute) == 2 and hour_minute[0].isnumeric() and hour_minute[1].isnumeric() and int(hour_minute[0]) >= 0 and int(hour_minute[0]) < 24 and int(hour_minute[1]) >= 0 and int(hour_minute[1]) < 60):
                    end_hour = hour_minute[0]
                    end_minute = hour_minute[1]
                else:
                    print("ERROR: The hour or minute from parameter '-E' is wrong.")
                    error = True
            else:
                print("ERROR: Parameter '-E' is wrong.")
                error = True

        # Frequency
        elif(argument_type == "F"):

            # Verifys which type of frequency and if the frequency is write correctly
            if(parameter[2:4] == "h:" and parameter[4:].isnumeric() and int(parameter[4:]) < 24  and int(parameter[4:]) > 0):
                frequency_hour = parameter[4:]
            elif(parameter[2:4] == "d:" and parameter[4:].isnumeric() and int(parameter[4:]) > 1):
                frequency_day = parameter[4:]
            elif(parameter[2:4] == "m:" and parameter[4:].isnumeric()):
                frequency_month = parameter[4:]
            else:
                print("ERROR: Parameter '-F' is wrong.")
                error = True

        # Download from Isolario
        elif(argument_type == "I"):

            download_from_Isolario = True

            # Verifys if the parameter is write correctly
            if(len(parameter) > 2 and parameter[2] == ":"):

                # Get the collectors
                collectors = parameter[3:].split(",")
                
                # Verifys if the collector are in the list of collectors (to see if they are write correctly and if the collector exists)
                for collector in collectors:
                    if(collector in collectors_Isolario):
                        chosen_collectors_Isolario = parameter[3:].split(",")
                    else:
                        print("ERROR: Collector '" + collector + "' was nos found in Isolario.")
                        error = True
            else:
                # If there is no other arguments in this parameter, than is to download from all the collectors from this project
                chosen_collectors_Isolario = collectors_Isolario

        # Download from RouteViews
        elif(argument_type == "V"):

            download_from_RouteViews = True

            # Verifys if the parameter is write correctly
            if(len(parameter) > 2 and parameter[2] == ":"):

                # Get the collectors
                collectors = parameter[3:].split(",")
                
                # Verifys if the collector are in the list of collectors (to see if they are write correctly and if the collector exists)
                for collector in collectors:
                    if(collector in collectors_RouteViews or collector in routeviews_specials):
                        chosen_collectors_RouteViews = parameter[3:].split(",")
                    else:
                        print("ERROR: Collector '" + collector + "' was nos found in RouteViews.")
                        error = True
            else:
                # If there is no other arguments in this parameter, than is to download from all the collectors from this project
                chosen_collectors_RouteViews = collectors_RouteViews + routeviews_specials

        # Download from RIPE
        elif(argument_type == "R"):

            download_from_RIPE = True

            # Verifys if the parameter is write correctly
            if(len(parameter) > 2 and parameter[2] == ":"):

                # Get the collectors
                collectors = parameter[3:].split(",")

                # Verifys if the collector are in the list of collectors (to see if they are write correctly and if the collector exists)
                for collector in collectors:
                    if(collector in collectors_RIPE):
                        chosen_collectors_RIPE = parameter[3:].split(",")
                    else:
                        print("ERROR: Collector '" + collector + "' was nos found in RIPE.")
                        error = True
            else:
                # If there is no other arguments in this parameter, than is to download from all the collectors from this project
                chosen_collectors_RIPE = collectors_RIPE

        # Number max of parallel downloads
        elif(argument_type == "P"):

            # Verifys if the parameter is write correctly
            if(parameter[2] == ":" and parameter[3:].isnumeric()):
                parallels_downloads = int(parameter[3:])
            else:
                print("ERROR: Parameter '-P' is wrong.")
                error = True

        # Path to save the downloaded files
        elif(argument_type == "S"):

            # Verifys if the parameter is write correctly
            if(parameter[2] == ":"):

                # Verifys if the path exists
                if(path.exists(parameter[3:])):
                    save_file_path = parameter[3:]
                else:
                    print("ERROR: Save path from parameter '-S' is wrong.")
                    error = True
            else:
                print("ERROR: Parameter '-S' is wrong.")
                error = True
        else:
            print("ERROR: Parameter '" + argument_type + "' is invalid.")
            error = True

obj_calendar = calendar.Calendar(6)

# Verify if date is correct
if(not error):
    begin_real_days = obj_calendar.itermonthdays(int(begin_year), int(begin_month))
    end_real_days = obj_calendar.itermonthdays(int(end_year), int(end_month))
    
    # Verify if the dates really exists
    if(int(begin_day) not in begin_real_days):
        error = True
        print("ERROR: Begin day doesn't exist.")
    elif(int(end_day) not in end_real_days):
        error = True
        print("ERROR: End day doesn't exist.")
    # Begin date and time must be before the end date and time
    elif(int(begin_year) > int(end_year)):
        error = True
        print("ERROR: Begin year must be less than end year.")
    elif(int(begin_year) == int(end_year)):
        if(int(begin_month) > int(end_month)):
            error = True
            print("ERROR: Begin month must be less than end month.")
        elif(int(begin_month) == int(end_month)):
            if(int(begin_day) > int(end_day)):
                error = True
                print("ERROR: Begin day must be less than end day.")
            elif(int(begin_day) == int(end_day)):
                if(int(begin_hour) > int(end_hour)):
                    error = True 
                    print("ERROR: Begin hour must be less than end hour.")
                elif(int(begin_hour) == int(end_hour)):
                    if(int(begin_minute) > int(end_minute)):
                        error = True
                        print("ERROR: Begin minute must be less than end minute.") 
                    elif(int(begin_minute) == int(end_minute)):
                        error = True 
                        print("ERROR: Begin time must be different from end time.") 




###### CREATE THE URL's LIST ######

# Verifys if there is no error in the paramenters
if(not(error)):

    # Verify the save_file_path
    if(save_file_path != ""):

        # Verify if the path has "/" at the end
        if(save_file_path[-1] != "/"):
            save_file_path.append("/")
    else:
        save_file_path = "Data/"

    # Verfiy if the path exists
    if(not path.exists(save_file_path)):
        # If not, create one
        os.mkdir(save_file_path[-1])

    # Verfiy if the path 'save_file_path/RIBS' exists
    if(not path.exists(save_file_path + "RIBS/")):
        # If not, create one
        os.mkdir(save_file_path + "RIBS")

    # Verfiy if the path 'save_file_path/UPDATES' exists
    if(not path.exists(save_file_path + "UPDATES/")):
        # If not, create one
        os.mkdir(save_file_path + "UPDATES")

    # Initialize the lists to save the URL's from each project
    url_list_Isolario = []
    url_list_RouteViews = []
    url_list_RIPE = []

    # Create a list with the days between the beginning and the end (the begin date and end date are included)
    list_dates = ListDays(int(begin_year), int(begin_month), int(begin_day), int(end_year), int(end_month), int(end_day))

    # Update the above list to add the time for each day
    # This list will be the base to download the datas, because the 'parameters' of the files are the date and the time
    list_dates = ListHourAndMinute(list_dates,int(begin_hour),int(begin_minute),int(end_hour),int(end_minute),int(frequency_hour))

    # Create the URL's for Isolario
    if(download_from_Isolario):

        # Gets the chosen collectors
        for collector in list(chosen_collectors_Isolario):

            # Create the URL's prefix with the chosen collector
            url_collector = url_prefix_Isolario + collector + "/"
            
            # Iterates through the selected dates
            for date in list_dates:

                # Adds the date to the URL's prefix
                url = url_collector + str(date[0]) + "_" + AdjustNumberString(date[1]) + "/"

                # Adds the RIB and the rest of the file name to be downloaded
                if(download_RIBS):
                    url_rib = url + "rib." + str(date[0]) + AdjustNumberString(date[1]) + AdjustNumberString(date[2]) + "." + str(date[3]) + str(date[4]) + ".bz2"

                    # Saves the URL to the list
                    url_list_Isolario.append(url_rib)

                # Adds the UPDATE and the rest of the file name to be downloaded
                if(download_UPDATES):
                    url_update = url + "updates." + str(date[0]) + AdjustNumberString(date[1]) + AdjustNumberString(date[2]) + "." + str(date[3]) + str(date[4]) + ".bz2"

                    # Saves the URL to the list
                    url_list_Isolario.append(url_update)  

    # Create the URL's for RouteViews
    if(download_from_RouteViews):

        # Gets the chosen collectors
        for collector in list(chosen_collectors_RouteViews):

            # Verifys which collecter was chosen, beacause depending on the collector, the final URL will be a different pattern
            # Create the URL's prefix with the chosen collector
            if(collector == "route-views2"):
                url_collector = url_prefix_RouteViews + "bgpdata/"
            elif(collector == "route-views3" or collector == "route-views4"):
                url_collector = url_prefix_RouteViews + collector + "/bgpdata/"
            elif(collector in collectors_RouteViews):
                if(collector == "saopaulo2"):
                    url_collector = url_prefix_RouteViews + "route-views2.saopaulo/bgpdata/"
                else:
                    url_collector = url_prefix_RouteViews + "route-views." + collector + "/bgpdata/"

            # Iterates through the selected dates
            for date in list_dates:

                # Adds the date to the URL's prefix
                url = url_collector + str(date[0]) + "." + AdjustNumberString(date[1]) + "/"

                # Adds the RIB and the rest of the file name to be downloaded
                if(download_RIBS):
                    url_rib = url + "RIBS/rib." + str(date[0]) + AdjustNumberString(date[1]) + AdjustNumberString(date[2]) + "." + str(date[3]) + str(date[4]) + ".bz2"
                    
                    # Saves the URL to the list
                    url_list_RouteViews.append(url_rib)

                # Adds the UPDATE and the rest of the file name to be downloaded
                if(download_UPDATES):
                    url_update = url + "UPDATES/updates." + str(date[0]) + AdjustNumberString(date[1]) + AdjustNumberString(date[2]) + "." + str(date[3]) + str(date[4]) + ".bz2"
                    
                    # Saves the URL to the list
                    url_list_RouteViews.append(url_update)  

    # Create the URL's for RIPE
    if(download_from_RIPE):

        # Gets the chosen collectors
        for collector in list(chosen_collectors_RIPE):

            # Create the URL's prefix with the chosen collector
            url_collector = url_prefix_RIPE + collector + "/"

            # Iterates through the selected dates
            for date in list_dates:

                # Adds the date to the URL's prefix
                url = url_collector + str(date[0]) + "." + AdjustNumberString(date[1]) + "/"

                # Adds the RIB and the rest of the file name to be downloaded
                if(download_RIBS):
                    url_rib = url + "bview." + str(date[0]) + AdjustNumberString(date[1]) + AdjustNumberString(date[2]) + "." + str(date[3]) + str(date[4]) + ".gz"

                    # Saves the URL to the list
                    url_list_RIPE.append(url_rib)

                # Adds the UPDATE and the rest of the file name to be downloaded
                if(download_UPDATES):
                    url_update = url + "updates." + str(date[0]) + AdjustNumberString(date[1]) + AdjustNumberString(date[2]) + "." + str(date[3]) + str(date[4]) + ".gz"

                    # Saves the URL to the list
                    url_list_RIPE.append(url_update)


    ###### DOWNLOAD THE FILES ######

    # Initializes the list for the logs of the downloads from Isolario
    error_log_Isolario = []

    ssl._create_default_https_context = ssl._create_unverified_context

    threads_Isolario = []

    for thread_index in range(0,parallels_downloads):
        threads_Isolario.append(threading.Thread(target=DownloadFromIsolario, args=()))
        threads_Isolario[thread_index].start()

    # Iterates through the sublists
    #for url_list in url_list_Isolario:
        # Initialize the thread with the list of URLs
        # The name of the project is to identify the thread to know which error log list to write on
        #thread_Isolario = threading.Thread(target=DownloadURLs, args=(url_list,"Isolario"))
        #thread_Isolario.start()


    # Iterates through the URL's from Isolario
    #for url in url_list_Isolario:

        # Try to download from the URL
    #    try: 
    #        print("\nDownloading the file '" + url.split("/")[-1] + "' from Isolario.")
    #        wget.download(url, out='Data/')
    #    except: # If occurs an error...

            # Create a log for the error
    #        error_log = "Failed to download the file '" + url.split("/")[-1] + "' from Isolario."
    #        print(error_log)

            # Save the log into the list
    #        error_log_Isolario.append(error_log + "\n")
    

    # Initializes the list for the logs of the downloads from RouteViews
    error_log_RouteViews = []

    threads_RouteViews = []

    for thread_index in range(0,parallels_downloads):
        threads_RouteViews.append(threading.Thread(target=DownloadFromRouteViews, args=()))
        threads_RouteViews[thread_index].start()

    # Iterates through the sublists
    #for url_list in url_list_RouteViews:
        # Initialize the thread with the list of URLs
        # The name of the project is to identify the thread to know which error log list to write on
        #thread_RouteViews = threading.Thread(target=DownloadURLs, args=(url_list,"RouteViews"))
        #thread_RouteViews.start()

    # Iterates through the URL's from RouteViews
    #for url in url_list_RouteViews:

        # Try to download from the URL
    #    try:
    #        print("\nDownloading the file '" + url.split("/")[-1] + "' from RouteViews.")
    #        wget.download(url, out='Data/')
    #    except: # If occurs an error...

            # Create a log for the error
    #        error_log = "Failed to download the file '" + url.split("/")[-1] + "' from RouteViews."
    #        print(error_log)

            # Save the log into the list
    #        error_log_RouteViews.append(error_log + "\n")


    # Initializes the list for the logs of the downloads from RIPE
    error_log_RIPE = []

    threads_RIPE = []

    for thread_index in range(0,parallels_downloads):
        threads_RIPE.append(threading.Thread(target=DownloadFromRIPE, args=()))
        threads_RIPE[thread_index].start()

    # Iterates through the sublists
    #for url_list in url_list_RIPE:
        # Initialize the thread with the list of URLs
        # The name of the project is to identify the thread to know which error log list to write on
        #thread_RIPE = threading.Thread(target=DownloadURLs, args=(url_list,"RIPE"))
        #thread_RIPE.start()

    # Iterates through the URL's from RIPE
    #for url in url_list_RIPE:

        # Try to download from the URL
    #    try:
    #        print("\nDownloading the file '" + url.split("/")[-1] + "' from RIPE.")
    #        wget.download(url, out='Data/')
    #    except: # If occurs an error...

            # Create a log for the error
    #        error_log = "Failed to download the file '" + url.split("/")[-1] + "' from RIPE."
    #        print(error_log)

            # Save the log into the list
    #        error_log_RIPE.append(error_log + "\n")


    ###### CREATING THE LOG ERROR FILES ######

    # Wait for all the threads to finish
    for thread_index in range(0,parallels_downloads):
        threads_Isolario[thread_index].join()
        threads_RouteViews[thread_index].join()
        threads_RIPE[thread_index].join()

    # Verifys if a directory for the logs exists
    if(not path.exists("Downloader Logs/")):

        # If not, create one
        os.mkdir("Downloader Logs")

    # Verifys if a directory for the logs of Isolario exists
    if(not path.exists("Downloader Logs/Isolario/")):

        # If not, create one
        os.mkdir("Downloader Logs/Isolario")

    # Verifys if a directory for the logs of RouteViews exists
    if(not path.exists("Downloader Logs/RouteViews/")):

        # If not, create one
        os.mkdir("Downloader Logs/RouteViews")

    # Verifys if a directory for the logs of RIPE exists
    if(not path.exists("Downloader Logs/RIPE/")):

        # If not, create one
        os.mkdir("Downloader Logs/RIPE")

    # Gets the current date and time 
    now = datetime.now()

    # Verifys if there is logs for Isolario
    if(len(error_log_Isolario) > 0):

        # Create the file inside de correct directory, with the current date and time in the file name
        error_log_Isolario_file = open ("Downloader Logs/Isolario/Log-" + now.strftime("%Y-%m-%d_%H:%M:%S") + ".txt", "w")

        # Write the logs in the file
        error_log_Isolario_file.writelines(error_log_Isolario)

        # Close the file
        error_log_Isolario_file.close()

    # Verifys if there is logs for RouteViews
    if(len(error_log_RouteViews) > 0):

        # Create the file inside de correct directory, with the current date and time in the file name
        error_log_RouteViews_file = open ("Downloader Logs/RouteViews/Log-" + now.strftime("%Y-%m-%d_%H:%M:%S") + ".txt", "w")

        # Write the logs in the file
        error_log_RouteViews_file.writelines(error_log_RouteViews)

        # Close the file
        error_log_RouteViews_file.close()

    # Verifys if there is logs for RIPE
    if(len(error_log_RIPE) > 0):

        # Create the file inside de correct directory, with the current date and time in the file name
        error_log_RIPE_file = open ("Downloader Logs/RIPE/Log-" + now.strftime("%Y-%m-%d_%H:%M:%S") + ".txt", "w")
        
        # Write the logs in the file
        error_log_RIPE_file.writelines(error_log_RIPE)

        # Close the file
        error_log_RIPE_file.close()

    
    
    

    
    
    
