import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions,  ClassificationsOptions



# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, api_key=False, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    if api_key:
        try:
            requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        except:
            print("Network exception occurred")
    else:
        try:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
        except:
            # If any error occurs
            print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    json_obj = json_payload['review']
    print(kwargs)
    try:
        response = requests.post(url, json=json_obj, params=kwargs)
    except:
        print("Error")
    print( response)
    return response


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results

def get_dealers_by_state(url, state):
    results=[]
    json_result = get_request(url, state=state)
    dealers =json_result['dealerships']

    for dealer in dealers:    
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
        results.append(dealer_obj)

    return results

def get_dealers_by_id(url, id):
    results=[]
    json_result = get_request(url, id=id)
    dealers =json_result['dealerships']
    
    for dealer in dealers:    
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
        results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, dealer_id):
    results=[]
    json_result = get_request(url, dealership=dealer_id)
    reviews =json_result['reviews']

    for review in reviews:    
        review_obj = DealerReview(dealership=review['dealership'], name=review['name'], purchase=review['purchase'], review=review['review'], purchase_date=review['purchase_date'], car_make=review['car_make'], car_model=review['car_model'], car_year=review['car_year'], id=review['id'], sentiment=analyze_review_sentiments(review['review']))
        results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    api_key = "uqDX6SaM0g9hzdzNlW-zjgymn_wHm96JbXBEoObAfNzn"
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/b9d9806b-52d5-47e1-af3c-e21cc26ba4ec"

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(url)

    response = natural_language_understanding.analyze(
        url='www.ibm.com',
        features=Features(sentiment= SentimentOptions())).get_result()

    sentiment_score = str(response["sentiment"]["document"]["score"])
    sentiment_label = response["sentiment"]["document"]["label"]

    sentimentresult = sentiment_label
    
    return sentimentresult


