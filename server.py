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


def error(msg):
    return json({
        "message": msg
    })


class Thread(PersistentData):
    id = Column()
    name = Column()


class Comment(PersistentData):
    id = Column()
    body = Column()
    thread = Column()
    author = Column()
    remote_addr = Column()


def find_all_comments(thread):
    return [comment for comment in p.load_all(Comment) if comment.thread == thread.name]


def find_thread(thread_name, ensure_exists=True):
    thread = p.find(Thread, lambda thread: thread.name == thread_name) or Thread(name=thread_name)
    if ensure_exists:
        p.save(thread)  # ensure thread is existing on database.
    return thread


@app.route("/api/comment.json", methods=["POST"])
def comment():
    body = request.json.get("body")
    thread = "$DEFAULT"
    if len(body) > 1000:
        return error("comment must be less than 10000 characters.")
    comment = Comment(
        body=body, thread=thread, author="anonymous",
        remote_addr=request.environ['REMOTE_ADDR'],
    )
    p.save(comment)
    return ok()


@app.route("/api/thread.json", methods=["GET"])
def thread():
    thread_name = "$DEFAULT"
    thread = find_thread(thread_name)
    comments = find_all_comments(thread)
    results = [comment_to_json(comment) for comment in comments]
    return json(results)


def comment_to_json(comment):
    return {
        "author": {
            "name": comment.author
        },
        "body": comment.body,
        "id": comment.id,
        "thread": {
            "name": comment.body
        }
    }


def main():
    app.run(port=9010, debug=True)

if __name__ == '__main__':
    main()
