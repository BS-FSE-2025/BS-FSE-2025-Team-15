import urllib.parse
import requests




api_key = "8dd997da83a84f2ea766746331ee9307"
def verify_location(address):
    try:

        encoded_address = urllib.parse.quote(address)
        url = f"https://api.geoapify.com/v1/geocode/search?text={encoded_address}&lang:he&filter=countrycode:il&apiKey={api_key}"

        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)

        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            if data.get('features') and len(data['features']) > 0:
                location = data['features'][0]['properties']
                city = location.get('city')
                return {
                    'success': True,
                    'city': city,
                    'latitude': location['lat'],
                    'longitude': location['lon'],
                    'formatted_address': location.get('formatted', address)
                }
            else:
                return {
                    'success': False,
                    'error': 'Address not found'
                }
        else:
            return {
                'success': False,
                'error': f'API Error: {response.status_code}'
            }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def calculate_street_distance(lat1, lon1, lat2, lon2):
    try:
        url = f"https://api.geoapify.com/v1/routing?waypoints={lat1},{lon1}|{lat2},{lon2}&mode=drive&apiKey={api_key}"

        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        distance = data['features'][0]['properties']['distance'] / 1000
        return round(distance, 2)

    except Exception as e:
        print(e)


def sort_pharmacies_by_distance(pharmacies):
    return sorted(pharmacies, key=lambda x: x['distance'])
