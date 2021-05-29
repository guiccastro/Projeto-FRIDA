# @Code created by Guilherme Silva de Castro on april 2021 and last updated on may 2021.@

#####################################################################
# This file will read some files that contain infos about the prepending policies by prefix and AS's numbers, 
# and some files that contain infos about the allocated AS's numbers per country. The idea is to create a new file
# with infos about the number of used prepending policies by countries and regions.
# The final files will be saved in the path "Policies/IPv4 OR IPv6", so, the final files from IPv4 and IPv6 stay in 
# different directories. The name of the final file has the pattern "Policie-DATE".

###############################################################
# TO DO AND IDEAS:
# [ ] - Improve this code to automatically download the files in a better way.


import gzip
import bz2

# Function to create a dictionary from each region file.
# ---------------------------------------------
# region_lines [list(string)]: List with the lines of the file of the specified region.
def CreateRegionDictionary(region_lines):
    
    # Initialize the final dictionary.
    final_dict = {}

    # Iterates through all the lines of the region lines...
    for line in region_lines:

        # Get a list with the infos that are separeted by the character '|'.
        line = line.decode("utf-8")[:-1].split("|")

        # If the line contain info about the AS numbers and the AS number hasn't a dot (it's numeric)...
        if(line[2] == "asn" and line[3].isnumeric()):

            # Get the country of the line.
            country = line[1]

            # Get the AS number of the line.
            as_number = line[3]

            # Get the count of the AS number of the line.
            as_count = line[4]

            # Verifies if the country is already in the dictionary.
            if(country in final_dict):

                # Generate the AS numbers based on the first number 'as_number' and its counter 'as_count'.
                for _ in range(0,int(as_count)):

                    # Verifies if the AS number isn't already in the list of the current country.
                    if(as_number not in final_dict[country]):

                        # Add the AS number to the list of the current country.
                        final_dict[country].append(as_number)

                    # Get the next AS number.
                    as_number = str(int(as_number) + 1)
            else:

                # Initialize the list of the AS numbers.
                list_as = []

                # Generate the AS numbers based on the first number 'as_number' and its counter 'as_count'.
                for _ in range(0,int(as_count)):

                    # Add the current AS number to the list.
                    list_as.append(as_number)

                    # Get the next AS number.
                    as_number = str(int(as_number) + 1)

                # Add the country to the dictionary and its list of AS numbers.
                final_dict[country] = list_as

    # Return the final dictionary.
    return final_dict


# Function to instantiate the country and region infos lists.
def CreateCountryInfoList(region_as_dict,region_string):

    # Initializes the number of allocated AS's for the current region.
    region_aloccated_as = 0

    # Initializes the number of used AS's for the current region.
    region_used_as = 0

    # Initializes the number of AS's with each policy for the current region.
    region_policies = [0,0,0,0,0]

    # Iterates through each item of the dictonary of the current region.
    for item in region_as_dict.items():

        # Get the country letter code.
        country = item[0]

        # Get how many AS's was aloccated for the current country.
        aloccated_as = len(item[1])

        # Initializes the number of used AS's for the current country.
        used_as = 0

        # Initializes the number of AS's with each policy for the current country.
        policies = [0,0,0,0,0]

        # Iterates through each AS number of the current country.
        for as_number in item[1]:

            # Verifies if the current AS number is in the AS policies dictionary.
            if(as_number in as_policies_dict):

                # If the AS numbes is in the dictionary, it means the AS number is actually used, and not just allocated.
                # Increase the number of used AS's.
                used_as += 1

                # Verifies how many policies the country uses.
                if(len(as_policies_dict[as_number]) > 1):

                    # If it's more than one policy, than the policy of the country is mixed (policy 4).
                    # Increase the number of policies 4.
                    policies[4] += 1

                else:

                    # If it's one policy, thant the policy number that must be increased is the policy number used for the country.
                    # There's no way to a country appear in the dictionary with no policy, so it's not necessary to check that.
                    policies[int(as_policies_dict[as_number][0])] += 1

        # Update the region variables.
        region_aloccated_as += aloccated_as
        region_used_as += used_as

        # For each policy (0 to 4), update its information.
        for i in range(0,5):
            region_policies[i] += policies[i]

        # Create the string with the line info of the current country.
        # Pattern:
        # region|country|aloccated AS's|used AS's|policy 0|policy 1|policy 2|policy 3|policy 4
        line = region_string + "|" + country + "|" + str(aloccated_as) + "|" + str(used_as) + "|" + str(policies[0]) + "|" + str(policies[1]) + "|" + str(policies[2]) + "|" + str(policies[3]) + "|" + str(policies[4]) + "\n"
        
        # Add the line to the list of the countries infos.
        country_info_lines.append(line)

    # Create the string with the line info of the current country.
    # Pattern:
    # region|aloccated AS's|used AS's|policy 0|policy 1|policy 2|policy 3|policy 4
    region_line = region_string + "|" + str(region_aloccated_as) + "|" + str(region_used_as) + "|" + str(region_policies[0]) + "|" + str(region_policies[1]) + "|" + str(region_policies[2]) + "|" + str(region_policies[3]) + "|" + str(region_policies[4]) + "\n"
    
    # Add the line to the list of the regions infos.
    region_info_lines.append(region_line)


# Open the file with the policies info per prefix.
#prepending_policies_file = gzip.open("v4_sane_policies_20111115.gz", "rb")
prepending_policies_file = gzip.open("v4_sane_policies_20200330.gz", "rb")

# Read the lines of the file.
# Don't read the first line because it has no information.
prepending_policies_lines = prepending_policies_file.readlines()[1:]

# Close the file.
prepending_policies_file.close()

# Create a dictionary to keep the policies based on the AS number.
# Pattern:
# AS number : list of policys
# Example:
# "20450" : ["0", "2"]
as_policies_dict = {}

# Iterates through each line of the file.
for line in prepending_policies_lines:

    # Get a list with the infos that are separeted by the character '|'.
    line = line.decode("utf-8")[:-1].split("|")

    # Get the IP.
    ip = line[0]

    # Get the AS number.
    as_number = line[1]

    # Get the number of monitors.
    num_monitor = line[2]

    # Get the list of observed prepends.
    observed_prepends = line[3].split(";")

    # Get the policy.
    policy = line[4]
    
    # Verifies if the AS numbes is already in the dictionary.
    if(as_number in as_policies_dict):

        # Verifies if the policy isn't already in the list of the AS number.
        if(policy not in as_policies_dict[as_number]):
            
            # Add the policy to the AS number.
            as_policies_dict[as_number].append(policy)
    else:

        # Add the AS number to the dictionary with the used policy.
        as_policies_dict[as_number] = [policy]


# Verify each region file to find the AS numberer that are allocated an get its information.

###### APNIC ######

# Open the APNIC file.
#apnic_file = gzip.open("delegated-apnic-20111115.gz", "rb")
apnic_file = gzip.open("delegated-apnic-20200330.gz", "rb")

# Read the lines of the file, starting at the line 32 because 
# of the commentaries ans some other useless infos in the file.
apnic_lines = apnic_file.readlines()[31:]

# Close the file.
apnic_file.close()

# Create a dictionary to keep the AS numbers based on the country.
# Pattern:
# country : list of AS
# Example:
# "JP" : [173,174,1250]
apnic_country_as_dict = CreateRegionDictionary(apnic_lines)


###### ARIN ######

# Open the ARIN file.
#arin_file = open("delegated-arin-20111115", "rb")
arin_file = open("delegated-arin-extended-20200330", "rb")

# Read the lines of the file, starting at the line 5 because 
# of the commentaries ans some other useless infos in the file.
arin_lines = arin_file.readlines()[4:]

# Close the file.
arin_file.close()

# Create a dictionary to keep the AS numbers based on the country.
# Pattern:
# country : list of AS
# Example:
# "US" : [173,174,1250]
arin_country_as_dict = CreateRegionDictionary(arin_lines)


###### LACNIC ######

# Open the LACNIC file.
#lacnic_file = open("delegated-lacnic-20111115", "rb")
lacnic_file = open("delegated-lacnic-20200330", "rb")

# Read the lines of the file, starting at the line 5 because 
# of the commentaries ans some other useless infos in the file.
lacnic_lines = lacnic_file.readlines()[4:]

# Close the file.
lacnic_file.close()

# Create a dictionary to keep the AS numbers based on the country.
# Pattern:
# country : list of AS
# Example:
# "US" : [173,174,1250]
lacnic_country_as_dict = CreateRegionDictionary(lacnic_lines)


###### AFRINIC ######

# Open the AFRINIC file.
#afrinic_file = open("delegated-afrinic-20111115", "rb")
afrinic_file = open("delegated-afrinic-20200330", "rb")

# Read the lines of the file, starting at the line 5 because 
# of the commentaries ans some other useless infos in the file.
afrinic_lines = afrinic_file.readlines()[4:]

# Close the file.
afrinic_file.close()

# Create a dictionary to keep the AS numbers based on the country.
# Pattern:
# country : list of AS
# Example:
# "ZA" : [173,174,1250]
afrinic_country_as_dict = CreateRegionDictionary(afrinic_lines)


###### RIPENCC ######

# Open the RIPENCC file.
#ripencc_file = bz2.open("delegated-ripencc-20111115.bz2", "rb")
ripencc_file = bz2.open("delegated-ripencc-20200330.bz2", "rb")

# Read the lines of the file, starting at the line 5 because 
# of the commentaries ans some other useless infos in the file.
ripencc_lines = ripencc_file.readlines()[4:]

# Close the file.
ripencc_file.close()

# Create a dictionary to keep the AS numbers based on the country.
# Pattern:
# country : list of AS
# Example:
# "FR" : [173,174,1250]
ripencc_country_as_dict = CreateRegionDictionary(ripencc_lines)


###### GENERATE THE INFO ######

country_info_lines = []
region_info_lines = []

###### APNIC ######
CreateCountryInfoList(apnic_country_as_dict,"apnic")

###### ARIN ######
CreateCountryInfoList(arin_country_as_dict,"arin")

###### LACNIC ######
CreateCountryInfoList(lacnic_country_as_dict,"lacnic")

###### AFRINIC ######
CreateCountryInfoList(afrinic_country_as_dict,"afrinic")

###### RIPENCC ######
CreateCountryInfoList(ripencc_country_as_dict,"ripencc")


# Create the file to save the final infos.
# File lines pattern:
# region1
# region2
# region3
# region4
# region5
# country1
# country2
# country3
# country4
#   .
#   .
#   .
# countryN
final_file = open("policies.txt","w")

# Write the regions infos.
final_file.writelines(region_info_lines)

# Write the countris infos.
final_file.writelines(country_info_lines)

# Close the file.
final_file.close()