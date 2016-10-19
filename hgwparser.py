from pyquery import PyQuery as pq
from multiprocessing.dummy import Pool as ThreadPool
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
        return None

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
    return doc("h1[class='rs-regular-sm']").prev().attr("content")
    # return doc("h1[class='rs-regular-sm']").text()


def extract_address(doc):
    return doc(".module-information .address .inner span[itemprop='streetAddress']").attr('title')


def extract_foodtypes(doc):
    resstring = ''
    res1 = doc(".module-information span[itemprop='servesCuisine']")
    for i in range(0, res1.size()):
        resstring += pq(res1[i]).text()
        if i + 1 < res1.size():
            resstring += ','
    return resstring


def extract_price(doc):
    res1 = (doc(".module-information meta[itemprop='priceRange']").next())("div[class='inner']")
    innertexts = res1.text().split()
    if innertexts.__len__() > 0 and innertexts[0][0] == '$':
        price = innertexts[0].split('$')
        if price.__len__() > 1:
            return float(price[1])


def extract_restaurant(url):
    content = get_page(url)
    if content is None:
        return None
    d = pq(content)
    if not is_hungrygowhere_review(d):
        return None

    foodname = extract_food_title(d)
    price = extract_price(d)
    address = extract_address(d)
    rating, numvoter = extract_numvote(d)
    types = extract_foodtypes(d)
    res = {'name': foodname, 'country' : 'Singapore', 'rating': rating, 'address': address,
            'averagePrice': price, 'sourceSite': url, 'foodType': types}

    return res


def extract_restaurants(urls, numthread = 4):
    pool = ThreadPool(numthread)
    restaurants = pool.map(extract_restaurant, urls)
    pool.close()
    pool.join()
    return restaurants


def get_urls_from_file(filename):
    f = open(filename, 'r')
    urls = []
    for line in f:
        urls.append(line)
    f.close()
    return urls


def test():
    urls = get_urls_from_file('urls.txt')
    #url = "http://www.hungrygowhere.com/singapore/arnold-s-fried-chicken-yishun/"
    #url = "http://www.hungrygowhere.com/singapore/928_yishun_laksa/"

    print 'extracting from', urls.__len__(), 'urls'
    resList = extract_restaurants(urls, 100)
    cursor, conn = db.init_db(True)
    db.close_db(conn, cursor)
    print 'inserting to db..'
    # print resList
    db.insert_restaurant_batch(resList)


if __name__ == '__main__':
    test()
