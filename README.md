# downloader.py

This code will download the MRT data files from the Isolario, RouteViews or RIPE project from all of its collectors.

## Parameters:

### __Data type__:
``-t`` => Download RIBs data.

``-T`` => Download UPDATE data.

### __Begin and end date__:
``-B:year/month/day,hour:minute`` => The first data to be downloaded

``-E:year/month/day,hour:minute`` => The last data to be downloaded

### __Frequency__:
``-Fh:n`` => Download the data every ``n`` hours between the begin and end date.

``-Fd:n`` => Download the data every ``n`` days between the begin and end date.

### __Project__:
``-I`` => Download data from the project Isolario.

``-V`` => Download data from the project RouteViews.

``-R`` => Download data from the project RIPE.

### __Collector__:
``-I:a,b,c,...`` => Download the data from collectors ``a``, ``b``, ``c``, ..., from project Isolario.

``-V:a,b,c,...`` => Download the data from collectors ``a``, ``b``, ``c``, ..., from project RouteViews.

``-R:a,b,c,...`` => Download the data from collectors ``a``, ``b``, ``c``, ..., from project RIPE.

### __Number of parallel downloads__:
``-P:n`` => Download ``n`` parallel files from each project.

### __Path to save file__:
``-S:path`` => Save the downloaded files in ``path``.

## Example:
    $ python3 downloader.py -t -B:2021/04/01,00:00 -E:2021/04/02,20:00 -Fh:3 -V:saopaulo -P:3
  
In this example, you will download only RIB files from the project RouteViews of its collector São Paulo. The files will be downloaded from the first day of April of 2021 until the second day of April of 2021, in every 3 hours. The code will download three files in the same time.

