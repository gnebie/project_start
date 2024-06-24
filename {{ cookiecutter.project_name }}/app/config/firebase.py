import firebase_admin
from firebase_admin import credentials, auth, firestore
import logging

# Configure logger
logger = logging.getLogger(__name__)

def initialize_firebase():
    """
    Initialize Firebase with the provided settings.

    """
    if not firebase_admin._apps:
        cred = credentials.Certificate("config-files/fairytale-stories-firebase-admin.json")
        firebase_admin.initialize_app(cred)
        logger.trace("Firebase initialized with credentials from %s", "config-files/fairytale-stories-firebase-admin.json")

initialize_firebase()
firestore_client = firestore.client()
