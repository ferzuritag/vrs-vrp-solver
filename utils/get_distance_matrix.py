import requests

def toCoordinatesPair(location: dict):
    return [location['latitude'], location['longitude']]

def get_distance_matrix(locations):
    # Prepare list of coordinate pairs
    coordinate_pairs = list(map(toCoordinatesPair, locations))
    
    # Set up the request
    url = 'https://api.openrouteservice.org/v2/matrix/driving-car'
    headers = {
        'Authorization': '5b3ce3597851110001cf6248cc7a57e8fa7149f0b6ffbbe447831a5c'
    }
    payload = {
        'locations': coordinate_pairs
    }

    # Make the POST request
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return [[int(element) for element in row] for row in data['durations']]
    else:
        return []
