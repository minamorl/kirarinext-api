from flask import Blueprint, request, session

from ..libs import p
from ..libs.response import *
from ..libs.models import *
from ..libs.auth import *
from ..libs.misc import *



api = Blueprint("favorites", __name__)

@api.route("/api/favorites/<comment_id>", methods=["POST"])
def favorites_post(comment_id):
    user = p.find_by(User, "username", session.get("username"))
    if user is None:
        return error("Authorization failed.")
    favorites = p.load_all(Favorite)
    for f in favorites:
        if f.comment_id == str(comment_id) and f.user_id == str(user.id):
            return ok()
    p.save(Favorite(user_id=user.id, comment_id=comment_id))
    return ok()

@api.route("/api/favorites/<comment_id>", methods=["DELETE"])
def favorites_delete(comment_id):
    user = p.find_by(User, "username", session.get("username"))
    if user is None:
        return error("Authorization failed.")
    favorites = p.load_all(Favorite)
    for f in favorites:
        if f.comment_id == str(comment_id) and f.user_id == str(user.id):
            p.delete(f)
            return ok()
    return ok()
