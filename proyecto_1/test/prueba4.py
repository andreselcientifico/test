import requests

API_KEY = "AIzaSyD0txU5n7xlPZ3zkEsEjW09yVHmmEVjU4o"
address = "calle 23 # 22-40, agustin codazzi"

base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
params = {"key": API_KEY, "address": address}

response = requests.get(base_url, params=params).json()
response.keys()

if response['status'] == 'OK':
    location = response["results"][0]["geometry"]
    print(location)
    latitude = location['location']['lat']
    longitude = location['location']['lng']
else:
    print(response['text'])
    raise Exception("Error in geocoding request")

print(f"Latitude: {latitude}")
print(f"Longitude: {longitude}")