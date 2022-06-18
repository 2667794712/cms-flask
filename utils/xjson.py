from flask import jsonify


class StatusCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500


def json_result(code, message, data):
    return jsonify({"code": code, "message": message, "data": data or {}})
