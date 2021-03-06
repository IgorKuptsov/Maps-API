import math
import sys
from io import BytesIO
import requests


def open_image(ll, z, file_name, points=[], mode='map'):
    # рисует карту и точку на ней
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": ll,
        "z": z,
        "l": mode,
        "size": '450,450'
    }
    # print(points)
    if points:
        map_params['pt'] = '~'.join(points)
    response = requests.get(map_api_server, params=map_params)
    # print(response.url)
    if response:
        map_file = file_name
        with open(map_file, "wb") as file:
            file.write(response.content)
    else:
        print(response.status_code, response.reason, response.url)


def geocode(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        raise RuntimeError(f'Ошибка выполнения запроса:\n' \
                           f'{response.url}\n' \
                           f'Статус: {response.status_code} {response.reason}')
    data = response.json()
    features = data["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


def get_coordinates(address):
    toponym = geocode(address)
    if toponym is None:
        return None, None
    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def get_longlat(address):
    toponym = geocode(address)
    if toponym is None:
        return None, None, None
    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")
    ll = ','.join([toponym_longitude, toponym_lattitude])
    address = toponym['metaDataProperty']['GeocoderMetaData']['Address']
    return ll, address


def find_businesses(place, ll, spn, locale='ru_RU', type='biz'):
    search_api_server = "https://search-maps.yandex.ru/v1/"

    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": place,
        "lang": locale,
        "ll": ll,
        'spn': spn,
        "type": type
    }
    response = requests.get(search_api_server, params=search_params)

    if not response:
        raise RuntimeError(f'Ошибка выполнения запроса:\n' \
                           f'{response.url}\n' \
                           f'Статус: {response.status_code} {response.reason}')
    data = response.json()
    features = data["features"]
    return features


def find_business(place, ll, spn, locale='ru_RU', type='biz'):
    orgs = find_businesses(place, ll, spn, locale, type)
    if orgs:
        return orgs[0]


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_long, a_lat = a
    b_long, b_lat = b

    radiance_lattitude = math.radians((a_lat + b_lat) / 2)
    lat_lon_factor = math.cos(radiance_lattitude)

    dx = abs(a_long - b_long) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx ** 2 + dy ** 2)

    return distance


def in_50_metres_range(ll, businesses):
    for business in businesses:
        business_ll = business['geometry']['coordinates']
        if lonlat_distance(ll, business_ll) <= 50:
            closest = business
            return closest['properties']['name'], business_ll
    return None

# open_image("37.620070,55.753630", '0.005,0.005', "1", 'image.jpeg', mode="map")