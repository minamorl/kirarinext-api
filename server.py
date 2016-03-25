from redisorm.core import Persistent, PersistentData, Column
from flask import Flask, request, jsonify
app = Flask(__name__)

p = Persistent("kirarinext")


def json(obj):
    """ just wraps jsonify """
    return jsonify(results=obj)


def ok():
    return json({
        "message": "ok"
    })


class Thread(PersistentData):
    id = Column()
    name = Column()


class Comment(PersistentData):
    id = Column()
    body = Column()
    thread = Column()
    author = Column()


@app.route("/api/comment.json", methods=["POST"])
def comment():
    body = request.json.get("body")
    thread = "$DEFAULT"
    comment = Comment(body=body, thread=thread, author="anonymous")
    p.save(comment)
    return ok()


@app.route("/api/thread.json", methods=["GET"])
def thread():
    thread = p.find(Thread, lambda thread: thread.name == "$DEFAULT") or Thread(name="$DEFAULT")
    p.save(thread)  # ensure thread is existing on database.
    comments = [comment for comment in p.load_all(Comment) if comment.thread == "$DEFAULT"]
    results = [comment_to_json(comment) for comment in comments]
    return json(results)


def comment_to_json(comment):
    return {
        "author": {
            "name": comment.author
        },
        "body": comment.body,
        "thread": {
            "name": comment.body
        }
    }


def main():
    app.run(port=9010, debug=True)

if __name__ == '__main__':
    main()
