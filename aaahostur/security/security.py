import bcrypt
import jwt

def generate_salt():
    return bcrypt.gensalt()


class Security:
    def __init__(self, secret, algorithm):
        self._secret = secret
        self._algorithm = algorithm

    def hashed_password(self, password) -> bytes:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd_bytes, salt)

    def verify_password(self, password, hashed_password) -> bool:
        pwd_bytes = password.encode('utf-8')
        return bcrypt.checkpw(pwd_bytes, hashed_password)

    def generate_jwt(self, payload: dict):
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode_jwt(self, token) -> dict:
        return jwt.decode(token, self._secret, algorithms=['self._algorithm'])
