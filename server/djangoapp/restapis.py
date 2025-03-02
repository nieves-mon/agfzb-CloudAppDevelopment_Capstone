import requests
import json
from .models import CarDealer, DealerReview, CarModel
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
	print(kwargs)
	print("GET from {} ".format(url))
	try:
		# Call get method of requests library with URL and parameters
		response = requests.get(
			url, headers={'Content-Type': 'application/json'}, params=kwargs)
		status_code = response.status_code
		print("With status {} ".format(status_code))
		json_data = json.loads(response.text)
		return json_data
	except:
		# If any error occurs
		print("Network exception occurred")
	
	return


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
	print("Payload: ", json_payload, ". Params: ", kwargs)
	print(f"POST {url}")
	try:
		response = requests.post(url, headers={'Content-Type': 'application/json'},
															json=json_payload, params=kwargs)
	except:
		# If any error occurs
		print("Network exception occurred")
	status_code = response.status_code
	print("With status {} ".format(status_code))
	json_data = json.loads(response.text)
	return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
	results = []
	# Call get_request with a URL parameter
	json_result = get_request(url)
	print(json_result)
	if json_result:
		# Get the row list in JSON as dealers
		dealers = json_result
		
		# For each dealer object
		for dealer in dealers:
			# Get its content in `doc` object
			dealer_doc = dealer
			print("Dealer",dealer_doc)
			# Create a CarDealer object with values in `doc` object
			dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
															id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
															short_name=dealer_doc["short_name"],
															st=dealer_doc["st"], zip=dealer_doc["zip"])
			results.append(dealer_obj)

	return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
	results = []
	# Call get_request with a URL parameter
	reviews = get_request(url)
	print(reviews)

	if reviews:
		# For each dealer object
		for review_doc in reviews:
			if review_doc["purchase"]:
				review_obj = DealerReview(
					dealership=review_doc["dealership"],
					name=review_doc["name"],
					purchase=review_doc["purchase"],
					review=review_doc["review"],
					purchase_date=review_doc["purchase_date"],
					car_make=review_doc["car_make"],
					car_model=review_doc["car_model"],
					car_year=review_doc["car_year"],
					sentiment=analyze_review_sentiments(review_doc["review"]),
					id=review_doc["id"],
				)
				results.append(review_obj)
	return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
	url = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/7250d85b-153d-4cec-a2de-8014ff4e59f2'

	params = json.dumps({"text": text, "features": {"sentiment": {}}})
	response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', 'SPw5aAcvMxCugr2YomHe3Q0pVPIssx4yvK5Pp_4ZOV5F'))

	try:
			return response.json()['sentiment']['document']['label']
	except KeyError:
			return 'neutral'
