import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pycountry
import numpy as np
import matplotlib as mpl
from matplotlib import cm

# Class to keep all informations about a country.
#----------------------------------------------------
# country_obj [pycountry.Country]: Referency to the Pycountry object of the country.
# allocated_as [int]: Number of allocated AS's of the country.
# used_as [int]: Number of used AS's of the country.
# list_number_policies [list(int)]: List of numbers of AS's per policies of the country.
# list_percentage_policies [list(float)]: List of percentages of AS's per policies of the country.
# The percentages of policy 0 is based on the number of used AS's.
# The percentages of policies 1 to 4 is based on the number of used AS's that are not policy 0 (used_as - list_number_policies[0]).
class Country:
    def __init__(self,country_obj, allocated_as, used_as, list_number_policies, list_percentage_policies):
        self.country_obj = country_obj
        self.allocated_as = allocated_as
        self.used_as = used_as
        self.number_policies = list_number_policies
        self.percentage_policies = list_percentage_policies


# Functions to get a list of each parameter in the list of countries.
# index_policy [int]: Number of the referenced policy.
def GetCountryObjectList():
    result_list = []
    for country in countries_list:
        result_list.append(country.country_obj)

    return result_list

def GetAllocatedASList():
    result_list = []
    for country in countries_list:
        result_list.append(country.allocated_as)

    return result_list

def GetUsedASList():
    result_list = []
    for country in countries_list:
        result_list.append(country.used_as)

    return result_list

def GetNumberPolicyList(index_policy):
    result_list = []
    for country in countries_list:
        result_list.append(country.number_policies[index_policy])

    return result_list

def GetPercentagePolicyList(index_policy):
    result_list = []
    for country in countries_list:
        result_list.append(country.percentage_policies[index_policy])

    return result_list



# Function to find the geometry of the country.
# The geometries of the countries are get from the cartopy lib.
def FindGeometry(country):

    # Get the pycountry informations of the country saved in the country_object of the Country class.
    alpha_2 = country.country_obj.alpha_2 # Two letter code.
    alpha_3 = country.country_obj.alpha_3 # Three letter code.
    numeric = country.country_obj.numeric # Three numeric code.
    name = country.country_obj.name # Name of the country.

    # Not all countries in the pycountry lib has its official name of the country.
    try:
        official_name = country.country_obj.official_name # Official name of the country.
    except: # If the country doesn't have the official name, than let it empty.
        official_name = ""

    # Iterates through all the countries in the cartopy lib.
    for country_info in countries_info:

        # Gets all the attributes from the current country.
        atr = country_info.attributes

        # Verifies if the two types of letter codes or the numeric code matches.
        if(alpha_2 == atr["ISO_A2"] or alpha_3 == atr["ISO_A3"] or numeric == atr["ISO_N3"]):
            return country_info.geometry

        # Verifies if the name matches.
        # Here there are nine verifications.
        # All these verificantions is because the name and official name from 
        # the pycountry lib can differ a little bit from the ones from the cartopy lib. 
        # So, more parameters are tested so that there are more matches.
        elif(name == atr["ADMIN"] or name == atr["GEOUNIT"] or name == atr["SUBUNIT"] or name == atr["NAME"] or name == atr["NAME_LONG"] or name == atr["BRK_NAME"] or name == atr["FORMAL_EN"] or name == atr["NAME_CIAWF"] or name == atr["NAME_SORT"] or name == atr["NAME_EN"]):
            return country_info.geometry

        # Verifies if the official name matches.
        # The same verifications of from the name test.
        elif(official_name != ""):
            if(official_name == atr["ADMIN"] or official_name == atr["GEOUNIT"] or official_name == atr["SUBUNIT"] or official_name == atr["NAME"] or official_name == atr["NAME_LONG"] or official_name == atr["BRK_NAME"] or official_name == atr["FORMAL_EN"] or official_name == atr["NAME_CIAWF"] or official_name == atr["NAME_SORT"] or official_name == atr["NAME_EN"]):
                return country_info.geometry

    return None


# Create the pdf file from the used AS's plot.
def CreateUsedASPlot():

    # Create the figure.
    fig = plt.figure()

    # Add the Robinson projection to the figure.
    ax = fig.add_subplot(1, 1, 1,projection=ccrs.Robinson())

    # Add a title.
    plt.title("Number of used AS's per country.")

    # Add some details to the map.
    # LAND: change the color of all the countrys to gray.
    ax.add_feature(cfeature.LAND, linewidth=0.4, color="#808080")

    # Create the legend of the colorbar.
    sm = plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(0,max_number_used_as))
    sm._A = []
    plt.colorbar(sm,ax=ax,label="Number of AS's",ticks=np.linspace(0, max_number_used_as, num=10)) # Create 10 ticks between 0 and the max number of used AS's.

    # Iterates through the countries list.
    for country in countries_list:

        # Find the geometry of the current country.
        geometry = FindGeometry(country)

        # If the geometry was found.
        if(geometry != None):
            
            # Defines the color of the country based on its value and the max value.
            color_number = country.used_as / max_number_used_as

            # Add the color geometry of the country.
            ax.add_geometries(geometry, ccrs.PlateCarree(),facecolor=cmap(color_number, 1))
        else:
            # If the geometry was not found, adds the country to a list of error.
            error_country_geometry.append(country)

    # Add some details to the map.
    # This details are added after the countries are painted for the lines to be on top and be very visible.
    # BORDERS: Countries's division lines.
    # COASTLINE: Countries's coastlines lines.
    ax.add_feature(cfeature.BORDERS,linewidth=0.1)
    ax.add_feature(cfeature.COASTLINE,linewidth=0.1)

    # Create the file.
    plt.savefig("plot_used_as.pdf")


# Create the pdf file from the number of AS's with each policies plot.
def CreateNumberPolicyPlot(policy_index):

    # Create the figure.
    fig = plt.figure()

    # Add the Robinson projection to the figure.
    ax = fig.add_subplot(1, 1, 1,projection=ccrs.Robinson())

    # Add a title.
    plt.title("Number of used AS's with policy " + str(policy_index) + " per country.")

    # Add some details to the map.
    # LAND: change the color of all the countrys to gray.
    ax.add_feature(cfeature.LAND, linewidth=0.4, color="#808080")

    # Create the legend of the colorbar.
    sm = plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(0,list_max_number_policies[policy_index]))
    sm._A = []
    plt.colorbar(sm,ax=ax,label="Number of AS's",ticks=np.linspace(0, list_max_number_policies[policy_index], num=10)) # Create 10 ticks between 0 and the max number of AS's per policy.

    # Iterates through the countries list.
    for country in countries_list:

        # Find the geometry of the current country.
        geometry = FindGeometry(country)

        # If the geometry was found.
        if(geometry != None):

            # Defines the color of the country based on its value and the max value.
            color_number = country.number_policies[policy_index] / list_max_number_policies[policy_index]

            # Add the color geometry of the country.
            ax.add_geometries(geometry, ccrs.PlateCarree(),facecolor=cmap(color_number, 1),linewidth=0.4)
        else:
            # If the geometry was not found, adds the country to a list of error.
            error_country_geometry.append(country)

    # Add some details to the map.
    # This details are added after the countries are painted for the lines to be on top and be very visible.
    # BORDERS: Countries's division lines.
    # COASTLINE: Countries's coastlines lines.
    ax.add_feature(cfeature.BORDERS,linewidth=0.1)
    ax.add_feature(cfeature.COASTLINE,linewidth=0.1)

    # Create the file.
    plt.savefig("plot_number_policy_" + str(policy_index) + ".pdf")


# Create the pdf file from the percentage of AS's with each policies plot.
def CreatePercentagePolicyPlot(policy_index):

    # Create the figure.
    fig = plt.figure()

    # Add the Robinson projection to the figure.
    ax = fig.add_subplot(1, 1, 1,projection=ccrs.Robinson())

    # Add a title.
    plt.title("Percentage of used AS's with policy " + str(policy_index) + " per country.")

    # Add some details to the map.
    # LAND: change the color of all the countrys to gray.
    ax.add_feature(cfeature.LAND, linewidth=0.4, color="#808080")

    # Create the legend of the colorbar.
    sm = plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(0,100))
    sm._A = []
    plt.colorbar(sm,ax=ax,label="Percentage of AS's")

    # Iterates through the countries list.
    for country in countries_list:

        # Find the geometry of the current country.
        geometry = FindGeometry(country)

        # If the geometry was found.
        if(geometry != None):

            # Defines the color of the country based on its value and the max value.
            color_number = country.percentage_policies[policy_index] / 100

            # Add the color geometry of the country.
            ax.add_geometries(geometry, ccrs.PlateCarree(),facecolor=cmap(color_number, 1),linewidth=0.4) # Create 10 ticks between 0 and 100, the max number is always 100 because the percentage its based on that.
        else:
            # If the geometry was not found, adds the country to a list of error.
            error_country_geometry.append(country)

    # Add some details to the map.
    # This details are added after the countries are painted for the lines to be on top and be very visible.
    # BORDERS: Countries's division lines.
    # COASTLINE: Countries's coastlines lines.
    ax.add_feature(cfeature.BORDERS,linewidth=0.1)
    ax.add_feature(cfeature.COASTLINE,linewidth=0.1)

    # Create the file.
    plt.savefig("plot_percentage_policy_" + str(policy_index) + ".pdf")



    
# NOT USED - Countries's letter codes from each region.
#apnic_countries = ["CN","KP","HK","JP","MO","MN","KR","TW","TF","AU","NZ","NF","FJ","NC","PG","SB","VU","FM","GU","KI","MH","NR","MP","PW","AS","CK","PF","NU","PN","WS","TK","TO","TV","WF","AF","BD","BT","IO","IN","MV","NP","PK","LK","BN","KH","CX","CC","ID","LA","MY","MM","PH","SG","TH","TL","VN"]
#arin_countries = ["CA","AI","AG","BS","BB","BM","KY","DM","GD","GP","JM","MQ","MS","BL","KN","LC","PM","VC","MF","TC","VG","US","PR","VI","UM","AQ","BV","HM","SH"]
#lacnic_countries = ["AR","AW","BZ","BO","BQ","BR","CL","CO","CR","CU","CW","EC","SV","GT","GY","GF","HT","HN","FK","MX","NI","PA","PY","PE","DO","BQ","BQ","MF","GS","SR","TT","UY","VE"]
#afrinic_countries = ["BI","DJ","ER","ET","KE","TZ","RW","SO","UG","BJ","BF","CV","CI","GM","GH","GN","LR","ML","NE","NG","SN","SL","TG","CM","CF","CD","GQ","GA","CG","ST","TD","DZ","EG","LY","MA","SD","SS","TN","MR","AO","BW","LS","NA","ZA","SZ","MZ","MW","ZM","ZW","MU","RE","KM","YT","MG","SC"]
#ripencc_countries = ["BH","IR","IQ","IL","JO","LB","OM","PS","QA","SA","SY","AE","YE","KZ","KG","TJ","TM","UZ","AL","AX","AD","AM","AT","AZ","BY","BE","BA","BG","HR","CY","CZ","DK","EE","FO","FI","FR","GE","DE","GI","GR","HU","IS","IE","IM","IT","LV","LI","LT","LU","MK","MT","MD","MC","ME","NL","NO","PL","PT","RO","RU","SM","RS","SK","SI","ES","SJ","SE","CH","TR","UA","GB","VA","GL"] 

# Open the file with the policies.
policies_file = open("policies.txt","rb")

# Read the lines from the file.
policies_lines = policies_file.readlines()

# Close the file.
policies_file.close()

# Download the infos from the countries from the cartopy lib.
shpfilename = shpreader.natural_earth(resolution='110m',category='cultural',name='admin_0_countries')

# Read the infos.
reader = shpreader.Reader(shpfilename)
countries_info = list(reader.records())

# Separates the region lines and the country lines.
regions_lines = policies_lines[:5]
country_lines = policies_lines[5:]

# Initizalize some lists.
# To keep the countris from policies's file.
countries_list = []
# To keep countries with letter codes errors.
error_letter_code = []
# To keep countries with geometry errors.
error_country_geometry = []

# Iterates through the countries's lines.
for line in country_lines:

    # Get the country's letter code from the line.
    country_letter_code = line.decode("utf-8").split("|")[1]

    # Try to get other informations.
    # It's possible that not all letter codes exists in the pycountry lib,
    # if not exists it will generate an error. This try is to prevent the code
    # to stop on this errors.
    try:

        # Get the pycountry object based on the letter code.
        country_obj = pycountry.countries.get(alpha_2=country_letter_code)

        # Get the number of allocated AS's from the line.
        number_allocated_as = int(line.decode("utf-8").split("|")[2])

        # Get the number of used AS's from the line.
        number_used_as = int(line.decode("utf-8").split("|")[3])

        # Initializes the list to keep the number of used policys.
        list_number_policies = []

        # For each policy (0 to 4).
        for i in range(0,5):
            # Get the number of AS's with the current policy from the line.
            list_number_policies.append(int(line.decode("utf-8").split("|")[i+4]))

        # Initializes the list to keep the number of used policys.
        # To prevent the code to do some divisions by zero, we already initialize the list with some values.
        list_percentage_policies = [0] * 5

        # Verifys if the number of used AS's is bigger than zero.
        # Otherwise, a division by zero would occur.
        if(number_used_as > 0):

            # Get the percentage of the policy 0 first, because the max number its diferent from the other policies.
            # The percentages of policy 0 is based on the number of used AS's.
            list_percentage_policies[0] = (list_number_policies[0] * 100) / number_used_as

            # The percentages of policies 1 to 4 is based on the number of used AS's that are not policy 0 (used_as - list_number_policies[0]).
            percentage_ref = number_used_as - list_number_policies[0]

            # Verifys if the percentage reference of AS's with policies 1 to 4 is bigger than zero.
            # Otherwise, a division by zero would occur.
            if(percentage_ref > 0):

                # For each policy (1 to 4).
                for i in range(1,5):

                    # Get the percentage of the current policy.
                    list_percentage_policies[i] = (list_number_policies[i] * 100) / percentage_ref

        # If the country was not already in the list...
        if(country_obj not in GetCountryObjectList()):

            # Create a new object Country with the infos and add the country to the list.
            countries_list.append(Country(country_obj,number_allocated_as,number_used_as,list_number_policies,list_percentage_policies))

        # If the country is already in the list, than update the values.
        # This is to sum all the informations from each country in one object.
        else:

            # Get the index of the current country from the list of countries.
            # The search is based on a list of country objects.
            index_country = GetCountryObjectList().index(country_obj)

            # Get the country from the list.
            country = countries_list[index_country]

            # Update the number of allocated AS's.
            country.allocated_as += number_allocated_as

            # Update the number of used AS's.
            country.used_as += number_used_as

            # Update the number of AS's with each policy.
            for i in range(0,5):
                country.number_policies[i] += list_number_policies[i]

            # Verifys if the number of used AS's is bigger than zero.
            # Otherwise, a division by zero would occur.
            if(country.used_as > 0):

                # Update the percentage of AS's with policy 0.
                country.percentage_policies[0] = (country.number_policies[0] * 100) / country.used_as

                # Update the percentage reference.
                percentage_ref = country.used_as - country.number_policies[0]

                # Verifys if the percentage reference of AS's with policies 1 to 4 is bigger than zero.
                # Otherwise, a division by zero would occur.
                if(percentage_ref > 0):

                    # Update the percentage of AS's with policy 1 to 4.
                    for i in range(1,5):
                        country.percentage_policies[i] = (country.number_policies[i] * 100) / percentage_ref

    except: # If an error occur...

        # Add the letter code of the country that generate an error to the list.
        error_letter_code.append(country_letter_code)

# Calculates the max value for all the allocated AS's.
max_number_allocated_as = max(GetAllocatedASList())

# Calculates the max value for all the used AS's.
max_number_used_as = max(GetUsedASList())

# Initilizes the lists for the max number and percentages for each policy.
list_max_number_policies = []
list_max_percentage_policies = []

# For each policy (0 to 4).
for i in range(0,5):

    # Calculates the max value for all the numbers of the current policy.
    list_max_number_policies.append(max(GetNumberPolicyList(i)))

    # Calculates the max value for all the percentages of the current policy.
    list_max_percentage_policies.append(max(GetPercentagePolicyList(i)))

# Creates the colormap that will be used to paint the countries in the plots.
# The colormap Viridis was chosen based that the minimum values will not be white 
# and the color differences from each country can be easily seen.
cmap = mpl.cm.viridis


###### CREATE THE PLOTS ######

###### NUMBER OF AS'S PER COUNTRY ######
CreateUsedASPlot()

###### NUMBER OF POLICIES PER COUNTRY ######

### POLICY 0 ###
CreateNumberPolicyPlot(0)

### POLICY 1 ###
CreateNumberPolicyPlot(1)

### POLICY 2 ###
CreateNumberPolicyPlot(2)

### POLICY 3 ###
CreateNumberPolicyPlot(3)

### POLICY 4 ###
CreateNumberPolicyPlot(4)


###### PERCENTAGE OF POLICIES PER COUNTRY ######

### POLICY 0 ###
CreatePercentagePolicyPlot(0)

### POLICY 1 ###
CreatePercentagePolicyPlot(1)

### POLICY 2 ###
CreatePercentagePolicyPlot(2)

### POLICY 3 ###
#CreatePlot(10)
CreatePercentagePolicyPlot(3)

### POLICY 4 ###
CreatePercentagePolicyPlot(4)