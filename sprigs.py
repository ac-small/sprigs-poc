#!/usr/bin/python
import psycopg2
from config import config
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


def db_insert(products):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()
        
        # execute insert statement
        cur.executemany("INSERT INTO flyer_item VALUES(%s,%s,%s,%s,%s,%s)", products)

        # commit the changes to db
        conn.commit()
       
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == "__main__":
    get_data()
    db_insert(product_list)
