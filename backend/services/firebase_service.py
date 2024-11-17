# services/firebase_service.py
import pyrebase
from config import Config

firebase = pyrebase.initialize_app(Config.FIREBASE_CONFIG)
auth = firebase.auth()

def verify_token(token):
    try:
        user = auth.get_account_info(token)
        return user['users'][0]
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None
