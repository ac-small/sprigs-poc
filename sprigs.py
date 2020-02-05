from textblob.classifiers import NaiveBayesClassifier
import requests

# Sample of Grocery Merchants
MERCHANTS = ['Loblaw', 'Walmart', 'Metro', 'Costco', 'Freshco', 'NoFrills', 'FoodBasics', 'Independent']
# Random Sample of locations across Canada
LOCATION = ['K1G5P9','T5J0N3', 'B3H1A4']

def get_flyer_data(location, merchant):
    req = requests.get('https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code='+ location +'&q=' + merchant)
    res = req.json()['items']
    return res

def open_file_write_headers():
    f = open("results.tsv", "a")
    f.write("Flyer Item" + "\t" + " Classification Result" + "\t" + " Prediction Confidence"  + "\n")
    return f

def close_file(file):
    file.close()

def test(test, file):
    for i in test:
        product = i['name'].upper()
        result = cl.classify(product)
        accuracy = cl.prob_classify(product)
        file.write(str(product) + "\t" + str(result) + "\t" + str(accuracy.prob(result)) + "\n")

if __name__ == "__main__":
    # Train the model
    with open('Data//training_data.json', 'r') as fp:
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
