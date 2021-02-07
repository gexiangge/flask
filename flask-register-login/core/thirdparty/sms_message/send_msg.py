# @Time    : 2020-11-07 12:05
# @Author  : 老赵
# @File    : send_msg.py


import requests


def send_mobile_msg(phone_number, msg):
    try:
        response = requests.get(
            url="http://114.255.71.158:8061/",
            params={
                "username": "hcsslssg1",
                "password": "9b26a1f92ffaa6sdsdsdsd23972876b9",
                "phone": phone_number,
                "epid": 126294,
                "message": msg,
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
