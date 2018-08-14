from random import randint

def get_host():
    index = randint(0, 1)
    if index == 0:
        host = "us" + str(randint(1, 1706)) + ".nordvpn.com"
    else:
        host = "ca" + str(randint(1, 291)) + ".nordvpn.com"
    return host

EMAIL_EMAIL = ""
EMAIL_PASSWORD = ""
EMAIL_SMTP = "smtp-mail.outlook.com"
HOST = ""
PORT = "80"
USERNAME = ""
PASSWORD = ""

MIN_PRICE = "500000"
MAX_PRICE = "2000000"
MAX_AGE = "200"
MIN_AGE = "0"
MIN_BEDROOM = "1"
MIN_BATHROOM = "1"
EMAIL_LIST = []
MIN_LOT_SIZE = {"Vancouver West": 4000,
                "Vancouver East": 4000,
                "Burnaby": 5000,
                "New Westminster": 5000,
                "Maple Ridge": 8000,
                "Coquitlam": 8000,
		"Mission": 8000}

# DO NOT CHANGE VALUES BELOW
RSPP = "20"  # not sure what this is
SRTB = "P_Price"  # not sure what this is
ERTA = "true"  # not sure what this is
SCTP = "RA"  # not sure what this is
ROW_P = "1"
PTYTID = "5"  # not sure what this is
