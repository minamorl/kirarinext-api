from flask import Flask, request, jsonify, session
import datetime
import os
import dotenv
import hashlib
import random
import re

from libs import p
from libs.response import *
from libs.models import *
from libs.auth import *
from libs.misc import *

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.permanent_session_lifetime = datetime.timedelta(days=7)



@app.before_request
def before_request():
    session.permanent = True


@app.route("/api/comments", methods=["POST"])
def comment():
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
def thread():
    """returns latest 50 comments"""
    thread_name = "$DEFAULT"
    thread = find_thread(thread_name)
    comments = find_comments(thread, request.args.get("from"))
    results = [comment_to_json(comment) for comment in comments]
    return json({
        "auth": is_signed_in(),
        "comments": results
    })

def is_signed_in():
    return session.get("username") is not None

@app.route("/api/users", methods=["POST"])
def signin():
    username = request.json.get("username")
    password = request.json.get("password")

    if not is_valid_username(username):
        return json({
            "auth": False
        })

    user = p.find_by(User, "username", username)

    if user is None:
        User(username=username, password=hashed_password(password), avatar_url=pick_author_image())
        p.save(user)
    else:
        if user.password != hashed_password(password):
            return json({
                "auth": False
            })

    session['username'] = username
    print(session)
    return json({
        "auth": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "avatar_url": user.avatar_url,
        }
    })


@app.route("/api/signout")
def signout():
    session.clear()
    return ok()


@app.route("/api/account_settings", methods=["POST"])
def account_settings():
    username = session.get("username")
    if username is None:
        return error("User is not authed")
    if request.json.get("update_icon"):
        user = p.find_by(User, "username", username)
        user.avatar_url = pick_author_image()
        p.save(user)

    return json({
        "auth": str(True),
        "user": {
            "id": user.id,
            "username": user.username,
            "avatar_url": user.avatar_url,
        }
    })


def main():
    app.run(port=9010, debug=True)

if __name__ == '__main__':
    main()
