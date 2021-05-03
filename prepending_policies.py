import gzip
import bz2
from sys import getsizeof

prepending_policies_file = gzip.open("v4_sane_policies_20111115.gz", "rb")
prepending_policies_lines = prepending_policies_file.readlines()[1:]
prepending_policies_file.close()

# as_policies_dict pattern
# AS number : list of politics
# "20450" : ["0", "2"]
as_policies_dict = {}

for line in prepending_policies_lines:
    line = line.decode("utf-8")[:-1].split("|")

    ip = line[0]
    as_number = line[1]
    num_monitor = line[2]
    observed_prepends = line[3]
    policy = line[4]
    

    if(as_number in as_policies_dict):
        if(policy not in as_policies_dict[as_number]):
            as_policies_dict[as_number].append(policy)
    else:
        as_policies_dict.update({as_number: [policy]})


###### APNIC ######

apnic_file = gzip.open("delegated-apnic-20111115.gz", "rb")
apnic_lines = apnic_file.readlines()[31:]
apnic_file.close()

# apnic_country_as_dict pattern
# country : list of AS
# "JP" : [173,174,1250]
apnic_country_as_dict = {}

done = False
line_index = 0

while(not done):
    line = apnic_lines[line_index].decode("utf-8")[:-1].split("|")

    if(line[2] == "asn"):

        country = line[1]
        as_number = line[3]
        as_count = line[4]

        if(country in apnic_country_as_dict):
            for _ in range(0,int(as_count)):
                if(as_number not in apnic_country_as_dict[country]):
                    apnic_country_as_dict[country].append(as_number)
                as_number = str(int(as_number) + 1)
        else:
            list_as = []
            for _ in range(0,int(as_count)):
                list_as.append(as_number)
                as_number = str(int(as_number) + 1)

            apnic_country_as_dict.update({country: list_as})
        
        line_index += 1
    else:
        done = True


###### ARIN ######

arin_file = open("delegated-arin-20111115", "rb")
arin_lines = arin_file.readlines()[4:]
arin_file.close()

# arin_country_as_dict pattern
# country : list of AS
# "US" : [173,174,1250]
arin_country_as_dict = {}

done = False
line_index = 0

while(not done):
    line = arin_lines[line_index].decode("utf-8")[:-1].split("|")

    if(line[2] == "asn"):

        country = line[1]
        as_number = line[3]
        as_count = line[4]

        if(country in arin_country_as_dict):
            for _ in range(0,int(as_count)):
                if(as_number not in arin_country_as_dict[country]):
                    arin_country_as_dict[country].append(as_number)
                as_number = str(int(as_number) + 1)
        else:
            list_as = []
            for _ in range(0,int(as_count)):
                list_as.append(as_number)
                as_number = str(int(as_number) + 1)

            arin_country_as_dict.update({country: list_as})
        
        line_index += 1
    else:
        done = True



###### LACNIC ######

lacnic_file = open("delegated-lacnic-20111115", "rb")
lacnic_lines = lacnic_file.readlines()[4:]
lacnic_file.close()

# lacnic_country_as_dict pattern
# country : list of AS
# "US" : [173,174,1250]
lacnic_country_as_dict = {}

done = False
#line_index = 0

#while(not done):

for line in lacnic_lines:
    line = line.decode("utf-8")[:-1].split("|")

    if(line[2] == "asn"):

        country = line[1]
        as_number = line[3]
        as_count = line[4]

        if(country in lacnic_country_as_dict):
            for _ in range(0,int(as_count)):
                if(as_number not in lacnic_country_as_dict[country]):
                    lacnic_country_as_dict[country].append(as_number)
                as_number = str(int(as_number) + 1)
        else:
            list_as = []
            for _ in range(0,int(as_count)):
                list_as.append(as_number)
                as_number = str(int(as_number) + 1)

            lacnic_country_as_dict.update({country: list_as})
        
        #line_index += 1
    #else:
        #done = True


###### AFRINIC ######

afrinic_file = open("delegated-afrinic-20111115", "rb")
afrinic_lines = afrinic_file.readlines()[4:]
afrinic_file.close()

# afrinic_country_as_dict pattern
# country : list of AS
# "ZA" : [173,174,1250]
afrinic_country_as_dict = {}

done = False
line_index = 0

while(not done):
    line = afrinic_lines[line_index].decode("utf-8")[:-1].split("|")

    if(line[2] == "asn" and line[3].isnumeric()):

        country = line[1]
        as_number = line[3]
        as_count = line[4]

        if(country in afrinic_country_as_dict):
            for _ in range(0,int(as_count)):
                if(as_number not in afrinic_country_as_dict[country]):
                    afrinic_country_as_dict[country].append(as_number)
                as_number = str(int(as_number) + 1)
        else:
            list_as = []
            for _ in range(0,int(as_count)):
                list_as.append(as_number)
                as_number = str(int(as_number) + 1)

            afrinic_country_as_dict.update({country: list_as})
        
        line_index += 1
    else:
        done = True



###### RIPENCC ######

ripencc_file = bz2.open("delegated-ripencc-20111115.bz2", "rb")
ripencc_lines = ripencc_file.readlines()[4:]
ripencc_file.close()

# ripencc_country_as_dict pattern
# country : list of AS
# "FR" : [173,174,1250]
ripencc_country_as_dict = {}

done = False
line_index = 0

while(not done):
    line = ripencc_lines[line_index].decode("utf-8")[:-1].split("|")

    if(line[2] == "ipv6"):
        done = True
    elif(line[2] == "asn"):
        country = line[1]
        as_number = line[3]
        as_count = line[4]

        if(country in ripencc_country_as_dict):
            for _ in range(0,int(as_count)):
                if(as_number not in ripencc_country_as_dict[country]):
                    ripencc_country_as_dict[country].append(as_number)
                as_number = str(int(as_number) + 1)
        else:
            list_as = []
            for _ in range(0,int(as_count)):
                list_as.append(as_number)
                as_number = str(int(as_number) + 1)

            ripencc_country_as_dict.update({country: list_as})
        
    line_index += 1
        


###### GENERATE THE INFO ######

country_info_lines = []

###### APNIC ######

apnic_aloccated_as = 0
apnic_used_as = 0
apnic_politics = [0,0,0,0,0]

# apnic_country_info_dict pattern
# country : list of info (aloccated AS's, used AS's, politic 0's, politic 1's, politic 2's, politic 3's,  politic 4's)
# "JP" : [100,90,10,20,30,30,0]
apnic_country_info_dict = {}

for item in apnic_country_as_dict.items():
    country = item[0]
    aloccated_as = len(item[1])
    used_as = 0
    politics = [0,0,0,0,0]

    for as_number in item[1]:
        if(as_number in as_policies_dict):
            used_as += 1

            if(len(as_policies_dict[as_number]) > 1):
                politics[4] += 1
            else:
                politics[int(as_policies_dict[as_number][0])] += 1

    apnic_aloccated_as += aloccated_as
    apnic_used_as += used_as
    apnic_politics[0] += politics[0]
    apnic_politics[1] += politics[1]
    apnic_politics[2] += politics[2]
    apnic_politics[3] += politics[3]
    apnic_politics[4] += politics[4]

    line = "apnic|" + country + "|" + str(aloccated_as) + "|" + str(used_as) + "|" + str(politics[0]) + "|" + str(politics[1]) + "|" + str(politics[2]) + "|" + str(politics[3]) + "|" + str(politics[4]) + "\n"
    country_info_lines.append(line)

apnic_info_line = "apnic|" + str(apnic_aloccated_as) + "|" + str(apnic_used_as) + "|" + str(apnic_politics[0]) + "|" + str(apnic_politics[1]) + "|" + str(apnic_politics[2]) + "|" + str(apnic_politics[3]) + "|" + str(apnic_politics[4]) + "\n"


###### ARIN ######


arin_aloccated_as = 0
arin_used_as = 0
arin_politics = [0,0,0,0,0]

# arin_country_info_dict pattern
# country : list of info (aloccated AS's, used AS's, politic 0's, politic 1's, politic 2's, politic 3's,  politic 4's)
# "JP" : [100,90,10,20,30,30,0]
arin_country_info_dict = {}

for item in arin_country_as_dict.items():
    country = item[0]
    aloccated_as = len(item[1])
    used_as = 0
    politics = [0,0,0,0,0]

    for as_number in item[1]:
        if(as_number in as_policies_dict):
            used_as += 1

            if(len(as_policies_dict[as_number]) > 1):
                politics[4] += 1
            else:
                politics[int(as_policies_dict[as_number][0])] += 1

    arin_aloccated_as += aloccated_as
    arin_used_as += used_as
    arin_politics[0] += politics[0]
    arin_politics[1] += politics[1]
    arin_politics[2] += politics[2]
    arin_politics[3] += politics[3]
    arin_politics[4] += politics[4]

    line = "arin|" + country + "|" + str(aloccated_as) + "|" + str(used_as) + "|" + str(politics[0]) + "|" + str(politics[1]) + "|" + str(politics[2]) + "|" + str(politics[3]) + "|" + str(politics[4]) + "\n"
    country_info_lines.append(line)

arin_info_line = "arin|" + str(arin_aloccated_as) + "|" + str(arin_used_as) + "|" + str(arin_politics[0]) + "|" + str(arin_politics[1]) + "|" + str(arin_politics[2]) + "|" + str(arin_politics[3]) + "|" + str(arin_politics[4]) + "\n"



###### LACNIC ######

lacnic_aloccated_as = 0
lacnic_used_as = 0
lacnic_politics = [0,0,0,0,0]

# lacnic_country_info_dict pattern
# country : list of info (aloccated AS's, used AS's, politic 0's, politic 1's, politic 2's, politic 3's,  politic 4's)
# "JP" : [100,90,10,20,30,30,0]
lacnic_country_info_dict = {}

for item in lacnic_country_as_dict.items():
    country = item[0]
    aloccated_as = len(item[1])
    used_as = 0
    politics = [0,0,0,0,0]

    for as_number in item[1]:
        if(as_number in as_policies_dict):
            used_as += 1

            if(len(as_policies_dict[as_number]) > 1):
                politics[4] += 1
            else:
                politics[int(as_policies_dict[as_number][0])] += 1

    lacnic_aloccated_as += aloccated_as
    lacnic_used_as += used_as
    lacnic_politics[0] += politics[0]
    lacnic_politics[1] += politics[1]
    lacnic_politics[2] += politics[2]
    lacnic_politics[3] += politics[3]
    lacnic_politics[4] += politics[4]

    line = "lacnic|" + country + "|" + str(aloccated_as) + "|" + str(used_as) + "|" + str(politics[0]) + "|" + str(politics[1]) + "|" + str(politics[2]) + "|" + str(politics[3]) + "|" + str(politics[4]) + "\n"
    country_info_lines.append(line)

lacnic_info_line = "lacnic|" + str(lacnic_aloccated_as) + "|" + str(lacnic_used_as) + "|" + str(lacnic_politics[0]) + "|" + str(lacnic_politics[1]) + "|" + str(lacnic_politics[2]) + "|" + str(lacnic_politics[3]) + "|" + str(lacnic_politics[4]) + "\n"




###### AFRINIC ######


afrinic_aloccated_as = 0
afrinic_used_as = 0
afrinic_politics = [0,0,0,0,0]

# afrinic_country_info_dict pattern
# country : list of info (aloccated AS's, used AS's, politic 0's, politic 1's, politic 2's, politic 3's,  politic 4's)
# "JP" : [100,90,10,20,30,30,0]
afrinic_country_info_dict = {}

for item in afrinic_country_as_dict.items():
    country = item[0]
    aloccated_as = len(item[1])
    used_as = 0
    politics = [0,0,0,0,0]

    for as_number in item[1]:
        if(as_number in as_policies_dict):
            used_as += 1

            if(len(as_policies_dict[as_number]) > 1):
                politics[4] += 1
            else:
                politics[int(as_policies_dict[as_number][0])] += 1

    afrinic_aloccated_as += aloccated_as
    afrinic_used_as += used_as
    afrinic_politics[0] += politics[0]
    afrinic_politics[1] += politics[1]
    afrinic_politics[2] += politics[2]
    afrinic_politics[3] += politics[3]
    afrinic_politics[4] += politics[4]

    line = "afrinic|" + country + "|" + str(aloccated_as) + "|" + str(used_as) + "|" + str(politics[0]) + "|" + str(politics[1]) + "|" + str(politics[2]) + "|" + str(politics[3]) + "|" + str(politics[4]) + "\n"
    country_info_lines.append(line)

afrinic_info_line = "afrinic|" + str(afrinic_aloccated_as) + "|" + str(afrinic_used_as) + "|" + str(afrinic_politics[0]) + "|" + str(afrinic_politics[1]) + "|" + str(afrinic_politics[2]) + "|" + str(afrinic_politics[3]) + "|" + str(afrinic_politics[4]) + "\n"



###### RIPENCC ######


ripencc_aloccated_as = 0
ripencc_used_as = 0
ripencc_politics = [0,0,0,0,0]

# ripencc_country_info_dict pattern
# country : list of info (aloccated AS's, used AS's, politic 0's, politic 1's, politic 2's, politic 3's,  politic 4's)
# "JP" : [100,90,10,20,30,30,0]
ripencc_country_info_dict = {}

for item in ripencc_country_as_dict.items():
    country = item[0]
    aloccated_as = len(item[1])
    used_as = 0
    politics = [0,0,0,0,0]

    for as_number in item[1]:
        if(as_number in as_policies_dict):
            used_as += 1

            if(len(as_policies_dict[as_number]) > 1):
                politics[4] += 1
            else:
                politics[int(as_policies_dict[as_number][0])] += 1

    ripencc_aloccated_as += aloccated_as
    ripencc_used_as += used_as
    ripencc_politics[0] += politics[0]
    ripencc_politics[1] += politics[1]
    ripencc_politics[2] += politics[2]
    ripencc_politics[3] += politics[3]
    ripencc_politics[4] += politics[4]

    line = "ripencc|" + country + "|" + str(aloccated_as) + "|" + str(used_as) + "|" + str(politics[0]) + "|" + str(politics[1]) + "|" + str(politics[2]) + "|" + str(politics[3]) + "|" + str(politics[4]) + "\n"
    country_info_lines.append(line)

ripencc_info_line = "ripencc|" + str(ripencc_aloccated_as) + "|" + str(ripencc_used_as) + "|" + str(ripencc_politics[0]) + "|" + str(ripencc_politics[1]) + "|" + str(ripencc_politics[2]) + "|" + str(ripencc_politics[3]) + "|" + str(ripencc_politics[4]) + "\n"

final_file = open("policies.txt","w")
final_file.write(apnic_info_line)
final_file.write(arin_info_line)
final_file.write(lacnic_info_line)
final_file.write(afrinic_info_line)
final_file.write(ripencc_info_line)
final_file.writelines(country_info_lines)

final_file.close()