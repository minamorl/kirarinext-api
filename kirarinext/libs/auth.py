import re
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

 
def is_valid_username(username):
    cond = True
    cond = username != "anonymous" 
    cond = cond and re.match(r'^[A-Za-z0-9_]{3,12}$', username) 
    return cond
