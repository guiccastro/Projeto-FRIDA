### (*)DATA TYPE(*) ### 
# -u -> download only RIBs data
# -U -> download only UPDATE data

### (*)BEGIN AND END DATE(*) ###
# -b[year.month.day.hour.minute] (Begin)
# -e[year.month.day.hour.minute] (End)
# or
# -B:year/month/day:hour.minute
# -E:year/month/day:hour.minute

### FREQUENCY ###
# -fh[n] -> every n hours per day (Frequency in hours)
# -fd[n] -> every n days per month (Frequency in days)
# -fm[n] -> every n months per year (Frequency in months)
# or 
# -Fh:n
# -Fd:n
# -Fm:n

### PROJECT ###
# -I -> download data from Isolario
# -V -> download data from RouteViews
# -R -> download data from RIPE

### COLECTOR ###
# -I:a;b;c
# -V:a;b;c
# -R:a;b;c

### NUMBER OF PARALLEL DOWNLOADS ###
# -n
# or
# -P:n

### PATH TO SAVE FILE ###
# -S:path


import wget
import sys
import os

def VerifyArg(arg):
    if(arg[0] == "[" and arg[-1] == "]"):
        return True
    else:
        return False           

def getParameters(parameters):
    p = [0] * 15
    begin = [0,0,0,0,0]
    end = [0,0,0,0,0]
    frequency = [0,0,0]
    project = ""
    collector = ""
    for parameter in list(parameters):
        if(parameter[0] == "-"):
            if(parameter[1] == "b"):
                arg = parameter[2:]
                if(VerifyArg(arg)):
                    arg = arg[1:-1]
                    arg = arg.split(".")
                    if(len(arg) == 5):
                        p[0] = int(arg[0])
                        p[1] = int(arg[1])
                        p[2] = int(arg[2])
                        p[3] = int(arg[3])
                        p[4] = int(arg[4])
                    else:
                        print("ERROR: Some argument of the begin parameter is missing.")
                else:
                    print("ERROR: Parameter without '[' or ']'.")
            if(parameter[1] == "e"):
                arg = parameter[2:]
                if(VerifyArg(arg)):
                    arg = arg[1:-1]
                    arg = arg.split(".")
                    if(len(arg) == 5):
                        p[5] = int(arg[0])
                        p[6] = int(arg[1])
                        p[7] = int(arg[2])
                        p[8] = int(arg[3])
                        p[9] = int(arg[4])
                    else:
                        print("ERROR: Some argument of the end parameter is missing.")
                else:
                    print("ERROR: Parameter without '[' or ']'.")
            if(parameter[1] == "f"):
                if(parameter[2] == "h"):
                    arg = parameter[3:]
                    if(VerifyArg(arg)):
                        arg = arg[1:-1]
                        p[10] = int(arg[0])
                    else:
                        print("ERROR: Parameter without '[' or ']'.")
                if(parameter[2] == "d"):
                    arg = parameter[3:]
                    if(VerifyArg(arg)):
                        arg = arg[1:-1]
                        p[11] = int(arg[0])
                    else:
                        print("ERROR: Parameter without '[' or ']'.")
                if(parameter[2] == "m"):
                    arg = parameter[3:]
                    if(VerifyArg(arg)):
                        arg = arg[1:-1]
                        p[12] = int(arg[0])
                    else:
                        print("ERROR: Parameter without '[' or ']'.")
            if(parameter[1] == "p"):
                arg = parameter[2:]
                if(VerifyArg(arg)):
                    p[13] = arg[1:-1] 
                else:
                    print("ERROR: Parameter without '[' or ']'.")
            if(parameter[1] == "c"):
                arg = parameter[2:]
                if(VerifyArg(arg)):
                    p[14] = arg[1:-1] 
                else:
                    print("ERROR: Parameter without '[' or ']'.")

            if(parameter[1] == "I"):

        else:
            print("ERROR: Parameter without '-'.")

    return p

#url = "http://archive.routeviews.org/route-views.saopaulo/bgpdata/2021.03/RIBS/rib.20210301.0200.bz2"
url = "https://image.shutterstock.com/image-illustration/space-background-nebula-stars-environment-260nw-1401778256.jpg"
wget.download(url, out='Dados/Name')

begin = [0,0,0,0,0]
end = [0,0,0,0,0]
frequency = [0,0,0]
project = ""
collector = ""


parameters = sys.argv[1:]

p = getParameters(parameters)
begin = p[0:5]
end = p[5:10]
frequency = p[10:13]
project = p[13]
collector = p[14]

print("Begin: " + str(begin))
print("End: " + str(end))
print("Frequency: " + str(frequency))
print("Project: " + str(project))
print("Collector: " + str(collector))







