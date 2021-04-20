# downloader.py

This code will download the MRT data files from the Isolario, RouteViews or RIPE project from all of its collectors.

## Parameters:

### __Data type__:

``-t`` -> download only RIBs data

``-T`` -> download only UPDATE data

### __Begin and end date__:

``-B:year/month/day,hour:minute``

``-E:year/month/day,hour:minute``

### __Frequency__:

``-Fh:n``

``-Fd:n``

``-Fm:n``

### __Project__:

``-I`` -> download data from Isolario

``-V`` -> download data from RouteViews

``-R`` -> download data from RIPE

### __Collector__:

``-I:a,b,c``

``-V:a,b,c``

``-R:a,b,c``

### __Number of parallel downloads__:

``-P:n``

### __Path to save file__:

``-S:path``
