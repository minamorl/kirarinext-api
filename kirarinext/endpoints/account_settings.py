from flask import Blueprint, request, session
import datetime

from ..libs import p
from ..libs.response import *
from ..libs.models import *
from ..libs.auth import *
from ..libs.misc import *



api = Blueprint("account_settings", __name__)

@api.route("/api/account_settings", methods=["POST"])
def account_settings_post():
    username = session.get("username")
    if is_signed_in() is False:
        return error("User is not authed")
    if request.json.get("update_icon"):
        user = p.find_by(User, "username", username)
        user.avatar_url = pick_author_image()
        p.save(user)
    if request.json.get("screen_name"):
        user = p.find_by(User, "username", username)
        user.screen_name = request.json.get("screen_name")
        p.save(user)
    if request.json.get("password"):
        user = p.find_by(User, "username", username)
        user.password = hash_password(requeit.json.get("password"))
        p.save(user)

    return json_response()
