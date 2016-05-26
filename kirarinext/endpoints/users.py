from flask import Blueprint, request, session

from ..libs import p
from ..libs.response import *
from ..libs.models import *
from ..libs.auth import *
from ..libs.misc import *

api = Blueprint("users", __name__)

@api.route("/api/users", methods=["POST"])
def users_post():
    username = request.json.get("username")
    password = request.json.get("password")

    if not is_valid_username(username):
        return error("Username must be 3-12 characters.")

    user = p.find_by(User, "username", username)

    if user is None:
        User(username=username, password=hash_password(password),
             avatar_url=pick_author_image(), screen_name=username)
        p.save(user)
    else:
        if user.password != hash_password(password):
            return error("Username or password is incorrect.")

    session['username'] = username
    print(session)
    return json_response()


