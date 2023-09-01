"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import requests

API = '1kgBEwgA8T3D3zaJIRkQMO9-vXUEjbc9xOWWVHiF3rRO'
URL = 'https://8696e352-53b8-4302-bd32-5ebf2fd03a8b-bluemix.cloudantnosqldb.appdomain.cloud'
USERNAME = '2a3dac3c-7f9d-484d-84d4-716d2585a304'

DBNAME = 'reviews'

def main(params):

    try:
        authenticator = IAMAuthenticator(API)
        cloudant = CloudantV1(authenticator=authenticator)
        cloudant.set_service_url(URL)
        if 'dealership' in params:
            dealer_id = int(params["dealership"]) 
        else:
            return { "Error" : "Dealership ID missing!" }
        try:
            response = cloudant.post_find(
                db=DBNAME,
                selector = {"dealership" : {
                    "$eq" : dealer_id
                    } 
                  }
                )
            
            reviews = response.result['docs']
            return {'reviews' : reviews }
        except (requests.exceptions.RequestException, ConnectionResetError) as err:
            print("Connection error")
            return {'error2':err }

    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error1": err}


