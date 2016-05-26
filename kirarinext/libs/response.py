from flask import jsonify, session
from .misc import is_signed_in
from . import p
from .models import *

def json_response(obj=None):
    """ just wraps jsonify """
    if obj is None:
        obj = {}
    return jsonify(results={
        **obj,
        **authorization_details(),
    })


def ok():
    return json_response({
        "message": "ok"
    })


def error(msg):
    return json_response({
        "message": msg
    })


def authorization_details():
    user = p.find_by(User, "username", session.get("username"))
    if is_signed_in():
        return {
            "auth": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "avatar_url": user.avatar_url,
                "screen_name": user.screen_name,
            }
        }
    return {
        "auth": False
    }
