# downloader.py

This code can download the MRT data files from the Isolario, RouteViews or RIPE project from all of its collectors.

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
  
In this example, you will download only RIB files from the project RouteViews of its collector São Paulo. The files will be downloaded from the first day of April of 2021 until the second day of April of 2021, in every 3 hours. The code will download three files in the same time.

    $ python3 downloader.py -t -T -B:2021/04/01,00:00 -E:2021/04/02,20:00 -Fh:2 -I -P:3
    
If you want to try a longer test, you can use the above example. Here you will download the RIB and UPDATE files from the same date from the previous example, but you will download from all the collectors from project Isolario. The frequency of download will be in every 2 hours, which will increase the number of downloaded files. Feel free to modify the paramenters and make some tests.

# sanitizer.py

This code will read the data from the MRT files, remove the ones with prefixes and routes invalids and create a new file with the sanitized data.

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


# web_plot_policies.py

This code will generate a plot in the web. The plot is create by the Bokeh API. The plot will be based on the files created in the code prepending_policies.py, that must be in the path: "web_plot_policies-PATH/Policies". In this path, the IPv4 and IPv6 files must be in different folders, so, it must exist a "web_plot_policies-PATH/Policies/IPv4" and "web_plot_policies-PATH/Policies/IPv6". The files will be read from this paths.

To run this code, a Bokeh server will be needed, so the command to run this code in the terminal is:

    $ bokeh serve --show web_plot_policies.py
    


