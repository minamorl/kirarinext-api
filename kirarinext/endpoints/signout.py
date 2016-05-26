from flask import Blueprint, request, session

from ..libs.response import *

api = Blueprint("signout", __name__)


@api.route("/api/signout")
def signout_get():
    session.clear()
    return ok()
