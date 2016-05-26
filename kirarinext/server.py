from flask import Flask, request, jsonify, session
import datetime
import os
import dotenv
import hashlib
import random
import re

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.permanent_session_lifetime = datetime.timedelta(days=7)


@app.before_request
def before_request():
    session.permanent = True

from . import endpoints
import types

for _, v in endpoints.__dict__.items():
    if isinstance(v, types.ModuleType):
        app.register_blueprint(v.api)
