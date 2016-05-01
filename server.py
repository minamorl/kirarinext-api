from redisorm.core import Persistent
from flask import Flask, request, jsonify
import datetime

from libs.response import *
from libs.models import *

app = Flask(__name__)

p = Persistent("kirarinext")


def find_comments(thread, fetch_from=None):
    if fetch_from is not None:
        max_id = p.get_max_id(Comment)
        if max_id is None:
            return []
        ids = range(int(fetch_from) + 1, max_id + 1)
        return [p.load(Comment, _id) for _id in ids]


    return [comment for comment in p.load_all(Comment)
            if comment.thread == thread.name]


def find_thread(thread_name, ensure_exists=True):
    thread = p.find(Thread, lambda thread: thread.name == thread_name) or Thread(name=thread_name)
    if ensure_exists:
        p.save(thread)  # ensure thread is existing on database.
    return thread


@app.route("/api/comments", methods=["POST"])
def comment():
    body = request.json.get("body")
    thread = "$DEFAULT"
    if len(body) > 1000:
        return error("comment must be less than 10000 characters.")
    if body == "":
        return error("comment cannot be empty.")

    comment = Comment(
        body=body, thread=thread, author="anonymous",
        remote_addr=request.environ.get("HTTP_X_REAL_IP"),
        created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    p.save(comment)

    idhash = generate_hash(comment.remote_addr)
    user = p.find_by(Anonymous, "remote_addr", comment.remote_addr) or Anonymous(avatar_url=pick_author_image(), remote_addr=comment.remote_addr)
    p.save(user)

    return ok()


@app.route("/api/comments", methods=["GET"])
def thread():
    thread_name = "$DEFAULT"
    thread = find_thread(thread_name)
    comments = find_comments(thread, request.args.get("from"))
    results = [comment_to_json(comment) for comment in comments]
    return json(results)


def generate_hash(string):
    import hashlib
    import random

    return hashlib.sha1((string or str(random.random())).encode("UTF-8")).hexdigest()[:10]


def pick_author_image():
    import random
    img = random.randrange(0, 12)

    return "./img/{0:03d}.jpeg".format(img)


def comment_to_json(comment):
    idhash = generate_hash(comment.remote_addr)
    user = None
    user = p.find_by(Anonymous, "remote_addr", comment.remote_addr) or Anonymous(avatar_url=pick_author_image(), remote_addr=comment.remote_addr)
    p.save(user)
    return {
        "author": {
            "name": comment.author,
            "id": idhash,
            "avatar": user.avatar_url,
        },
        "body": comment.body,
        "created_at": comment.created_at or "有史以前",
        "id": comment.id,
        "thread": {
            "name": comment.body
        }
    }


def main():
    app.run(port=9010, debug=True)

if __name__ == '__main__':
    main()
