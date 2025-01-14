import jwt
import datetime
from typing import Optional, Union

class JWTAuthManager:
    def __init__(self):
        with open("private_key.pem", "r") as PrivateFile:
            self.PrivateKey = PrivateFile.read().replace("/n", "")
        with open("public_key.pem", "r") as PublicFile:
            self.PublicKey = PublicFile.read().replace("/n", "")

    def CreateToken(self, identity: Union[str, int], AdditionalInfo: Optional[dict] = None) -> str:
        expiration = datetime.datetime.now() + datetime.timedelta(hours=3)
        payload = {
            "sub": identity,
            "exp": expiration,
            "iat": datetime.datetime.now()
        }
        if AdditionalInfo:
            payload.update(AdditionalInfo)
        return jwt.encode(payload, self.PrivateKey, algorithm="RS256")

    def CheckToken(self, token: str) -> dict:
        try:
            DecodedToken = jwt.decode(token, self.PublicKey, algorithms=["RS256"])
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False

