#!/usr/bin/python
from db_conn import connect
from db_conn import close
import requests
import re

# Sample of Grocery Merchants
MERCHANTS = ['Loblaw', 'Walmart', 'Metro', 'Costco', 'Freshco', 'NoFrills', 'FoodBasics', 'Independent', 'Zehrs','ShoppersDrugMart', 'ValuMart', 'Sobeys', 'IGA']
# Central Postal Code in Ottawa
LOCATION = ['K1P1J1']

# Initialize product list
product_list = []

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
                product_name = i['name'].upper()
                merchant = i['merchant_name'].upper()
                sale_price = i['current_price']
                price_units = i['post_price_text']
                start_date = i['valid_from']
                end_date = i['valid_to']

                # add each row to product list for insert
                product_list.append((price_units, start_date, sale_price, product_name, merchant, end_date))

def insert_data(cursor, connection, products):
    # execute insert statement
    cursor.executemany("INSERT INTO flyer_item VALUES(%s,%s,%s,%s,%s,%s)", products)
    # commit the changes to db
    connection.commit()

if __name__ == "__main__":
    # gather data, connect to db, insert data, terminate db connection
    get_data()
    cursor, connection = connect()
    insert_data(cursor, connection, product_list)
    close(cursor, connection)
