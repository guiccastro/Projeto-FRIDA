from sys import getsizeof
import matplotlib as mpl
from matplotlib import cm
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def CreatePlot(index):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1,projection=ccrs.Robinson())

    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.COASTLINE)

    sm = plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(0,max_numbers[index]))
    sm._A = []
    plt.colorbar(sm,ax=ax)

    #print("\n" + str(max_numbers[index]))

    for country in countries_info:
        country_name = country.attributes['ISO_A2']

        if(country_name in countries_dict):
            #print(country_name + " " + str(countries_dict[country_name][index]))

            #print((int(as_number)*9)/number_max_as)

            #color_number = (as_number * 0.7) / float(max_number_used_as)
            #color_number += 0.3


            color_number = countries_dict[country_name][index]/ float(max_numbers[index])

            ax.add_geometries(country.geometry, ccrs.PlateCarree(),facecolor=cmap(color_number, 1))

    plt.savefig("fig" + str(index) + ".pdf")
    #plt.show()

#apnic_countries = ["CN","KP","HK","JP","MO","MN","KR","TW","TF","AU","NZ","NF","FJ","NC","PG","SB","VU","FM","GU","KI","MH","NR","MP","PW","AS","CK","PF","NU","PN","WS","TK","TO","TV","WF","AF","BD","BT","IO","IN","MV","NP","PK","LK","BN","KH","CX","CC","ID","LA","MY","MM","PH","SG","TH","TL","VN"]
#arin_countries = ["CA","AI","AG","BS","BB","BM","KY","DM","GD","GP","JM","MQ","MS","BL","KN","LC","PM","VC","MF","TC","VG","US","PR","VI","UM","AQ","BV","HM","SH"]
#lacnic_countries = ["AR","AW","BZ","BO","BQ","BR","CL","CO","CR","CU","CW","EC","SV","GT","GY","GF","HT","HN","FK","MX","NI","PA","PY","PE","DO","BQ","BQ","MF","GS","SR","TT","UY","VE"]
#afrinic_countries = ["BI","DJ","ER","ET","KE","TZ","RW","SO","UG","BJ","BF","CV","CI","GM","GH","GN","LR","ML","NE","NG","SN","SL","TG","CM","CF","CD","GQ","GA","CG","ST","TD","DZ","EG","LY","MA","SD","SS","TN","MR","AO","BW","LS","NA","ZA","SZ","MZ","MW","ZM","ZW","MU","RE","KM","YT","MG","SC"]
#ripencc_countries = ["BH","IR","IQ","IL","JO","LB","OM","PS","QA","SA","SY","AE","YE","KZ","KG","TJ","TM","UZ","AL","AX","AD","AM","AT","AZ","BY","BE","BA","BG","HR","CY","CZ","DK","EE","FO","FI","FR","GE","DE","GI","GR","HU","IS","IE","IM","IT","LV","LI","LT","LU","MK","MT","MD","MC","ME","NL","NO","PL","PT","RO","RU","SM","RS","SK","SI","ES","SJ","SE","CH","TR","UA","GB","VA","GL"] 

policies_file = open("policies.txt","rb")
policies_lines = policies_file.readlines()
policies_file.close()

shpfilename = shpreader.natural_earth(resolution='110m',category='cultural',name='admin_0_countries')
reader = shpreader.Reader(shpfilename)
countries_info = list(reader.records())

regions_lines = policies_lines[:5]

country_lines = policies_lines[5:]

countries_dict = {}

for line in country_lines:
    country_name = line.decode("utf-8").split("|")[1]
    number_allocated_as = int(line.decode("utf-8").split("|")[2])
    number_used_as = int(line.decode("utf-8").split("|")[3])
    number_policy_0 = int(line.decode("utf-8").split("|")[4])
    number_policy_1 = int(line.decode("utf-8").split("|")[5])
    number_policy_2 = int(line.decode("utf-8").split("|")[6])
    number_policy_3 = int(line.decode("utf-8").split("|")[7])
    number_policy_4 = int(line.decode("utf-8").split("|")[8])
    if(number_used_as > 0):
        percentage_policy_0 = (number_policy_0 * 100) / number_used_as
        percentage_policy_1 = (number_policy_1 * 100) / number_used_as
        percentage_policy_2 = (number_policy_2 * 100) / number_used_as
        percentage_policy_3 = (number_policy_3 * 100) / number_used_as
        percentage_policy_4 = (number_policy_4 * 100) / number_used_as
    else:
        percentage_policy_0 = 0
        percentage_policy_1 = 0
        percentage_policy_2 = 0
        percentage_policy_3 = 0
        percentage_policy_4 = 0
    
    if(country_name not in countries_dict):
        countries_dict[country_name] = [number_allocated_as,number_used_as,number_policy_0,number_policy_1,number_policy_2,number_policy_3,number_policy_4,percentage_policy_0,percentage_policy_1,percentage_policy_2,percentage_policy_3,percentage_policy_4]
    else:
        countries_dict[country_name][0] += number_allocated_as
        countries_dict[country_name][1] += number_used_as
        countries_dict[country_name][2] += number_policy_0
        countries_dict[country_name][3] += number_policy_1
        countries_dict[country_name][4] += number_policy_2
        countries_dict[country_name][5] += number_policy_3
        countries_dict[country_name][6] += number_policy_4
        countries_dict[country_name][7] = (countries_dict[country_name][2] * 100) / countries_dict[country_name][1]
        countries_dict[country_name][8] = (countries_dict[country_name][3] * 100) / countries_dict[country_name][1]
        countries_dict[country_name][9] = (countries_dict[country_name][4] * 100) / countries_dict[country_name][1]
        countries_dict[country_name][10] = (countries_dict[country_name][5] * 100) / countries_dict[country_name][1]
        countries_dict[country_name][11] = (countries_dict[country_name][6] * 100) / countries_dict[country_name][1]

max_numbers = [0] * 12

for value in countries_dict.values():

    for i in range(0,12):
        if(value[i] > max_numbers[i]):
            max_numbers[i] = value[i]




cmap = mpl.cm.viridis

###### NUMBER OF AS PER COUNTRY ######
CreatePlot(1)


###### NUMBER OF POLICIES PER COUNTRY ######

### POLICY 0 ###
CreatePlot(2)

### POLICY 1 ###
CreatePlot(3)

### POLICY 2 ###
CreatePlot(4)

### POLICY 3 ###
CreatePlot(5)

### POLICY 4 ###
CreatePlot(6)


###### PERCENTAGE OF POLICIES PER COUNTRY ######

### POLICY 0 ###
CreatePlot(7)

### POLICY 1 ###
CreatePlot(8)

### POLICY 2 ###
CreatePlot(9)

### POLICY 3 ###
CreatePlot(10)

### POLICY 4 ###
CreatePlot(11)