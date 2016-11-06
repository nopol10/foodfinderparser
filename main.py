
from multiprocessing.dummy import Pool as ThreadPool
import ffdb as db
import hgwparser as hgw
import zomatoparser as zomato
import  tripadvparser as tripadv
import urllib2
from urlparse import urlparse

HGWDOMAIN = "www.hungrygowhere.com"
ZOMATODOMAIN = "www.zomato.com"
TRIPADVISORDOMAIN = "www.tripadvisor.com"

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
        print "Error urlopen"
        return None

    return page.read()


def get_urls_from_file(filename):
    f = open(filename, 'r')
    urls = []
    for line in f:
        urls.append(line)
    f.close()
    return urls


def get_parser(url, content):
    host = urlparse(url).netloc

    if host == HGWDOMAIN:
        return hgw.HgwParser(content, url)
    if host == ZOMATODOMAIN:
        return zomato.ZomatoParser(content, url)
    if TRIPADVISORDOMAIN in host:
        return tripadv.TripAdvParser(content, url)

    print host, 'invalid'
    return None


def extract_restaurant(url):
    content = get_page(url)
    if content is None:
        return None

    parser = get_parser(url, content)
    if parser is None:
        return None

    if not parser.is_review():
        return None

    country = parser.extract_country()
    foodname = parser.extract_food_title()
    price = parser.extract_price()
    address = parser.extract_address()
    rating, numvoter = parser.extract_numvote()
    types = parser.extract_foodtypes()
    res = {'name': foodname, 'country' : country, 'rating': rating, 'address': address,
            'averagePrice': price, 'sourceSite': url, 'foodType': types}
    print res
    return res


def extract_restaurants(urls, numthread = 4):
    pool = ThreadPool(numthread)
    restaurants = pool.map(extract_restaurant, urls)
    pool.close()
    pool.join()
    return restaurants


def main():
    urls = get_urls_from_file('urls.txt')
    #url = "http://www.hungrygowhere.com/singapore/arnold-s-fried-chicken-yishun/"
    #url = "http://www.hungrygowhere.com/singapore/928_yishun_laksa/"

    print 'extracting from', urls.__len__(), 'urls'
    resList = extract_restaurants(urls, 100)

    cursor, conn = db.init_db(True)
    db.close_db(conn, cursor)

    print 'inserting to db..'
    db.insert_restaurant_batch(resList)


def test():
    #url = "https://www.zomato.com/vi/santa-barbara-ca/los-agaves-1-santa-barbara"
    url = "https://www.tripadvisor.com.sg/Restaurant_Review-g294265-d796940-Reviews-Summer_Pavilion-Singapore.html"
    extract_restaurant(url)

if __name__ == '__main__':
    main()
