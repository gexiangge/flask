# @Time    : 2020-11-07 11:58
# @Author  : 老赵
# @File    : send_message.py


"""
Feature: #Enter feature name here
# Enter feature description here

Scenario: #Enter scenario name here
# Enter steps here

Test File Location: # Enter
"""

# Install the Python Requests library:
# `pip install requests`
"""
JSM40481-0029

模版内容：您的验证码是@1@，在@2@分钟内使用，为保障您的账户安全，请勿将此验证码短信转发给他人。如非本人操作请忽略。"""

import requests


# MSG_TEMPID = 'JSM40481-0041'

def send_mobile_msg(phone_number, vercode, time, tempid='JSM40481-0029'):
    try:
        response = requests.post(
            url="http://112.74.76.186:8030/service/httpService/httpInterface.do",
            params={
                "method": "sendUtf8Msg",
            },
            headers={
                "Cookie": "JSESSIONID=1F3F5ED4EEssdsffs6FE6EBsdsd09DBE328",
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            },
            data={
                "mobile": str(phone_number),
                "password": "3serfs",
                "veryCode": "dssf3sdd",
                "content": "@1@={},@2@={}".format(vercode, 1),
                "tempid": tempid,
                "code": "utf-8",
                "msgtype": "2",
                "username": "JSM4048102",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
        return 1
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        return -1


if __name__ == '__main__':
    send_mobile_msg(18911411111, 'khasdhk', 1)
