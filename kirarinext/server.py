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

app.register_blueprint(endpoints.users.api)
app.register_blueprint(endpoints.comments.api)
app.register_blueprint(endpoints.account_settings.api)
app.register_blueprint(endpoints.signout.api)
