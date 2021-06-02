# @Code created by Guilherme Silva de Castro on april 2021 and last updated on june 2021.@

##########################################################
# This code will download the files that will be used in the prepending_policies code, based on the files got from the 
# GitHub repository (https://github.com/pedrobmarcos/prependingPolicies). The files from the repository must be already
# downloaded, the IPv4 (v4_sane_policies_DATE.gz) and IPv6 (v6_sane_policies_DATE.gz) files must be inside the folder 
# "Prepending Policies Files/IPv4 OR IPv6", depending on the file. The downloaded files from this code will be in the 
# directory "Files Regions/REGION NAME".


############################################################
# TO DO AND IDEAS:
# [ ] - Adjust the code, some parts are doing some useless stuff.
# [ ] - Create a file with the files that generate an error.

############################################################
# KNOWN ISSUES:
# The files from the repository can't be downloaded using wget.

import wget
from datetime import datetime
import os
from os import path

# Download the files from the AFRINIC.
def DownloadAFRINIC(list_files):

    # Link pattern:
    # https://ftp.lacnic.net/pub/stats/afrinic/2010/delegated-afrinic-20100101
    prefix_file_name = "delegated-afrinic-"
    prefix_url = "https://ftp.lacnic.net/pub/stats/afrinic/"

    error = []

    for file in list_files:
        url_file = ""
        url_file += prefix_url

        list_date = file.split("_")
        date_file = list_date[-1][:-3]
        date = []
        date.append(date_file[:4])
        date.append(date_file[4:6])
        date.append(date_file[6:])

        url_file += date[0] + "/"

        file_name = prefix_file_name + date[0] + date[1] + date[2]

        url_file += file_name

        if(file_name not in os.listdir("Files Regions/AFRINIC")):
            try:
                wget.download(url_file,out='Files Regions/AFRINIC/')
            except:
                error.append(url_file)

    return error

# Download the files from the APNIC.
def DownloadAPNIC(list_files):

    # Link pattern:
    # https://ftp.lacnic.net/pub/stats/apnic/2020/delegated-apnic-20201130.gz
    prefix_file_name = "delegated-apnic-"
    prefix_url = "https://ftp.lacnic.net/pub/stats/apnic/"

    error = []

    for file in list_files:
        url_file = ""
        url_file += prefix_url

        list_date = file.split("_")
        date_file = list_date[-1][:-3]
        date = []
        date.append(date_file[:4])
        date.append(date_file[4:6])
        date.append(date_file[6:])

        url_file += date[0] + "/"

        file_name = prefix_file_name + date[0] + date[1] + date[2] + ".gz"

        url_file += file_name

        if(file_name not in os.listdir("Files Regions/APNIC")):
            try:
                wget.download(url_file,out='Files Regions/APNIC/')
            except:
                error.append(url_file)

    return error

# Download the files from the LACNIC.
def DownloadLACNIC(list_files):

    # Link pattern:
    # https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-20111101

    prefix_url = "https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-"

    error = []

    for file in list_files:
        url_file = ""
        url_file += prefix_url

        list_date = file.split("_")
        date_file = list_date[-1][:-3]
        date = []
        date.append(date_file[:4])
        date.append(date_file[4:6])
        date.append(date_file[6:])

        file_name = "delegated-lacnic-" + date[0] + date[1] + date[2]

        url_file +=  date[0] + date[1] + date[2]

        if(file_name not in os.listdir("Files Regions/LACNIC")):
            try:
                wget.download(url_file,out='Files Regions/LACNIC/')
            except:
                error.append(url_file)

    return error

# Download the files from the RIPENCC.
def DownloadRIPENCC(list_files):

    # Link pattern:
    # https://ftp.lacnic.net/pub/stats/ripencc/2020/delegated-ripencc-20200318.bz2
    prefix_file_name = "delegated-ripencc-"
    prefix_url = "https://ftp.lacnic.net/pub/stats/ripencc/"

    error = []

    for file in list_files:
        url_file = ""
        url_file += prefix_url

        list_date = file.split("_")
        date_file = list_date[-1][:-3]
        date = []
        date.append(date_file[:4])
        date.append(date_file[4:6])
        date.append(date_file[6:])

        url_file += date[0] + "/"

        file_name = prefix_file_name + date[0] + date[1] + date[2] + ".bz2"

        url_file += file_name

        if(file_name not in os.listdir("Files Regions/RIPENCC")):
            try:
                wget.download(url_file,out='Files Regions/RIPENCC/')
            except:
                error.append(url_file)

    return error

# Download the files from the ARIN.
def DownloadARIN(list_files):

    # Links pattern (until the year 2016, the path is different from the other, and the files names change at some point):
    # https://ftp.lacnic.net/pub/stats/arin/archive/2010/delegated-arin-20100101
    # https://ftp.lacnic.net/pub/stats/arin/archive/2016/delegated-arin-extended-20160602
    # https://ftp.lacnic.net/pub/stats/arin/delegated-arin-extended-20170101

    prefix_file_name1 = "delegated-arin-"
    prefix_file_name2 = "delegated-arin-extended-"
    prefix_url1 = "https://ftp.lacnic.net/pub/stats/arin/archive/"
    prefix_url2 = "https://ftp.lacnic.net/pub/stats/arin/delegated-arin-extended-"

    error = []

    for file in list_files:

        list_date = file.split("_")
        date_file = list_date[-1][:-3]
        date = []
        date.append(date_file[:4])
        date.append(date_file[4:6])
        date.append(date_file[6:])

        if(int(date[0]) > 2016):
            url_file = ""
            url_file += prefix_url2

            file_name = "delegated-arin-extended-" + date[0] + date[1] + date[2]

            url_file += date[0] + date[1] + date[2]

            if(file_name not in os.listdir("Files Regions/ARIN")):
                try:
                    wget.download(url_file,out='Files Regions/ARIN/')
                except:
                    error.append(url_file)
        else:
            url_file = ""
            url_file += prefix_url1 + date[0] + "/" + prefix_file_name1 + date[0] + date[1] + date[2]

            file_name = prefix_file_name1 + date[0] + date[1] + date[2]

            if(file_name not in os.listdir("Files Regions/ARIN")):
                try:
                    wget.download(url_file,out='Files Regions/ARIN/')
                except:
                    url_file = ""
                    url_file += prefix_url1 + date[0] + "/" + prefix_file_name2 + date[0] + date[1] + date[2]
                    
                    file_name = prefix_file_name2 + date[0] + date[1] + date[2]
                    if(file_name not in os.listdir("Files Regions/ARIN")):
                        try:
                            wget.download(url_file,out='Files Regions/ARIN/')
                        except:
                            error.append(url_file)

    return error


# Create the needed folders.
if(not path.exists("Files Regions/")):
    os.mkdir("Files Regions")

if(not path.exists("Files Regions/APNIC/")):
    os.mkdir("Files Regions/APNIC")

if(not path.exists("Files Regions/ARIN/")):
    os.mkdir("Files Regions/ARIN")

if(not path.exists("Files Regions/LACNIC/")):
    os.mkdir("Files Regions/LACNIC")

if(not path.exists("Files Regions/AFRINIC/")):
    os.mkdir("Files Regions/AFRINIC")

if(not path.exists("Files Regions/RIPENCC/")):
    os.mkdir("Files Regions/RIPENCC")

if(not path.exists("Prepending Policies Files/")):
    os.mkdir("Prepending Policies Files")

if(not path.exists("Prepending Policies Files/IPv4/")):
    os.mkdir("Prepending Policies Files/IPv4")

if(not path.exists("Prepending Policies Files/IPv6/")):
    os.mkdir("Prepending Policies Files/IPv6")

# Get the current date.
now = datetime.now()

# Get the files from IPv4 and IPv6.
list_files_ipv4 = os.listdir("Prepending Policies Files/IPv4")
list_files_ipv6 = os.listdir("Prepending Policies Files/IPv6")

# Add the to lists in to one.
list_files = list_files_ipv4 + list_files_ipv6
# Remove the repeated files.
list_files = list(set(list_files))
list_files.sort()


# Download the files from each region based on the list of files.
DownloadAFRINIC(list_files)
DownloadAPNIC(list_files)
DownloadLACNIC(list_files)
DownloadRIPENCC(list_files)
DownloadARIN(list_files)