import mysql.connector

TABLES = dict()

TABLES['restaurants'] = (
    "CREATE TABLE `restaurants` ("
    "  `restaurant_id` INT PRIMARY KEY AUTO_INCREMENT,"
    "  `restaurant_name` varchar(64) NOT NULL,"
    "  `country` varchar(64),"
    "  `web_rating` FLOAT,"
    "  `address` varchar(128),"
    "  `average_price` FLOAT,"
    "  `food_type` VARCHAR(256),"
    "  `source_website` varchar(256)"
    ") ENGINE=InnoDB")

TABLES['food_type_id'] = (
    "CREATE TABLE `food_type_id` ("
    "   `id` INT PRIMARY KEY, "
    "   `food_type` VARCHAR(32) "
    ") ENGINE=InnoDB"
)

TABLES['restaurant_food_type'] = (
    "CREATE TABLE `restaurant_food_type` ("
    "   `id` INT PRIMARY KEY, "
    "   `food_type` VARCHAR(32) "
    ") ENGINE=InnoDB"
)


# Clear tables and reset db
def reset_db(cursor):
    for name, ddl in TABLES.iteritems():
        try:
            print "Creating table {}: ".format(name)
            cursor.execute('DROP TABLE {}'.format(name))
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")


def init_db(reset=False):
    conn = mysql.connector.connect(user='foodfinder', password='foodfinder',
                                   host='127.0.0.1',
                                   database='foodfinder')

    cursor = conn.cursor(prepared=True)
    if reset:
        reset_db(cursor)

    return cursor, conn


def close_db(conn, cursor):
    cursor.close()
    conn.close()


def standard_clean_name(inString):
    inString = inString.lower()
    inString = ','.join([x.strip() for x in inString.split(',')])

    return inString

def insert_restaurant_batch(restaurantList):

    # name="-", country="-", rating=0.0, address="-", averagePrice=0.0, foodType='', sourceSite="-"

    cursor, conn = init_db()
    query = 'SELECT MAX(restaurant_id) FROM restaurants'
    cursor.execute(query)

    nextRestaurantId = 0
    for (lastRestaurantId,) in cursor:
        # should only contain 1 row
        if lastRestaurantId is None:
            break
        nextRestaurantId = lastRestaurantId + 1

    for restaurant in restaurantList:
        name = restaurant['name']
        country = restaurant['country']
        rating = restaurant['rating']
        address = restaurant['address']
        averagePrice = restaurant['averagePrice']
        sourceSite = restaurant['sourceSite']
        foodType = restaurant['foodType']
        country = standard_clean_name(country)
        foodType = standard_clean_name(foodType)

        insertStatement = 'INSERT INTO restaurants (restaurant_id, restaurant_name, country, web_rating, address, average_price, ' \
                          'source_website, food_type)' \
                          ' VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(insertStatement, (name, country, rating, address, averagePrice, sourceSite, foodType))

    cursor.close()
    conn.commit()
    conn.close()


def insert_restaurant(name="-", country="-", rating=0.0, address="-", averagePrice=0.0, foodType='', sourceSite="-"):
    cursor, conn = init_db()
    query = 'SELECT MAX(restaurant_id) FROM restaurants'
    cursor.execute(query)

    nextRestaurantId = 0
    for (lastRestaurantId,) in cursor:
        # should only contain 1 row
        if lastRestaurantId is None:
            break
        nextRestaurantId = lastRestaurantId + 1

    country = standard_clean_name(country)
    foodType = standard_clean_name(foodType)

    insertStatement = 'INSERT INTO restaurants (restaurant_id, restaurant_name, country, web_rating, address, average_price, ' \
                      'source_website, food_type)' \
                      ' VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)'

    cursor.execute(insertStatement, (name, country, rating, address, averagePrice, sourceSite, foodType))
    cursor.close()
    conn.commit()
    conn.close()



def db_test():
    cursor, conn = init_db(True)
    close_db(conn, cursor)
    insert_restaurant_batch([{'name':'btest', 'country':'c1', 'rating':0.5, 'address':'here',
                              'averagePrice':222, 'sourceSite':'www.google.com', 'foodType':'japanese,korean'},
                             {'name': 'WHAT', 'country': 'c2', 'rating': 0.5, 'address': 'here',
                              'averagePrice': 222, 'sourceSite': 'www.google.com', 'foodType': 'japanese,korean'}
                             ])
    # insert_restaurant("haha", "sg", 5, "aaa", 0.5, "foodone, foodtwo a ", "www.google.com")
    # insert_restaurant("haha2", "sg", 5, "aaa", 0.5, "kkk", "www.google.com")


if __name__ == '__main__':
    db_test()
