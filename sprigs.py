#!/usr/bin/python
from db_conn import connect
from db_conn import close
import requests
import re

# Sample of Grocery Merchants
MERCHANTS = ['Loblaw', 'Walmart', 'Metro', 'Costco', 'Freshco', 'NoFrills', 'FoodBasics', 'Independent', 'Zehrs','ShoppersDrugMart', 'ValuMart', 'Sobeys', 'IGA']
# Central Postal Code in Ottawa
LOCATION = ['K1P1J1']

# Initialize variables
product_list = []
classification_list = []
global data

def flipp_request(location, merchant):
    req = requests.get('https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code='+ location + '&radius=50km' + '&q=' + merchant)
    res = req.json()['items']
    return res

def get_data():
    # retrieve flyer data
    for loc in LOCATION:
        for mer in MERCHANTS:
            data = flipp_request(loc,mer)

            # loop over data, format, and extract values of interest
            for i in data:
                flyer_id = i['flyer_item_id']
                product_name = i['name'].upper()
                merchant = i['merchant_name'].upper()
                sale_price = i['current_price']
                price_units = i['post_price_text']
                start_date = i['valid_from']
                end_date = i['valid_to']

                # add each row to product list for insert
                product_list.append((price_units, start_date, sale_price, product_name, merchant, end_date, flyer_id))

def broad_category_classify():
    for i in product_list:
        name = i[3]
        flyer_id = i[6]

        if "CHICKEN" in name:
            add_classification(flyer_id, "CHICKEN")
        if "TURKEY" in name:
            add_classification(flyer_id, "TURKEY")
        if "DUCK" in name:
            add_classification(flyer_id, "DUCK")
        else:
            add_classification(flyer_id, None)

def add_classification(flyer_id, classification_string):
    classification_list.append((flyer_id, classification_string))

def insert_data(cursor, connection, products, classifications):
    # execute and commit insert statements
    cursor.executemany("INSERT INTO flyer_item (price_units, start_date, sale_price, product_name, merchant, end_date, flyer_id) VALUES(%s,%s,%s,%s,%s,%s,%s)", products)
    connection.commit()
    cursor.executemany("INSERT INTO classification VALUES(%s,%s)", classifications)
    connection.commit()

if __name__ == "__main__":
    # gather data, connect to db, insert data, terminate db connection
    get_data()
    broad_category_classify()
    cursor, connection = connect()
    insert_data(cursor, connection, product_list, classification_list)
    close(cursor, connection)
