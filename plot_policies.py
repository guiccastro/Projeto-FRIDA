from sys import getsizeof
import matplotlib as mpl
from matplotlib import cm
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pycountry
import numpy as np

class Country:
    def __init__(self,country_obj, allocated_as, used_as, list_number_policies, list_percentage_policies):
        self.country_obj = country_obj
        self.allocated_as = allocated_as
        self.used_as = used_as
        self.number_policies = list_number_policies
        self.percentage_policies = list_percentage_policies

def GetCountryLetterCodeList(countries_list):
    result_list = []
    for country in countries_list:
        result_list.append(country.letter_code)

    return result_list

def GetCountryNameList(countries_list):
    result_list = []
    for country in countries_list:
        result_list.append(country.name)

    return result_list

def GetCountryNumberCodeList(countries_list):
    result_list = []
    for country in countries_list:
        result_list.append(country.number_code)

    return result_list

def GetAllocatedASList(countries_list):
    result_list = []
    for country in countries_list:
        result_list.append(country.allocated_as)

    return result_list

def GetUsedASList(countries_list):
    result_list = []
    for country in countries_list:
        result_list.append(country.used_as)

    return result_list

def GetNumberPolicyList(countries_list,index_policy):
    result_list = []
    for country in countries_list:
        result_list.append(country.number_policies[index_policy])

    return result_list

def GetPercentagePolicyList(countries_list,index_policy):
    result_list = []
    for country in countries_list:
        result_list.append(country.percentage_policies[index_policy])

    return result_list

def GetCountryObjectList():
    result_list = []
    for country in countries_list:
        result_list.append(country.country_obj)

    return result_list

def FindGeometry(country):

    alpha_2 = country.country_obj.alpha_2
    alpha_3 = country.country_obj.alpha_3
    numeric = country.country_obj.numeric
    name = country.country_obj.name

    try:
        official_name = country.country_obj.official_name
    except:
        official_name = ""

    for country_info in countries_info:

        atr = country_info.attributes

        if(alpha_2 == atr["ISO_A2"] or alpha_3 == atr["ISO_A3"] or numeric == atr["ISO_N3"]):
            return country_info.geometry
        elif(name == atr["ADMIN"] or name == atr["GEOUNIT"] or name == atr["SUBUNIT"] or name == atr["NAME"] or name == atr["NAME_LONG"] or name == atr["BRK_NAME"] or name == atr["FORMAL_EN"] or name == atr["NAME_CIAWF"] or name == atr["NAME_SORT"] or name == atr["NAME_EN"]):
            return country_info.geometry
        elif(official_name != ""):
            if(official_name == atr["ADMIN"] or official_name == atr["GEOUNIT"] or official_name == atr["SUBUNIT"] or official_name == atr["NAME"] or official_name == atr["NAME_LONG"] or official_name == atr["BRK_NAME"] or official_name == atr["FORMAL_EN"] or official_name == atr["NAME_CIAWF"] or official_name == atr["NAME_SORT"] or official_name == atr["NAME_EN"]):
                return country_info.geometry

    return None


def CreateUsedASPlot():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1,projection=ccrs.Robinson())

    plt.title("Number of used AS's per country.")

    ax.add_feature(cfeature.LAND, linewidth=0.4, color="#808080")
    ax.add_feature(cfeature.BORDERS,linewidth=0.4)
    ax.add_feature(cfeature.COASTLINE,linewidth=0.4)

    sm = plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(0,max_number_used_as))
    sm._A = []
    plt.colorbar(sm,ax=ax,label="Number of AS's",ticks=np.linspace(0, max_number_used_as, num=10))


    for country in countries_list:
        geometry = FindGeometry(country)

        if(geometry != None):
            color_number = country.used_as / max_number_used_as

            ax.add_geometries(geometry, ccrs.PlateCarree(),facecolor=cmap(color_number, 1),linewidth=0.4)
        else:
            error_country_geometry.append(country)

    plt.savefig("plot_used_as.pdf")



def CreateNumberPolicyPlot(policy_index):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1,projection=ccrs.Robinson())

    plt.title("Number of used AS's with policy " + str(policy_index) + " per country.")

    ax.add_feature(cfeature.LAND, linewidth=0.4, color="#808080")
    ax.add_feature(cfeature.BORDERS,linewidth=0.4)
    ax.add_feature(cfeature.COASTLINE,linewidth=0.4)

    sm = plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(0,list_max_number_policies[policy_index]))
    sm._A = []
    plt.colorbar(sm,ax=ax,label="Number of AS's",ticks=np.linspace(0, list_max_number_policies[policy_index], num=10))


    for country in countries_list:
        geometry = FindGeometry(country)

        if(geometry != None):
            color_number = country.number_policies[policy_index] / list_max_number_policies[policy_index]

            ax.add_geometries(geometry, ccrs.PlateCarree(),facecolor=cmap(color_number, 1),linewidth=0.4)
        else:
            error_country_geometry.append(country)

    plt.savefig("plot_number_policy_" + str(policy_index) + ".pdf")


def CreatePercentagePolicyPlot(policy_index):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1,projection=ccrs.Robinson())

    plt.title("Percentage of used AS's with policy " + str(policy_index) + " per country.")

    ax.add_feature(cfeature.LAND, linewidth=0.4, color="#808080")
    ax.add_feature(cfeature.BORDERS,linewidth=0.4)
    ax.add_feature(cfeature.COASTLINE,linewidth=0.4)

    sm = plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(0,100))
    sm._A = []
    plt.colorbar(sm,ax=ax,label="Percentage of AS's")


    for country in countries_list:
        geometry = FindGeometry(country)

        if(geometry != None):
            color_number = country.percentage_policies[policy_index] / 100

            ax.add_geometries(geometry, ccrs.PlateCarree(),facecolor=cmap(color_number, 1),linewidth=0.4)
        else:
            error_country_geometry.append(country)

    plt.savefig("plot_percentage_policy_" + str(policy_index) + ".pdf")



    

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

countries_list = []
error_letter_code = []
error_country_geometry = []

for line in country_lines:
    country_letter_code = line.decode("utf-8").split("|")[1]

    try:
        country_obj = pycountry.countries.get(alpha_2=country_letter_code)

        number_allocated_as = int(line.decode("utf-8").split("|")[2])
        number_used_as = int(line.decode("utf-8").split("|")[3])

        list_number_policies = []
        for i in range(0,5):
            list_number_policies.append(int(line.decode("utf-8").split("|")[i+4]))

        list_percentage_policies = [0] * 5
        if(number_used_as > 0):
            list_percentage_policies[0] = (list_number_policies[0] * 100) / number_used_as
            percentage_ref = number_used_as - list_number_policies[0]

            if(percentage_ref > 0):
                for i in range(1,5):
                    list_percentage_policies[i] = (list_number_policies[i] * 100) / percentage_ref

        if(country_obj not in GetCountryObjectList()):
            countries_list.append(Country(country_obj,number_allocated_as,number_used_as,list_number_policies,list_percentage_policies))
        else:
            index_country = GetCountryObjectList().index(country_obj)

            country = countries_list[index_country]

            country.allocated_as += number_allocated_as
            country.used_as += number_used_as

            for i in range(0,5):
                country.number_policies[i] += list_number_policies[i]

            country.percentage_policies[0] = (country.number_policies[0] * 100) / country.used_as
            percentage_ref = country.used_as - country.number_policies[0]

            if(percentage_ref > 0):
                for i in range(1,5):
                    country.percentage_policies[i] = (country.number_policies[i] * 100) / percentage_ref

    except:
        error_letter_code.append(country_letter_code)

max_number_allocated_as = max(GetAllocatedASList(countries_list))
max_number_used_as = max(GetUsedASList(countries_list))

list_max_number_policies = []
list_max_percentage_policies = []

for i in range(0,5):
    list_max_number_policies.append(max(GetNumberPolicyList(countries_list,i)))
    list_max_percentage_policies.append(max(GetPercentagePolicyList(countries_list,i)))


cmap = mpl.cm.viridis

###### NUMBER OF AS PER COUNTRY ######
#CreatePlot(1)
CreateUsedASPlot()


###### NUMBER OF POLICIES PER COUNTRY ######

### POLICY 0 ###
#CreatePlot(2)
CreateNumberPolicyPlot(0)

### POLICY 1 ###
#CreatePlot(3)
CreateNumberPolicyPlot(1)

### POLICY 2 ###
#CreatePlot(4)
CreateNumberPolicyPlot(2)

### POLICY 3 ###
#CreatePlot(5)
CreateNumberPolicyPlot(3)

### POLICY 4 ###
#CreatePlot(6)
CreateNumberPolicyPlot(4)


###### PERCENTAGE OF POLICIES PER COUNTRY ######

### POLICY 0 ###
#CreatePlot(7)
CreatePercentagePolicyPlot(0)

### POLICY 1 ###
#CreatePlot(8)
CreatePercentagePolicyPlot(1)

### POLICY 2 ###
#CreatePlot(9)
CreatePercentagePolicyPlot(2)

### POLICY 3 ###
#CreatePlot(10)
CreatePercentagePolicyPlot(3)

### POLICY 4 ###
#CreatePlot(11)
CreatePercentagePolicyPlot(4)