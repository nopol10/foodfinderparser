from pyquery import PyQuery as pq
import urllib2
import ffdb as db

#address, rating, country, food_type, name, price

def check_restaurant(x, y):
    print pq(y).attr("content")


def get_page(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()

    return page.read()


def is_hungrygowhere_review(doc):
    res = doc("meta[property='og:type']")
    for i in range(0, res.size()):
        if res.attr("content") == "hungrygowhere:restaurant":
            return True
    return False

def extract_numvote(doc):
    res = doc(".number-vote")
    vote = res.text()
    vote = vote.split('%')[0]
    numvoter = res.next().text().split()[0]
    vote = float(vote) / 100
    numvoter = int(numvoter)
    return vote, numvoter


def extract_food_title(doc):
    return doc("h1").text()


def extract_address(doc):
    res1 = doc(".module-information")
    res2 = res1(".address")
    if res2.size() <= 0:
        return ""
    return pq(res2[0]).text()


def extract_foodtypes(doc):
    resstring = ''
    res1 = doc(".module-information")
    res2 = res1("span[itemprop='servesCuisine']")
    for i in range(0, res2.size()):
        resstring += pq(res2[i]).text()
        if i + 1 < res2.size():
            resstring += ','
    return resstring


def extract_price(doc):
    res1 = doc(".module-information")
    res2 = (res1("meta[itemprop='priceRange']").next())("div[class='inner']")
    innertexts = res2.text().split()
    if innertexts.__len__() > 0 and innertexts[0][0] == '$':
        price = innertexts[0].split('$')
        if price.__len__() > 1:
            return price[1]


def extract_restaurant(url):
    content = get_page(url)
    d = pq(content)
    if not is_hungrygowhere_review(d):
        return None

    foodname = extract_food_title(d)
    price = extract_price(d)
    address = extract_address(d)
    rating, numvoter = extract_numvote(d)
    types = extract_foodtypes(d)
    res = {'name': foodname, 'country' : 'Singapore', 'rating': rating, 'address': address,
            'averagePrice': int(price), 'sourceSite': url, 'foodType': types}

    return res


def extract_restaurants(urls):
    restaurants = []
    for i in range(0, urls.__len__()):
        res = extract_restaurant(urls[i])
        if res is not None:
            restaurants.append(res)
    return restaurants


def test():
    urls = ["http://www.hungrygowhere.com/singapore/arnold-s-fried-chicken-yishun/",
            "http://www.hungrygowhere.com/singapore/928_yishun_laksa/"]
    #url = "http://www.hungrygowhere.com/singapore/arnold-s-fried-chicken-yishun/"
    #url = "http://www.hungrygowhere.com/singapore/928_yishun_laksa/"

    resList = extract_restaurants(urls)
    cursor, conn = db.init_db(True)
    db.close_db(conn, cursor)
    db.insert_restaurant_batch(resList)


if __name__ == '__main__':
    test()
