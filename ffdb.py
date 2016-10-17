import mysql.connector

TABLES = dict()

TABLES['restaurants'] = (
    "CREATE TABLE `restaurants` ("
    "  `restaurant_id` INT PRIMARY KEY,"
    "  `restaurant_name` varchar(64) NOT NULL,"
    "  `country` varchar(64),"
    "  `web_rating` FLOAT,"
    "  `address` varchar(128),"
    "  `average_price` FLOAT,"
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


def reset_db(cursor):
    for name, ddl in TABLES.iteritems():
        try:
            print "Creating table {}: ".format(name)
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


def standard_clean_name(str):
    str = str.lower()

    return str

def insert_restaurant(name="-", country="-", rating=0.0, address="-", averagePrice=0.0, foodType='', sourceSite="-"):
    cursor, conn = init_db()
    query = 'SELECT MAX(restaurant_id) FROM restaurants'
    cursor.execute(query)

    nextRestaurantId = 0
    for (lastRestaurantId) in cursor:
        # should only contain 1 row
        nextRestaurantId = lastRestaurantId + 1

    insertStatement = 'INSERT INTO restaurants (restaurant_name, country, web_rating, address, average_price, ' \
                      'source_website)' \
                      ' VALUES (%s, $s, %s, $s, %s, $s)'

    cursor.execute(insertStatement, (name, country, rating, address, averagePrice, sourceSite))

    # TODO Process food type



if __name__ == '__main__':
    init_db(True)

    print 'hi'
