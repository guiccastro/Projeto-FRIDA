### (*)DATA TYPE(*) ### 
# -t -> download only RIBs data
# -T -> download only UPDATE data

### (*)BEGIN AND END DATE(*) ###
# -B:year/month/day,hour:minute
# -E:year/month/day,hour:minute

### FREQUENCY ###
# -Fh:n
# -Fd:n
# -Fm:n

### PROJECT ###
# -I -> download data from Isolario
# -V -> download data from RouteViews
# -R -> download data from RIPE

### COLLECTOR ###
# -I:a,b,c
# -V:a,b,c
# -R:a,b,c

### NUMBER OF PARALLEL DOWNLOADS ###
# -P:n

### PATH TO SAVE FILE ###
# -S:path

import wget
import sys
import os
import calendar
from multiprocessing import Pool

def CreatListFromIterator(iterator):
    list_days = []
    for day in iterator:
        if(day != 0):
            list_days.append(day)
    
    return list_days

def ListDays(b_year,b_month,b_day,e_year,e_month,e_day):

    obj_calendar = calendar.Calendar(6)

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

def AdjustNumberString(number_int):
    if(number_int < 10):
        return "0" + str(number_int)
    else:
        return str(number_int)

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


def GetDateFromFrequencyDay(list_date,frequency_day):
    index = 0
    new_date_list = []
    while(index < len(list_date)):
        new_date_list.append(list_date[index])
        index += frequency_day

    if(new_date_list[-1] != list_date[-1]):
        new_date_list.append(list_date[-1])

    return new_date_list

    

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

download_RIBS = False
download_UPDATES = False

beging_year = ""
beging_month = ""
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

parallels_downloads = 0

save_file_path = ""


parameters = sys.argv[1:]

for parameter in list(parameters):
    if(parameter[0] != "-"):
        print("ERROR: Character '-' is missing.")
    else:
        argument_type = parameter[1]

        if(argument_type == "t"):
            download_RIBS = True

        elif(argument_type == "T"):
            download_UPDATES = True

        elif(argument_type == "B"):
            if(len(parameter) > 2 and parameter[2] == ":" and parameter[3:].count(":") == 1 and parameter[3:].count("/") == 2 and parameter[3:].count(",") == 1):
                date = parameter[3:].split(",")[0].split("/")
                hour_minute = parameter[3:].split(",")[1].split(":")

                if(len(date) == 3 and date[0].isnumeric() and date[1].isnumeric() and date[2].isnumeric()):
                    beging_year = date[0]
                    beging_month = date[1]
                    begin_day = date[2]
                else:
                    print("ERROR: The date from parameter '-B' is wrong.")
                
                if(len(hour_minute) == 2 and hour_minute[0].isnumeric() and hour_minute[1].isnumeric()):
                    begin_hour = hour_minute[0]
                    begin_minute = hour_minute[1]
                else:
                    print("ERROR: The hour or minute from parameter '-B' is wrong.")
            else:
                print("ERROR: Parameter '-B' is wrong.")

        elif(argument_type == "E"):
            if(len(parameter) > 2 and parameter[2] == ":" and parameter[3:].count(":") == 1 and parameter[3:].count("/") == 2 and parameter[3:].count(",") == 1):
                date = parameter[3:].split(",")[0].split("/")
                hour_minute = parameter[3:].split(",")[1].split(":")

                if(len(date) == 3 and date[0].isnumeric() and date[1].isnumeric() and date[2].isnumeric()):
                    end_year = date[0]
                    end_month = date[1]
                    end_day = date[2]
                else:
                    print("ERROR: The date from parameter '-E' is wrong.")
                
                if(len(hour_minute) == 2 and hour_minute[0].isnumeric() and hour_minute[1].isnumeric()):
                    end_hour = hour_minute[0]
                    end_minute = hour_minute[1]
                else:
                    print("ERROR: The hour or minute from parameter '-E' is wrong.")
            else:
                print("ERROR: Parameter '-E' is wrong.")

        elif(argument_type == "F"):
            if(parameter[2:4] == "h:" and parameter[4:].isnumeric() and int(parameter[4:]) < 24  and int(parameter[4:]) > 0):
                frequency_hour = parameter[4:]
            elif(parameter[2:4] == "d:" and parameter[4:].isnumeric() and int(parameter[4:]) > 1):
                frequency_day = parameter[4:]
            elif(parameter[2:4] == "m:" and parameter[4:].isnumeric()):
                frequency_month = parameter[4:]
            else:
                print("ERROR: Parameter '-F' is wrong.")

        elif(argument_type == "I"):
            download_from_Isolario = True
            if(len(parameter) > 2 and parameter[2] == ":"):
                chosen_collectors_Isolario = parameter[3:].split(",")

        elif(argument_type == "V"):
            download_from_RouteViews = True
            if(len(parameter) > 2 and parameter[2] == ":"):
                chosen_collectors_RouteViews = parameter[3:].split(",")

        elif(argument_type == "R"):
            download_from_RIPE = True
            if(len(parameter) > 2 and parameter[2] == ":"):
                chosen_collectors_RIPE = parameter[3:].split(",")

        elif(argument_type == "P"):
            if(parameter[2] == ":" and parameter[3:].isnumeric()):
                parallels_downloads = int(parameter[3:])
            else:
                print("ERROR: Parameter '-P' is wrong.")

        elif(argument_type == "S"):
            if(parameter[2] == ":"):
                save_file_path = parameter[3:]
            else:
                print("ERROR: Parameter '-S' is wrong.")

        else:
            print("ERROR: Parameter '" + argument_type + "' is invalid.")


url_list_Isolario = []
url_list_RouteViews = []
url_list_RIPE = []

list_dates = ListDays(int(beging_year), int(beging_month), int(begin_day), int(end_year), int(end_month), int(end_day))

list_dates = ListHourAndMinute(list_dates,int(begin_hour),int(begin_minute),int(end_hour),int(end_minute),int(frequency_hour))

if(download_from_Isolario):
    for collector in list(chosen_collectors_Isolario):
        url_collector = url_prefix_Isolario + collector + "/"
        
        for date in list_dates:
            url = url_collector + str(date[0]) + "_" + AdjustNumberString(date[1]) + "/"

            if(download_RIBS):
                url_rib = url + "rib." + str(date[0]) + AdjustNumberString(date[1]) + AdjustNumberString(date[2]) + "." + str(date[3]) + str(date[4]) + ".bz2"
                url_list_Isolario.append(url_rib)

            if(download_UPDATES):
                url_update = url + "updates." + str(date[0]) + AdjustNumberString(date[1]) + AdjustNumberString(date[2]) + "." + str(date[3]) + str(date[4]) + ".bz2"
                url_list_Isolario.append(url_update)  


if(download_from_RouteViews):
    for collector in list(chosen_collectors_RouteViews):
        error = False
        if(collector == "route-views2"):
            url_collector = url_prefix_RouteViews + "bgpdata/"
        elif(collector == "route-views3" or collector == "route-views4"):
            url_collector = url_prefix_RouteViews + collector + "/bgpdata/"
        elif(collector in collectors_RouteViews):
            if(collector == "saopaulo2"):
                url_collector = url_prefix_RouteViews + "route-views2.saopaulo/bgpdata/"
            else:
                url_collector = url_prefix_RouteViews + "route-views." + collector + "/bgpdata/"
        else:
            error = True
            print("ERROR: Collector '" + collector + "' was nos found in RouteViews.")

        if(not(error)):
            for date in list_dates:
                url = url_collector + str(date[0]) + "." + AdjustNumberString(date[1]) + "/"

                if(download_RIBS):
                    url_rib = url + "RIBS/rib." + str(date[0]) + AdjustNumberString(date[1]) + AdjustNumberString(date[2]) + "." + str(date[3]) + str(date[4]) + ".bz2"
                    url_list_RouteViews.append(url_rib)

                if(download_UPDATES):
                    url_update = url + "UPDATES/updates." + str(date[0]) + AdjustNumberString(date[1]) + AdjustNumberString(date[2]) + "." + str(date[3]) + str(date[4]) + ".bz2"
                    url_list_RouteViews.append(url_update)  


if(download_from_RIPE):
    for collector in list(chosen_collectors_RIPE):
        url_collector = url_prefix_RIPE + collector + "/"

        for date in list_dates:
            url = url_collector + str(date[0]) + "." + AdjustNumberString(date[1]) + "/"

            if(download_RIBS):
                url_rib = url + "bview." + str(date[0]) + AdjustNumberString(date[1]) + AdjustNumberString(date[2]) + "." + str(date[3]) + str(date[4]) + ".gz"
                url_list_RIPE.append(url_rib)

            if(download_UPDATES):
                url_update = url + "updates." + str(date[0]) + AdjustNumberString(date[1]) + AdjustNumberString(date[2]) + "." + str(date[3]) + str(date[4]) + ".gz"
                url_list_RIPE.append(url_update)

#def DownloadURL(url):
#    try:
#        wget.download(url, out='Data/')
#        print("Baixou")
#        final_time = time.time() - start
#        print("\n" + str(final_time) + "\n")
#    except:
#        print("Não achou")
#
#import threading
#import time
#
#start = time.time()
#
#threads = list()
#for index in range(3):
#    x = threading.Thread(target=DownloadURL, args=(url_list_RouteViews[index],))
#    threads.append(x)
#    x.start()
#
#for index in range(3):
#    try:
#        wget.download(url_list_RouteViews[index], out='Data/')
#        print("Baixou")
#    except:
#        print("Não achou")


for url in url_list_Isolario:
    try:
        wget.download(url, out='Data/')
        print("Baixou")
    except:
        print("Não achou")

for url in url_list_RouteViews:
    try:
        wget.download(url, out='Data/', bar=bar_thermometer)
        print("Baixou")
    except:
        print("Não achou")

for url in url_list_RIPE:
    try:
        wget.download(url, out='Data/')
        print("Baixou")
    except:
        print("Não achou")