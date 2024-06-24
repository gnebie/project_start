from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from firebase_admin import auth
import firebase_admin
from app.config.firebase import firestore_client

class FirebaseAuth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(FirebaseAuth, self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        credentials = await super(FirebaseAuth, self).__call__(request)
        if credentials:
            token = credentials.credentials
            try:
                decoded_token = auth.verify_id_token(token)
                request.state.user = decoded_token
                return decoded_token
            except firebase_admin.auth.InvalidIdTokenError:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        raise HTTPException(status_code=403, detail="Invalid authorization code")

firebase_auth = FirebaseAuth()
