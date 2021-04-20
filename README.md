# downloader.py

This code will download the MRT data files from the Isolario, RouteViews or RIPE project from all of its collectors.

### Parameters:

* DATA TYPE
-t -> download only RIBs data
-T -> download only UPDATE data

* BEGIN AND END DATE
-B:year/month/day,hour:minute
-E:year/month/day,hour:minute

* FREQUENCY
-Fh:n
-Fd:n
-Fm:n

* PROJECT
-I -> download data from Isolario
-V -> download data from RouteViews
-R -> download data from RIPE

* COLLECTOR
-I:a,b,c
-V:a,b,c
-R:a,b,c

* NUMBER OF PARALLEL DOWNLOADS
-P:n

* PATH TO SAVE FILE
-S:path
