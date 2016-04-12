from flask import jsonify

def json(obj):
    """ just wraps jsonify """
    return jsonify(results=obj)


def ok():
    return json({
        "message": "ok"
    })


def error(msg):
    return json({
        "message": msg
    })
