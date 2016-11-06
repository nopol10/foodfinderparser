from pyquery import PyQuery as pq
import IParser
from geopy.geocoders import Nominatim
# address, rating, country, food_type, name, price


class TripAdvParser(IParser.IParser):
    def __init__(self, content, url):
        self.doc = pq(content)

    def is_review(self):
        res = self.doc("h3[class='tabs_header']")
        for i in range(0, res.size()):
            if pq(res[i]).text() == "Restaurant Details":
                return True
        return False

    def extract_price(self):
        return -1.0

    def extract_foodtypes(self):
        resstring = ''
        res = self.doc("div[class='title']")
        for i in range(0, res.size()):
            sub = pq(res[i])
            if sub.text() == "Cuisine":
                resstring = sub.next().text()
                break
        return resstring

    def extract_address(self):
        res = self.doc("div[class='detail'] span[class='format_address']").text()
        return res
        # return self.doc(".module-information .address .inner span[itemprop='streetAddress']").attr('title')

    def extract_food_title(self):
        res = self.doc("h1[property='name']")
        return res.text()
        # return self.doc("h1[class='rs-regular-sm']").prev().attr("content")

    def extract_numvote(self):
        maxrating = 4
        vote = 0
        numvoter = 0

        try:
            res = self.doc("div[class='colTitle']")
            for i in range(0, res.size()):
                sub = pq(res[i])
                if sub.text() == "Traveller rating":
                    sub = sub.next()
                    ratings = sub("li")
                    for j in range(0, ratings.size()):
                        split = pq(ratings[j]).text().split()
                        index = 2 if j == 1 else 1
                        num = (int)(split[index])
                        numvoter += num
                        vote += (maxrating - j) * num
                    break


            vote = (float(vote)/numvoter)/4.0
            vote = round(vote,2)
        except:
            return -1.0, -1
        return vote, numvoter

    def extract_country(self):
        res = self.doc("span[class='country-name']")
        country = ""
        for i in range(0, res.size()):
            sub = pq(res[i])
            country = sub.text() if sub.text() != "" else sub.attr("content")
            if country != "":
                break
        return country
