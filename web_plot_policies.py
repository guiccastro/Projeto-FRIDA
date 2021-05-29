# @Code created by Guilherme Silva de Castro on may 2021 and last updated on may 2021.@

############################################################
# This code will generate a plot as the plot_policies.py, but this one will be on web. The plot is create by the Bokeh API. The plot will be based on the 
# files created in the code prepending_policies.py, that must be in the path: web_plot_policies-PATH/Policies. 
# In this path, the IPv4 and IPv6 files must be in different folders, so, it must exist 
# a web_plot_policies-PATH/Policies/IPv4 and web_plot_policies-PATH/Policies/IPv6. 
# The files will be read from this paths.
# To run this code, a Bokeh server will be needed, so the command to run this code in the terminal is:
# $ bokeh serve --show web_plot_policies.py

##############################################################################
# TO DO AND IDEAS:
# [ ] - Ajust the Dropdown's list that stays behind the plot.
# [ ] - Don't let the user create a plot when some information was not selected.
# [ ] - Draw all the countrys in the plot, even the ones with no info (draw them in gray maybe).
# [ ] - Show the colorbar always with a info from 0 to 100 in the percentage infos.

##############################################################################
# KNOWN ISSUES (SOLUTIONS):
# Dropdown's list stays behind the plot.

from bokeh.palettes import Viridis256 as palette
from bokeh.plotting import figure, curdoc
from bokeh.models import Button, RadioButtonGroup, ColorBar, LinearColorMapper
from bokeh.models.widgets import Dropdown
from bokeh.layouts import column, row
import cartopy.io.shapereader as shpreader
import pycountry
from os import listdir

# Class to keep all informations about a country.
# ----------------------------------------------------
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

    global countries_list

    result_list = []
    for country in countries_list:
        result_list.append(country.country_obj)

    return result_list

# Function to find the geometry of the country.
# The geometries of the countries are get from the cartopy lib.
def FindGeometry(country):
    
    global country_info

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

# List the years that appears in the files list. 
# Returns a list of Strings.
def ListYears():

    years = []

    for file in list_files:
        if(file[:4] not in years):
            years.append(file[:4])
    
    return years

# List the months that appears in the files list based on a year. 
# Returns a list of Strings.
def ListMonths(year):

    months = []

    for file in list_files:
        if(file[:4] == year and file[4:6] not in months):
            months.append(file[4:6])

    return months

# List the days that appears in the files list based on a year and a month. 
# Returns a list of Strings.
def ListDays(year, month):

    days = []

    for file in list_files:
        if(file[:4] == year and file[4:6] == month and file[6:-4] not in days):
            days.append(file[6:-4])

    return days

# Change the selected prefix type.
# New is the value of the selected, it works as a list. For example, the options is ["IPv4","IPv6"],
# if the selected was IPv4 than the new value will be 0, if was IPv6 the new value will be 1.
def OnChangeIPv4IPv6RadioButton(attr, old, new): 

    global year_dropdown
    global month_dropdown
    global day_dropdown
    global list_files
    global selected_prefix_type

    # When a new prefix type is selected, the months and days Dropdowns needs to be disabled, because a new year must me selected first.
    month_dropdown.disabled = True
    day_dropdown.disabled = True

    # As the files is supposed to be separated by IPv4 and IPv6 folder, when the prefix type is changed, the list of files needs top be updated.
    if(new == 0):
        selected_prefix_type = "IPv4"
        list_files = listdir("Policies/IPv4")
    else:
        selected_prefix_type = "IPv6"
        list_files = listdir("Policies/IPv6")

    # The list of year needs to be updated too.
    year_dropdown.menu = ListYears()
    year_dropdown.menu.sort()

# Change the selected year. The "event" variable holds the item from the list that was selected.
def OnClickYearDropdown(event):

    global selected_year
    global month_dropdown

    # Change the selected year. The variable will be of type String.
    selected_year = event.item

    # Enable the month Dropdown.
    month_dropdown.disabled = False

    # Update the list of months.
    month_dropdown.menu = ListMonths(selected_year)
    month_dropdown.menu.sort()

# Change the selected month. The "event" variable holds the item from the list that was selected.
def OnClickMonthDropdown(event):

    global selected_year
    global selected_month
    global day_dropdown

    # Change the selected month. The variable will be of type String.
    selected_month = event.item

    # Enable the day Dropdown.
    day_dropdown.disabled = False

    # Update the list of days.
    day_dropdown.menu = ListDays(selected_year,selected_month)
    day_dropdown.menu.sort()

# Change the selected month. The "event" variable holds the item from the list that was selected.
def OnClickDayDropdown(event):

    global selected_day

    # Change the selected day. The variable will be of type String.
    selected_day = event.item

# Change the type of plot. Here, the new variable works as was explained in the OnChangeIPv4IPv6RadioButton function.
# The list of possible values for new is:
# 0 -> Number of total used AS's
# 1 -> Number of AS's per policy
# 2 -> Percentage of AS's per policy
def OnChangePlotTypeRadioButton(attr, old, new):

    global policies_radio_button
    global plot_type
    global selected_policy

    # If the selected type of plot was not the "Number of total used AS's", a of type of policy needs to be chosen.
    if(new != 0):
        policies_radio_button.visible = True
    else:
        policies_radio_button.visible = False
        selected_policy = None

    # Change the type of plot.
    plot_type = new

# Change the selected policy. Here, the new variable works as was explained in the OnChangeIPv4IPv6RadioButton function.
# The list of possible values for new is:
# 0 -> Without prepending
# 1 -> With prepending
# 2 -> Uniform policy
# 3 -> Binary policy
# 4 -> Diverse policy
# 5 -> Mixed policy
def OnChangePoliciesRadioButton(attr, old, new):

    global selected_policy

    # Change the selected policy.
    selected_policy = new

# Creates the plot.
def OnClickUpdatePlotButton():
    
    global selected_prefix_type
    global selected_year
    global selected_month
    global selected_day
    global plot_type
    global selected_policy
    global p
    global palette
    global doc

    # First, the file selecetd by the dates needs to be read.
    # Open the file with the policies.
    if(selected_prefix_type == "IPv4"):
        policies_file = open("Policies/IPv4/" + selected_year + selected_month + selected_day + ".txt","rb")
    else:
        policies_file = open("Policies/IPv6/" + selected_year + selected_month + selected_day + ".txt","rb")

    # Read the lines from the file.
    policies_lines = policies_file.readlines()

    # Close the file.
    policies_file.close()

    # Download the infos from the countries from the cartopy lib.
    # This infos holds the geometrys for the countries.
    # In this moment that this part of the code was made, this API only has information about 177 countries.
    shpfilename = shpreader.natural_earth(resolution='110m',category='cultural',name='admin_0_countries')

    # Read the infos.
    reader = shpreader.Reader(shpfilename)

    # countries_info will be used in the function FindGeometry, so it needs to be set as Global.
    global countries_info
    countries_info = list(reader.records())

    # Separates the region lines and the country lines.
    regions_lines = policies_lines[:5] # Not used for now.
    country_lines = policies_lines[5:]

    # Initizalize some lists.
    # To keep the countries from policies's file.
    # countries_list will be used in the function GetCountryObjectList, so it needs to be set as Global.
    global countries_list
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

            # Verifies if the number of used AS's is bigger than zero.
            # Otherwise, a division by zero would occur.
            if(number_used_as > 0):

                # Get the percentage of the policy 0 first, because the max number its diferent from the other policies.
                # The percentages of policy 0 is based on the number of used AS's.
                list_percentage_policies[0] = (list_number_policies[0] * 100) / number_used_as

                # The percentages of policies 1 to 4 is based on the number of used AS's that are not policy 0 (used_as - list_number_policies[0]).
                percentage_ref = number_used_as - list_number_policies[0]

                # Verifies if the percentage reference of AS's with policies 1 to 4 is bigger than zero.
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

                # Verifies if the number of used AS's is bigger than zero.
                # Otherwise, a division by zero would occur.
                if(country.used_as > 0):

                    # Update the percentage of AS's with policy 0.
                    country.percentage_policies[0] = (country.number_policies[0] * 100) / country.used_as

                    # Update the percentage reference.
                    percentage_ref = country.used_as - country.number_policies[0]

                    # Verifies if the percentage reference of AS's with policies 1 to 4 is bigger than zero.
                    # Otherwise, a division by zero would occur.
                    if(percentage_ref > 0):

                        # Update the percentage of AS's with policy 1 to 4.
                        for i in range(1,5):
                            country.percentage_policies[i] = (country.number_policies[i] * 100) / percentage_ref

        except: # If an error occur...

            # Add the letter code of the country that generate an error to the list.
            error_letter_code.append(country_letter_code)

    # Initializes the lists that will be used in the plot.
    # Each position in the list of points will represent a polygon of a country.
    # For example, if a country A have a geometry {[(1,1), (2,2)], [(3,3), (4,4)]}, and a 
    # country B have a geometry {[(1,2), (2,1)], [(3,4), (4,3)]},
    # (each value inside "(X,Y)" represent a point from the polygon "[]" from the geometry "{}"), the list 
    # of X and Y points, and the list names would be: 
    # X = [[1,2], [3,4], [1,2], [3,4]] 
    # Y = [[1,2], [3,4], [2,1], [4,3]]
    # Names = [A, A, B, B]
    # The names is to represent from which country the point represents, so X[0] and Y[0] is a polygon from the country Names[0].
    list_x_points = []
    list_y_points = []
    list_names = []
    list_allocated_as = []
    list_used_as = []
    list_number_policy_0 = []
    list_number_policy_1 = []
    list_number_policy_2 = []
    list_number_policy_3 = []
    list_number_policy_4 = []
    list_number_policy_5 = []
    list_percentage_policy_0 = []
    list_percentage_policy_1 = []
    list_percentage_policy_2 = []
    list_percentage_policy_3 = []
    list_percentage_policy_4 = []
    list_percentage_policy_5 = []

    # As the we already know what countris need to be drawn (the ones with info in the files read above),
    # needs to find its geometries in the info from the API.
    for country in countries_list:

        # Gets the geometry of the current country.
        geometry = FindGeometry(country)

        # If was found...
        if(geometry != None):

            # A country can have more than one polygon to represent the country's geometry.
            for polygon in list(geometry):

                # Initializes the auxiliar list of points.
                x_points = []
                y_points = []

                # Iterates through each point from the polygon.
                for point in list(polygon.exterior.coords):

                    # Adds the points.
                    x_points.append(point[0])
                    y_points.append(point[1])

                # Adds the list of points and the others informations from the current country.
                list_x_points.append(x_points)
                list_y_points.append(y_points)
                list_names.append(country.country_obj.name)
                list_allocated_as.append(country.allocated_as)
                list_used_as.append(country.used_as)
                list_number_policy_0.append(country.number_policies[0])
                list_number_policy_1.append(country.number_policies[1])
                list_number_policy_2.append(country.number_policies[2])
                list_number_policy_3.append(country.number_policies[3])
                list_number_policy_4.append(country.number_policies[4])
                list_number_policy_5.append(country.used_as - country.number_policies[0])
                list_percentage_policy_0.append(country.percentage_policies[0])
                list_percentage_policy_1.append(country.percentage_policies[1])
                list_percentage_policy_2.append(country.percentage_policies[2])
                list_percentage_policy_3.append(country.percentage_policies[3])
                list_percentage_policy_4.append(country.percentage_policies[4])
                list_percentage_policy_5.append(100.0 - country.percentage_policies[0])

    # Create a dictonary to keep the informations to make the plot
    data=dict(
        x=list_x_points,
        y=list_y_points,
        name=list_names,
        allocated_as=list_allocated_as,
        used_as=list_used_as,
        number_policy_0=list_number_policy_0,
        number_policy_1=list_number_policy_1,
        number_policy_2=list_number_policy_2,
        number_policy_3=list_number_policy_3,
        number_policy_4=list_number_policy_4,
        number_policy_5=list_number_policy_5,
        percentage_policy_0=list_percentage_policy_0,
        percentage_policy_1=list_percentage_policy_1,
        percentage_policy_2=list_percentage_policy_2,
        percentage_policy_3=list_percentage_policy_3,
        percentage_policy_4=list_percentage_policy_4,
        percentage_policy_5=list_percentage_policy_5,
    )

    # Set the tools that can be used in the plot.
    TOOLS = "pan,wheel_zoom,reset,hover,save"

    # Initialize the type of data that will be plot.
    TYPE_DATA = ""

    # Verifies if the type of plot is "Number of total used AS's".
    if(plot_type == 0):
        TITLE = "Number of total used AS's"
        TYPE_DATA = "used_as"

    # Verifies if the type of plot is "Number of AS's".
    elif(plot_type == 1):
        TITLE = "Number of AS's "

        # Verifies which type of policy.
        if(selected_policy == 0):
            TITLE += "without prepending"
            TYPE_DATA = "number_policy_0"
        elif(selected_policy == 1):
            TITLE += "with prepending"
            TYPE_DATA = "number_policy_5"
        elif(selected_policy == 2):
            TITLE += "with uniform policy"
            TYPE_DATA = "number_policy_1"
        elif(selected_policy == 3):
            TITLE += "with binary policy"
            TYPE_DATA = "number_policy_2"
        elif(selected_policy == 4):
            TITLE += "with diverse policy"
            TYPE_DATA = "number_policy_3"
        elif(selected_policy == 5):
            TITLE += "with mixed policy"
            TYPE_DATA = "number_policy_4"

    # The type of plot is "Percentage of AS's".
    else:
        TITLE = "Percentage of AS's "

        # Verifies which type of policy.
        if(selected_policy == 0):
            TITLE += "without prepending"
            TYPE_DATA = "percentage_policy_0"
        elif(selected_policy == 1):
            TITLE += "with prepending"
            TYPE_DATA = "percentage_policy_5"
        elif(selected_policy == 2):
            TITLE += "with uniform policy"
            TYPE_DATA = "percentage_policy_1"
        elif(selected_policy == 3):
            TITLE += "with binary policy"
            TYPE_DATA = "percentage_policy_2"
        elif(selected_policy == 4):
            TITLE += "with diverse policy"
            TYPE_DATA = "percentage_policy_3"
        elif(selected_policy == 5):
            TITLE += "with mixed policy"
            TYPE_DATA = "percentage_policy_4"

    # Finalize the title.
    TITLE += " for " + selected_prefix_type + " on " + selected_month + "/" + selected_day + "/" + selected_year + "."

    # Remove the old plot from the document.
    doc.remove_root(p)

    # Create the new plot.
    p = figure(
        title=TITLE, tools=TOOLS,
        x_axis_location=None, y_axis_location=None,plot_width=1200, plot_height=500,
        tooltips=[ # Informations that will be shown when the mouse stay on top. 
            ("Name", "@name"), ("Used AS's", "@used_as"), ("Number without prepending", "@number_policy_0"), ("Number with prepending", "@number_policy_5"),
            ("Number with uniform policy", "@number_policy_1"), ("Number with binary policy", "@number_policy_2"),
            ("Number with diverse policy", "@number_policy_3"), ("Number with mixed policy", "@number_policy_4"),
            ("Percentage without prepending", "@percentage_policy_0%"), ("Percentage with prepending", "@percentage_policy_5%"), ("Percentage of uniform policy", "@percentage_policy_1%"),
            ("Percentage of binary policy", "@percentage_policy_2%"), ("Percentage of diverse policy", "@percentage_policy_3%"),
            ("Percentage of mixed policy", "@percentage_policy_4%")
        ])

    # Disable the grid.
    p.grid.grid_line_color = None

    # The policy for the point of the plot.
    p.hover.point_policy = "follow_mouse"

    # Initialize the palette.
    palette = tuple(palette)

    # Set the max and the min of the info that will be shown.
    MAX = max(data[TYPE_DATA])
    MIN = min(data[TYPE_DATA])

    # Create the color map.
    color_mapper = LinearColorMapper(palette=palette, high=MAX, low=MIN)

    # Create the plot with the infos.
    p.patches('x', 'y', source=data,
            fill_color={'field': TYPE_DATA, 'transform': color_mapper},
            fill_alpha=1.0, line_color="black", line_width=1.0)
    
    # Create a colorbar to be shown in the plot.
    color_bar = ColorBar(color_mapper=color_mapper, major_tick_line_color="black", major_tick_out=5, bar_line_color="black")
    
    # Adds the colorbar to the right of the plot.
    p.add_layout(color_bar, 'right')

    # Add the new plot to the document.
    # This will make the plot to be "above" the other objects, hiding the list of year, month and day. (Needs to be fixed)
    doc.add_root(p)


# Document to keep the objects in the server
doc = curdoc()

# Initilizes some usefull variables
list_files = listdir("Policies/IPv4")
selected_prefix_type = "IPv4"
selected_year = ListYears()[0]
selected_month = ListMonths(selected_year)[0]
selected_day = ListDays(selected_year, selected_month)[0]
plot_type = 0
selected_policy = None

# Choose between IPv4 and IPv6.
LABELS_IPV4_IPV6 = ["IPv4", "IPv6"]
ipv4_ipv6_radio_button = RadioButtonGroup(labels=LABELS_IPV4_IPV6, active=0)
ipv4_ipv6_radio_button.on_change("active", OnChangeIPv4IPv6RadioButton) # Change the selected prefix.

# Dropdown to select the year.
# Dropdown list is based on the chosen prefix type, for example, if IPv4 is selected, only years with IPv4 files will be shown.
year_dropdown = Dropdown(label="Select year", menu=ListYears())
year_dropdown.on_click(OnClickYearDropdown) # Change the selected year.

# Dropdown to select the month. The months that will be shown is based os the selected prefix and the selected year.
month_dropdown = Dropdown(label="Select month", menu=ListMonths(selected_year))
month_dropdown.on_click(OnClickMonthDropdown) # Change the selected month.
month_dropdown.disabled = True # It will only let the user select the month if the year was already selected.

# Dropdown to select the day. The days that will be shown is based os the selected prefix, the selected year and the selected month.
day_dropdown = Dropdown(label="Select day", menu=ListDays(selected_year,selected_month))
day_dropdown.on_click(OnClickDayDropdown) # Change the selected day.
day_dropdown.disabled = True # It will only let the user select the day if the year and the month was already selected.

# Choose the type of plot.
LABELS_PLOT_TYPE = ["Number of total used AS's", "Number of AS's per policy", "Percentage of AS's per policy"]
plot_type_radio_button = RadioButtonGroup(labels=LABELS_PLOT_TYPE, active=0)
plot_type_radio_button.on_change("active", OnChangePlotTypeRadioButton) # Change the selected type of plot.

# Choose the policie. 
LABELS_POLICIES = ["Without prepending", "With prepending", "Uniform policy", "Binary policy", "Diverse policy", "Mixed policy"]
policies_radio_button = RadioButtonGroup(labels=LABELS_POLICIES, active=0)
policies_radio_button.on_change("active", OnChangePoliciesRadioButton) # Change the selected policy.
policies_radio_button.visible = False # This option will be only shown if the selected type of plot be the number per policy or the percentage per policy.

# Button to create the plot.
update_plot_button = Button(label="Update Plot", button_type="success")
update_plot_button.on_click(OnClickUpdatePlotButton) # Call the function that will generate the plot.

# Initizalizes the plot.
# It is not really necessary to initizalize the plot, but to make the function OnClickUpdatePlotButton() more generic, it will help.
# A button it's initialized as the plot, because if a empty plot is initialize, for some reason the "doc.remove_root(p)" on OnClickUpdatePlotButton() does not remove the plot.
# To make up for it, the button is not visible.
# A empty variable (p = None) can not be passed, because will generate an error when added to the doc.
p = Button(label="Update Plot", button_type="success")
p.visible = False

# Add all the above objects to the document in a column (it will make them stay in the same "level").
# You will see that the list of Dropdowns will be behind the plot, because new plots will be generated "above" this objects. (This need to be fixed).
doc.add_root(column(ipv4_ipv6_radio_button, row(year_dropdown,month_dropdown,day_dropdown), plot_type_radio_button, policies_radio_button, update_plot_button, p))