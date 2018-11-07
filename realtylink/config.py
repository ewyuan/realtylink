
"""
The settings below are for your email account.

The email account is used for sending the output CSV file to the email list.
"""
EMAIL_EMAIL = ""
EMAIL_PASSWORD = ""
EMAIL_SMTP = ""
EMAIL_LIST = []

"""
The settings below are for the scraper.
"""
# If RUN_DAILY is True, then the START_TIME needs to be configured.
RUN_DAILY = False

# START_TIME represents the starting time for the algorithm. (START_TIME is in 24hr clock format)
START_TIME = "09:00"

# If PROXY_SUPPORT is True, then the proxy account information below needs to be filled out.
PROXY_SUPPORT = True



"""
The settings below are for your proxy account.

This program's proxy support was based on NordVPN's proxy servers.
"""
HOST = ""
PORT = ""
USERNAME = ""
PASSWORD = ""

# # The function below was used to generate random proxies for requests to use
# from random import randint
# def get_host():
#     index = randint(0, 1)
#     if index == 0:
#         host = "us" + str(randint(1, 1706)) + ".nordvpn.com"
#     else:
#         host = "ca" + str(randint(1, 291)) + ".nordvpn.com"
#     return host
""" 
The settings below represent the configurable search settings.

Please note, cities.csv will need to be changed to contain the neighbourhood codes.
The neighbourhood codes are found by navigating to the neighbourhood page of a given city
and traversing the following xPath: 
/html/body/div/table[1]/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/form/select
"""
# MIN_PRICE represents the lower bound of the property listing price
MIN_PRICE = "500000"

# MAX_PRICE represents the upper bound of the property listing price
MAX_PRICE = "2000000"

# MAX_AGE represents the maximum age of the property
# 0 Years Old: "0"
# 1 Year Old: "1"
# 10 Years Old: "10"
# 20 Years Old: "20"
# 30 Years Old: "30"
# 40 Years Old: "40"
# 50 Years Old: "50"
# 60 Years Old: "60"
# 70 Years Old: "70"
# 80 Years Old: "80"
# 90+ Years Old: "200"
MAX_AGE = "200"

# MIN_AGE represents the minimum age of the property
# 0 Years Old: "0"
# 1 Year Old: "1"
# 10 Years Old: "10"
# 20 Years Old: "20"
# 30 Years Old: "30"
# 40 Years Old: "40"
# 50 Years Old: "50"
# 60 Years Old: "60"
# 70 Years Old: "70"
# 80 Years Old: "80"
# 90+ Years Old: "200"
MIN_AGE = "0"

# MIN_BEDROOM represents the minimum number of bedrooms in the property
# 0 or more: "0"
# 1 or more: "1"
# 2 or more: "2"
# 3 or more: "3"
# 4 or more: "4"
# 5 or more: "5"
MIN_BEDROOM = "1"

# MIN_BATHROOM represents the minimum number of bathrooms in the property
# 0 or more: "0"
# 1 or more: "1"
# 2 or more: "2"
# 3 or more: "3"
# 4 or more: "4"
# 5 or more: "5"
MIN_BATHROOM = "1"

# MIN_LOT_SIZE represents the the minimum lot size in order for the scraper to track the property.
# If the listing is not available, then the listing is still tracked although it may not meet the
# minimum property size requirement.
# {CITY_NAME: SIZE}, CITY_NAME is a string and case sensitive; SIZE is an int and in square feet
MIN_LOT_SIZE = {"Vancouver West": 4000,
                "Vancouver East": 4000,
                "Burnaby": 5000,
                "New Westminster": 5000,
                "Maple Ridge": 8000,
                "Coquitlam": 8000,
		        "Mission": 8000}

# PTYTID represents the type of property
# Apartment = "1"
# Townhouse = "2"
# Duplex = "3"
# Farm or Ranch = "4"
# House = "5"
# Mobile Home = "6"
# Multiplex = "7"
# Recreational w/Building = "8"
# Recreational wo/Building = "12"
# Others = "9"
# Lot = "10"
# Acreage = "11"
PTYTID = "5"  # not sure what this is

""" Changing the variables may make the scraper's behaviour unstable """
# RSPP represents the number of properties listed per page
RSPP = "25"

# ERTA represents whether you want to select all neighbourhoods of a given city
ERTA = "true"

# SRTB represents how listings are sorted by
SRTB = "P_Price"

SCTP = "RA"
ROW_P = "1"

