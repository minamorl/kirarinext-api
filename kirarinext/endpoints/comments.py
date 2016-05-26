from flask import Blueprint, request, session
import datetime

from ..libs import p
from ..libs.response import *
from ..libs.models import *
from ..libs.auth import *
from ..libs.misc import *



api = Blueprint("comments", __name__)

@api.route("/api/comments", methods=["POST"])
def comments_post():
    body = request.json.get("body")
    thread = "$DEFAULT"
    if len(body) > 1000:
        return error("comment must be less than 10000 characters.")
    if body == "":
        return error("comment cannot be empty.")
    comment = Comment(
        body=body, thread=thread, author=session.get("username") or "anonymous",
        remote_addr=request.environ.get("HTTP_X_REAL_IP"),
        created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    p.save(comment)

    if not session.get("username"):
        user = p.find_by(Anonymous, "remote_addr", comment.remote_addr) or Anonymous(avatar_url=pick_author_image(), remote_addr=comment.remote_addr)
        p.save(user)

    return ok()


@api.route("/api/comments", methods=["GET"])
def comments_get():
    """returns latest 50 comments"""
    thread_name = "$DEFAULT"
    thread = find_thread(thread_name)
    comments = find_comments(thread, request.args.get("from"))
    results = [comment_to_json(comment) for comment in comments]
    return json_response({
        "comments": results,
    })
