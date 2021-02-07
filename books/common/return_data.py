from flask import jsonify


def compose_return_data(data, code, msg):
    _return = {
        "data": data,
        "code": code,
        "msg": msg
    }

    return jsonify(_return)