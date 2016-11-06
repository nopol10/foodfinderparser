from pyquery import PyQuery as pq
import IParser
from geopy.geocoders import Nominatim
# address, rating, country, food_type, name, price


class ZomatoParser(IParser.IParser):
    def __init__(self, content, url):
        self.doc = pq(content)
        self.url = url

    def is_review(self):
        s = self.url.split('/')
        url_last = s[-1].strip()
        if url_last == "reviews" or url_last == "menu" or url_last == "photos":
            return False

        res = self.doc("meta[property='og:type']")
        if res.attr("content") == "zomatocom:restaurant":
            return True
        return False

    def extract_price(self):
        res = self.doc("span[itemprop='priceRange']").text()
        res = res.split()
        if res.__len__() <= 0:
            return 0.0
        if res[0] == "Average":
            price_str = res[1]
            price = ''
            for i in range(0, price_str.__len__()):
                if price_str[i].isdigit():
                    price += price_str[i]
            return float(price)
        return -1.0

    def extract_foodtypes(self):
        return self.doc("div[class='res-info-cuisines clearfix']").text()


    def extract_address(self):
        res = self.doc("div[class='borderless res-main-address']").text()
        return res

    def extract_food_title(self):
        res = self.doc("h1[itemprop='name']").text()
        return res

    def extract_numvote(self):
        try:
            res = self.doc("div[itemprop='ratingValue']").text()
            vote = res.split('/')[0]
            numvoter = self.doc("span[itemprop='ratingCount']").text()
            vote = float(vote) / 5.0
            numvoter = int(numvoter)
        except:
            return -1.0, -1
        return vote, numvoter

    def extract_country(self):
        try:
            geolocator = Nominatim()
            latitude = self.doc("meta[property='place:location:latitude']").attr("content")
            longtitude = self.doc("meta[property='place:location:longitude']").attr("content")
            location = geolocator.reverse(latitude+', ' + longtitude)
            s = location.address.split(',')
            country = s[s.__len__() -1 : s.__len__()][0]
            return country.strip()
        except:
            return ""
