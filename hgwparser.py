from pyquery import PyQuery as pq
import IParser
from geopy.geocoders import Nominatim
# address, rating, country, food_type, name, price


class HgwParser(IParser.IParser):
    def __init__(self, content, url):
        self.doc = pq(content)

    def is_review(self):
        #res = self.doc("meta[itemprop='priceRange'], meta[itemprop='name'], span[itemprop='address']")
        return self.doc(".module-ibl-summary").size() > 0
        # res = self.doc("meta[property='og:type']")
        # for i in range(0, res.size()):
        #    if res.attr("content") == "hungrygowhere:restaurant":
        #        return True
        # return False

    def extract_price(self):
        # res1 = (self.doc(".module-information meta[itemprop='priceRange']").next())("div[class='inner']")
        res1 = (self.doc("meta[itemprop='priceRange']").next())
        innertexts = res1.text().split()
        if innertexts.__len__() > 0 and innertexts[2][0] == '$':
            price = innertexts[2].split('$')
            if price.__len__() > 1:
                return float(price[1])

    def extract_foodtypes(self):
        resstring = ''
        res1 = self.doc("span[itemprop='servesCuisine']")
        for i in range(0, res1.size()):
            resstring += pq(res1[i]).text()
            if i + 1 < res1.size():
                resstring += ','
        return resstring

    def extract_address(self):
        res = self.doc(".address[itemprop='address']").remove('script, a').text()
        return res
        # return self.doc(".module-information .address .inner span[itemprop='streetAddress']").attr('title')

    def extract_food_title(self):
        res = self.doc("meta[itemprop='name']")
        return res.attr("content")
        # return self.doc("h1[class='rs-regular-sm']").prev().attr("content")

    def extract_numvote(self):
        res = self.doc(".module-ibl-summary meta[itemprop='ratingValue']")
        vote = res.attr("content")
        res1 = self.doc("meta[itemprop='ratingCount']")
        numvoter = res1.attr("content")
        try:
            vote = float(vote) / 5.0
            numvoter = int(numvoter)
        except:
            return 0.0, 0
        return vote, numvoter

    def extract_country(self):
        try:
            geolocator = Nominatim()
            latitude = self.doc("meta[itemprop='latitude']").attr("content")
            longtitude = self.doc("meta[itemprop='longitude']").attr("content")
            location = geolocator.reverse(latitude + ', ' + longtitude)
            s = location.address.split(',')
            country = s[s.__len__() - 1: s.__len__()][0]
            return country.strip()
        except:
            return ""
