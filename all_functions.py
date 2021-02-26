import math
import sys
from io import BytesIO
import requests


def open_image(ll, spn, file_name, points=[], mode='map'):
    # рисует карту и точку на ней
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": mode,
        "size": '450,450'
    }
    # print(points)
    if points:
        map_params['pt'] = '~'.join(points)
    response = requests.get(map_api_server, params=map_params)
    if response:
        map_file = file_name
        with open(map_file, "wb") as file:
            file.write(response.content)
    else:
        print(response.status_code, response.reason)


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


def get_ll_span(address):
    toponym = geocode(address)
    if toponym is None:
        return None, None, None
    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")
    ll = ','.join([toponym_longitude, toponym_lattitude])

    envelope = toponym['boundedBy']['Envelope']
    left, bottom = map(float, envelope['lowerCorner'].split(' '))
    right, top = map(float, envelope['upperCorner'].split(' '))

    dx = abs(left - right) / 2
    dy = abs(bottom - top) / 2

    span = f'{dx},{dy}'
    address = toponym['metaDataProperty']['GeocoderMetaData']['Address']

    return ll, span, address


def find_businesses(place, ll, spn, locale='ru_RU', type='biz'):
    # print(500)
    # print(place)
    # print(600)
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

    # print(response.status_code, response.reason)
    if not response:
        raise RuntimeError(f'Ошибка выполнения запроса:\n' \
                           f'{response.url}\n' \
                           f'Статус: {response.status_code} {response.reason}')
    data = response.json()
    # print(data)
    features = data["features"]
    # print(features)
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

    return distance  # , dx, dy


# def longtitude_offset(a, offset):
#     a_long, a_lat = a
#     degree_to_meters_factor = 111 * 1000
#     dx = degree_to_meters_factor * offset
#     ####
#     radiance_lattitude = math.radians(a_lat)
#     lat_lon_factor = math.cos(radiance_lattitude)
#     b_long = -(dx / degree_to_meters_factor / lat_lon_factor) + a_long
#     return b_long, a_lat

def in_50_metres_range(ll, businesses):
    for business in businesses:
        business_ll = business['geometry']['coordinates']
        if lonlat_distance(ll, business_ll) <= 50:
            closest = business
            return closest['properties']['name'], business_ll
    return None




# a = 92.888549, 56.009220
# b = 92.885234, 56.009220
# print(lonlat_distance(a, b))
# print(longtitude_offset(a, 0.001 / 600 * 50))
# 61.668793, 50.836497
# 62.027216, 129.732178
# print(find_businesses('стрижка', '92.888549,56.00922', '0.0015,0.0015'))
# print(find_business('Тверской район, Центральный административный округ, Москва, Россия', '37.617734,55.751999', '0.015,0.015', type='geo'))
