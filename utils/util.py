from datetime import timedelta, datetime
import jwt
import os
from dotenv import load_dotenv
from flask import request, jsonify
from functools import wraps

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

def encode_token(user_id):
    payload={
        'exp': datetime.now() + timedelta(days=0, hours=1 ),
        'iat': datetime.now(),
        'sub':user_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(' ')[1]
                print('Token:', token)
                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            except jwt.ExpiredSignatureError:
                return jsonify({'message':'token expired'})
            except jwt.InvalidTokenError:
                return jsonify({'message':"invalid token"})
        if not token:
            return jsonify({'message':'token missing'})
        return f(*args, **kwargs)
    
    return decorated