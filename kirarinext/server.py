from flask import Flask, request, jsonify, session
import datetime
import os
import dotenv
import hashlib
import random
import re

from .libs import p
from .libs.response import *
from .libs.models import *
from .libs.auth import *
from .libs.misc import *


app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.permanent_session_lifetime = datetime.timedelta(days=7)


@app.before_request
def before_request():
    session.permanent = True


@app.route("/api/comments", methods=["POST"])
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


@app.route("/api/comments", methods=["GET"])
def comments_get():
    """returns latest 50 comments"""
    thread_name = "$DEFAULT"
    thread = find_thread(thread_name)
    comments = find_comments(thread, request.args.get("from"))
    results = [comment_to_json(comment) for comment in comments]
    return json_response({
        "comments": results,
    })


@app.route("/api/users", methods=["POST"])
def users_post():
    username = request.json.get("username")
    password = request.json.get("password")

    if not is_valid_username(username):
        return error("Username must be 3-12 characters.")

    user = p.find_by(User, "username", username)

    if user is None:
        User(username=username, password=hashed_password(password),
             avatar_url=pick_author_image(), screen_name=username)
        p.save(user)
    else:
        if user.password != hashed_password(password):
            return error("Username or password is incorrect.")

    session['username'] = username
    print(session)
    return json_response()


@app.route("/api/signout")
def signout_get():
    session.clear()
    return ok()


@app.route("/api/account_settings", methods=["POST"])
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
        user.password = hashed_password(requeit.json.get("password"))
        p.save(user)

    return json_response()
