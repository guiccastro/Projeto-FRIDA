# downloader.py

This code can download the MRT data files from the Isolario, RouteViews or RIPE project from all of its collectors. The downloaded files will be in the path that user pass as the parameter, if the path is passed, than the default path is ``downloader.py-PATH/Data``. Some error logs can be generated by the code. Each project will have a separate directory to keep its logs from the download errors. The directories are: ``downloader.py-PATH/Downloader Logs/PROJECT NAME``. The logs will have name in the pattern: ``Log-DATE``, the date is to tell the user which date file could not be downloaded.

## Dependencies:
- Wget (Download the files)
- Sys (Read the parameters)
- OS (Create directories, verifies if a path exists)
- Calendar (Get access to a calendar)
- Datetime (Get the current date and time)
- Threading (Create threads)
- SSL (Configure https context)

## Parameters:

### __Data type__:
``-t`` => Download RIBs data.

``-T`` => Download UPDATE data.

You must pass one of the parameters, otherwise the code will not generate any URL.

### __Begin and end date__:
``-B:year/month/day,hour:minute`` => The first data to be downloaded

``-E:year/month/day,hour:minute`` => The last data to be downloaded

### __Frequency__:
``-Fh:n`` => Download the data every ``n`` hours between the begin and end date.

### __Project__:
``-I`` => Download data from the project Isolario.

``-V`` => Download data from the project RouteViews.

``-R`` => Download data from the project RIPE.

### __Collector__:
``-I:a,b,c,...`` => Download the data from collectors ``a``, ``b``, ``c``, ..., from project Isolario.

``-V:a,b,c,...`` => Download the data from collectors ``a``, ``b``, ``c``, ..., from project RouteViews.

``-R:a,b,c,...`` => Download the data from collectors ``a``, ``b``, ``c``, ..., from project RIPE.

To download from all collectors from a project you just need to pass none collector in the parameter (e.g., to download from all collectors from Isolario, pass the parameter like '-I').

### __Number of parallel downloads__:
``-P:n`` => Download ``n`` parallel files from each project.

If not passed, the code will download all files linearly.

### __Path to save file__:
``-S:path`` => Save the downloaded files in ``path``.

If not passed, the default path is "Data/". The path doesn't need to exist, because the code will create the directory, but the path must be in the same directory as this code, otherwise wget will not download the file.

## Example:
    $ python3 downloader.py -t -B:2021/04/01,00:00 -E:2021/04/02,20:00 -Fh:3 -V:saopaulo -P:3
  
In this example, you will download only RIB files from the project RouteViews of its collector S??o Paulo. The files will be downloaded from the first day of April of 2021 until the second day of April of 2021, in every 3 hours. The code will download three files in the same time.

    $ python3 downloader.py -t -T -B:2021/04/01,00:00 -E:2021/04/02,20:00 -Fh:2 -I -P:3
    
If you want to try a longer test, you can use the above example. Here you will download the RIB and UPDATE files from the same date from the previous example, but you will download from all the collectors from project Isolario. The frequency of download will be in every 2 hours, which will increase the number of downloaded files. Feel free to modify the paramenters and make some tests.

# sanitizer.py

This code will read the data from the MRT files, remove the ones with invalids prefixes and routes, and create a new file with the sanitized data. The bogons that will be download will be keeped in the path "Bogons/". The sanitized files will be in the path "Sanitized Data/". The error logs will be in the path "Sanitizer Logs/" with a name in the pattern: "Log-Bogons-DATE".

## Dependencies:
- OS (List directories, use terminal by code and create directory, verifies if a path exists)
- PyTricia (Create a Tree to keep the prefixes)
- Sys (Read the parameters)
- Wget (Download the files)
- Gzip (Open and create .gz files)
- Datetime (Get the current date and time)
- Threading (Create threads)

## Parameters:

### __Filter type__:

``-f`` => Filter by bogons.
``-F`` => Filter by fullbogons.

This parameters only need to be passed if the filtration will not use a user's list, otherwise it will generate no effect.

### __User list__:

``-L:path`` => Use a file given by the user to filter the data.

It needs to be passed with the path and the name of the file.

### __User list__:

``-P:path`` => Path to where the data to be sanitized is.

If not passed, the default path is the directorie "Data/".

## Example:
    $ python3 sanitizer.py -F
  
In this example, the code will download the fullbogons based on the date from each MRT file and use them to filter the data. Here, if you want to try a longer test, you just need to download more files to be sanitized. There is a variable in this code which allows you to determine how many parallel sanitizations the code will run, the varible is called ``parallel_sanitization``, and its default value it's 2, but you can change this value if you want (just be warned that the more parallel sanitizations, the slower the computer can get).

# download_policies_files.py

This code will download the files that will be used in the prepending_policies code, based on the files got from the GitHub repository (https://github.com/pedrobmarcos/prependingPolicies). The files from the repository must be already downloaded, the IPv4 (``v4_sane_policies_DATE.gz``) and IPv6 (``v6_sane_policies_DATE.gz``) files must be inside the folder ``Prepending Policies Files/IPv4 OR IPv6``, depending on the file. The downloaded files from this code will be in the directory ``Files Regions/REGION NAME``.

## Dependencies:
- Wget (Download the files)
- Datetime (Get the current date and time)
- OS (List directories, create directory, verifies if a path exists)

# prepending_policies.py

This file will read some files that contain infos about the prepending policies by prefix and AS's numbers, and some files that contain infos about the allocated AS's numbers per country. The idea is to create a new file with infos about the number of used prepending policies by countries and regions. The final files will be saved in the path ``Policies/IPv4 OR IPv6``, so, the final files from IPv4 and IPv6 stay in different directories. The name of the final file has the pattern ``Policie-DATE`` numbers and must be in the directory ``Prepending Policies Files/IPv4 OR IPv6``.

The first files are from [this repository](https://github.com/pedrobmarcos/prependingPolicies). Here you can download the files with the name ``v4 OR v6_sane_policies_DATE.gz``. This files contain the infos about the prepending policies by prefix and AS's numbers.

The second files can be downloaded from each region. Here you must found the files that you want, because the project's sites are a little bit confused.  This files must be in the directory ``Files Regions/REGION NAME``.
- [APNIC](https://ftp.apnic.net/apnic/stats/apnic/)
- [ARIN](https://ftp.arin.net/pub/stats/arin/)
- [LACNIC](https://ftp.lacnic.net/pub/stats/lacnic/)
- [AFRINIC](https://ftp.afrinic.net/pub/stats/afrinic/)
- [RIPENCC](https://ftp.ripe.net/pub/stats/ripencc/)

``To download the second files automatically, use the code download_policies_files.py.``

## Dependencies:
- Gzip (Open .gz files)
- Bz2 (Open .bz2 files)
- OS (List directories)

# plot_policies.py

This code will read the file generated by the prepending_policies.py and create a plot. The plot will be saved as a .pdf file. If you want to gerenate a plot using others informations in the file, you need to change this on code, because the main code for this function is the web_plot_policies.py that will be explained next.

## Dependencies:
- Cartopy (Geometries infos of the countries for the plot)
- Matplotlib (Create a plot)
- Pycountry (Codes and names of the countries) (Cartopy has codes and names of the countries too, but some infos are missing, Pycountry is more complete)
- Numpy (Create a colorbar, numerically speaking)

# web_plot_policies.py

This code will generate a plot as the plot_policies.py, but this one will be on web. The plot is create by the Bokeh API. The plot will be based on the files created in the code prepending_policies.py, that must be in the path: ``web_plot_policies-PATH/Policies``. In this path, the IPv4 and IPv6 files must be in different folders, so, it must exist a ``web_plot_policies-PATH/Policies/IPv4`` and ``web_plot_policies-PATH/Policies/IPv6``. The files will be read from this paths.

To run this code, a Bokeh server will be needed, so the command to run this code in the terminal is:

    $ bokeh serve --show web_plot_policies.py

## Dependencies:
- Bokeh (Create the plot in the web)
- Cartopy (Geometries infos of the countries)
- Pycountry (Codes and names of the countries) (Cartopy has codes and names of the countries too, but some infos are missing, Pycountry is more complete)
- OS (To list the directories)
    
    
# Developers:

- Guilherme Silva de Castro (from march 2021 to june 2021).
    


