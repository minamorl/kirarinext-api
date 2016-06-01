import datetime
import os
import dotenv
import hashlib
import random
import re
from . import p
from .models import *
from flask import session


def find_comments(thread, fetch_from=None, page=None):
    COMMENT_PER_PAGE = 50
    max_id = p.get_max_id(Comment)
    if max_id is None:
        return []
    if fetch_from is not None:
        ids = range(int(fetch_from) + 1, max_id + 1)
        return [p.load(Comment, _id) for _id in ids]
    # if both page and fetch_from are None, then return latest 50 comments.
    ids = range(max_id + 1 - 50, max_id + 1)
    return [p.load(Comment, _id) for _id in ids]


def find_thread(thread_name, ensure_exists=True):
    thread = p.find(Thread, lambda thread: thread.name == thread_name) or Thread(name=thread_name)
    if ensure_exists:
        p.save(thread)  # ensure thread is existing on database.
    return thread


def pick_author_image():
    img = random.randrange(0, 15)
    return "./img/{0:03d}.jpeg".format(img)


def is_signed_in():
    return session.get("username") is not None
