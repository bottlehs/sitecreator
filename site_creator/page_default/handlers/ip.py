import requests


def get_ip_data(ip):
    response = requests.get(f'http://ip-api.com/json/{ip}')
    return response.json()