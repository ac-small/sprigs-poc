from textblob.classifiers import NaiveBayesClassifier
import requests
import re

# Sample of Grocery Merchants
MERCHANTS = ['Loblaw', 'Walmart', 'Metro', 'Costco', 'Freshco', 'NoFrills', 'FoodBasics', 'Independent', 'Zehrs','ShoppersDrugMart', 'ValuMart', 'Sobeys', 'IGA']
# Random Sample of locations across Ontario
LOCATION = ['K1G5P9','N2M2B3', 'L1E2B4']

def get_flyer_data(location, merchant):
    req = requests.get('https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code='+ location +'&q=' + merchant)
    res = req.json()['items']
    return res

def open_file_write_headers():
    f = open("results.tsv", "a", encoding="utf-8")
    f.write("Merchant" + "\t" + "Flyer Item" + "\t" + "Price" + "\t" + " Classification Result" + "\t" + " Prediction Confidence"  + "\n")
    return f

def close_file(file):
    file.close()

def test(test, file):
    for i in test:
        product = i['name'].upper()
        price = i['current_price']
        merchant = i['merchant_name']

        '''Only classify products that are priced per weight (pounds / kilos)
           This will help eliminate many products that are non-meats or prepackaged'''

        if i['post_price_text'] != None:
            units = i['post_price_text'].lower()
            if re.search('lb|kg$', units):
                full_price = str(price) + str(units)
            else:
                full_price = None
        else:
            full_price = None

        ''' Run classification, check accuracy, produce report'''

        if full_price != None:
                result = cl.classify(product)
                accuracy = cl.prob_classify(product)
                file.write(str(merchant) + '\t' +str(product) + "\t" + str(full_price) + "\t" + str(result) + "\t" + str(accuracy.prob(result)) + "\n")

if __name__ == "__main__":
    # Train the model and split into appropriate meat categories.
    with open('Data//broad_classifications.json', 'r') as fp:
        cl = NaiveBayesClassifier(fp, format="json")

    # Open Results File
    file = open_file_write_headers()

    # Test the model
    for loc in LOCATION:
        for mer in MERCHANTS:
            data = get_flyer_data(loc,mer)
            test(data, file)

    # Close the File        
    close_file(file)
