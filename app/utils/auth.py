import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from pydantic import EmailStr

load_dotenv()


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # os.getenv('secret_dust')
    secret = 't7w!z%C*F-JaNdRgUkXn2r5u8x/A?D(G+KbPeShVmYq3s6v9y$B&E)H@McQfTjWn'

    def hashit(self, password):
        return self.pwd_context.hash(password)

    def verify_pwd(self, plain, hashed):
        return self.pwd_context.verify(plain, hashed)

    def token_data(self, data):
        re_data = self.untokenize(data)
        return re_data

    def tokenize(self, email: EmailStr, pin: str, fullname: str):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, hours=8),
            'iat': datetime.utcnow(),
            'sub': [fullname, pin, email]
        }
        return jwt.encode(payload, self.secret, 'HS256')

    def untokenize(self, token):
        try:
            payload = jwt.decode(token, self.secret, 'HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Signature has expired and action cancelled.')
        except jwt.InvalidTokenError as ex:
            raise HTTPException(
                status_code=401, detail="Invalid token provided and access denied.")

    def signed(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.untokenize(auth.credentials)
