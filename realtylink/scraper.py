import csv
import time
import pandas as pd
import requests
from lxml import etree
from realtylink import config

def remove_trailing(string):
    """
    Return a new string with trailing spaces on the left and right side of the string.

    :param string: string to remove sequences from
    :return: str
    """
    string = string.lstrip()
    string = string.rstrip()
    return string

def generate_links(file):
    """ Return a list of generated links based on the information from the csv file and config.py.

    :param str file: the name of the csv file
    :rtype: list
    """
    links = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skips header
        for row in reader:
            gv, area_title, aprk, aidl = row[0], row[1], row[2], row[3]
            link = "http://www.realtylink.org/prop_search/Summary.cfm?" \
                   "BCD=" + gv + "&" \
                   "areatitle=" + area_title + "&" \
                   "ARPK=" + aprk + "&" \
                   "AIDL=" + aidl + "&" \
                   "RSPP=" + config.RSPP + "&" \
                   "SRTB=" + config.SRTB + "&" \
                   "ERTA=" + config.ERTA + "&" \
                   "MNAGE=" + config.MIN_AGE + "&" \
                   "MXAGE=" + config.MAX_AGE + "&" \
                   "MNBD=" + config.MIN_BEDROOM + "&" \
                   "MNBT=" + config.MIN_BATHROOM + "&" \
                   "PTYTID=" + config.PTYTID + "&" \
                   "MNPRC=" + config.MIN_PRICE + "&" \
                   "MXPRC=" + config.MAX_PRICE + "&" \
                   "SCTP=" + config.SCTP
            links.append(link)
        return links

""" Scrapes necessary information from realtylink.org. """


class Scraper:
    def __init__(self, yesterday_file, file):
        """
        Initialize a Scraper with the file.

        :param file: str
        """
        self.link = generate_links(file)
        self.data_frame = self.__build_empty_dataframe()
        self.houses = {}
        try:
            for i in pd.read_csv(yesterday_file).to_dict(orient="split")["data"]:
                key = i.pop(0)
                if i[0] != "Removed":
                    i.pop(0)
                    self.houses[key] = [""] + i
        except FileNotFoundError:
            print("File does not exist.")
        self.header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

    def get_pages(self):
        """
        Return a dictionary of all the pages and the number of houses listed on the page.

        :return: dict(str, int)
        """
        pages = {}
        for link in self.link:
            tree = self.__build_tree(link)
            options = tree.xpath("//html//option")
            if options is None:
                raise AttributeError
            for option in options:
                string = remove_trailing(option.text)
                values = string.split(" - ")
                if len(values) == 2:
                    num_houses = int(values[1]) - int(values[0]) + 1
                elif len(values) == 1:
                    num_houses = 1
                page = link + "&rowp=" + values[0]
                if page not in pages:
                    pages[page] = num_houses
        return pages

    def parse_realtylink_pages(self, pages):
        """
        Return a list of all the houses in areas in cities.csv with detailed information of the house.

        :param pages: dict(str, int)
        :return: list[str]
        """
        houses = {}
        for page in pages:
            tree = self.__build_tree(page)
            num_houses = pages[page]
            interval = 0
            for num in range(num_houses):
                address = tree.xpath("/html/body/div/table/tr[6]/td/table/tr["
                                     + str(5 + interval)
                                     + "]/td[1]/font")
                address = remove_trailing(address[0].text)
                location = tree.xpath("/html/body/div/table/tr[6]/td/table/tr["
                                      + str(3 + interval)
                                      + "]/td[2]/table/tr/td[1]/font/b")
                location = location[0].text.split(", ")
                neighbourhood = location[0]
                city = location[1]
                price = tree.xpath("/html/body/div/table/tr[6]/td/table/tr["
                                   + str(4 + interval)
                                   + "]/td[1]/font/text()")
                price = price[0][2:]
                mls = tree.xpath("/html/body/div/table/tr[6]/td/table/tr["
                                 + str(6 + interval)
                                 + "]/td[1]/font")
                mls = mls[0].text
                lot_dimensions = tree.xpath("/html/body/div/table/tr[6]/td/table/tr["
                                            + str(6 + interval)
                                            + "]/td[5]/font")
                lot_dimensions = remove_trailing(lot_dimensions[0].text)
                link = tree.xpath("/html/body/div/table/tr[6]/td/table/tr["
                                  + str(4 + interval)
                                  + "]/td[1]/a")
                link = "http://www.realtylink.org/prop_search/" + link[0].get("href")
                try:
                    lot_dimensions = lot_dimensions.split(" x ")
                    lot_size = float(lot_dimensions[0]) * float(lot_dimensions[1])
                    if lot_size >= config.MIN_LOT_SIZE[city]:
                        lot_size = round(lot_size, 2)
                        lot_size = str(lot_size)
                        houses[mls] = ["", city, neighbourhood, address, price, lot_size, link]
                except ValueError:
                    lot_size = "Not Available"
                    houses[mls] = ["", city, neighbourhood, address, price, lot_size, link]
                interval += 6

            if len(houses) == 0:
                raise Exception("Proxy error")
        return houses

    def update_houses(self, today_file, houses):
        """
        Modify houses, and return a list containing number of listings with new prices,
        new listings, and removed listings.

        Index 0 of the list returned represents to the number of price changes, index 1
        represents the number of new listings, and index 2 represents the number of listings removed.

        This method also updates the csv file after all the houses have been updated.

        :param today_file: str
        :param houses: dict(str: list[str])
        :return: list[int]
        """
        changes = [0, 0, 0]
        removed_houses = {}
        current_houses = {}
        for mls in self.houses:
            if mls in houses:
                current_houses[mls] = self.houses[mls]
            else:
                removed_houses[mls] = self.houses[mls]
                removed_houses[mls][0] = "Removed"
                changes[2] += 1

        for mls in houses:
            if mls in current_houses:
                current_price = float(current_houses[mls][4][:-2].replace(",", ""))
                listing_price = float(houses[mls][4][:-2].replace(",", ""))
                if current_price > listing_price:
                    houses[mls][0] = "Price Decrease from " + str(current_price)
                    changes[0] += 1
                elif current_price < listing_price:
                    houses[mls][0] = "Price Increase from " + str(current_price)
                    changes[0] += 1
                else:
                    houses[mls][0] = ""
            else:
                houses[mls][0] = "New Listing"
                changes[1] += 1

        houses.update(removed_houses)
        self.__update_csv(today_file, houses)
        return changes

    def __update_csv(self, file_name, houses):
        # """
        # Update the out.csv file with current houses.
        #
        # :param houses: dict(str: list[str])
        # :return: None
        # """
        df = pd.DataFrame.from_dict(houses,
                                    orient="index",
                                    columns=["Status", "City", "Neighbourhood", "Address",
                                             "Listing Price", "Lot Size", "RealtyLink"])
        self.data_frame = df
        self.data_frame.to_csv(file_name)

    def __build_tree(self, link):
        # """
        # Return an Element Tree constructed with the html of the downloaded link.
        #
        # :param link: str
        # :return: ElementTree
        # """
        time.sleep(10)  # add a 2 second delay
        session = requests.get(url=link,
                               headers=self.header,
                               proxies=dict(http='http://' + config.USERNAME +
                                                 ':' + config.PASSWORD +
                                                 '@' + config.HOST +
                                                 ':' + config.PORT))
        if session.status_code != requests.codes.ok:
            session.raise_for_status()
        try:
            tree = etree.HTML(session.text)
        except Exception as exc:
            print("There was a problem: %s" % exc)
            return None
        return tree

    def __build_empty_dataframe(self):
        # """
        # Return an empty pandas data frame with all the required columns set.
        #
        # :return: DataFrame
        # """
        df = pd.DataFrame()
        df["Status"] = ""
        df["City"] = ""
        df["Neighbourhood"] = ""
        df["Address"] = ""
        df["Listing Price"] = ""
        df["Lot Size"] = ""
        df["RealtyLink"] = ""
        return df
