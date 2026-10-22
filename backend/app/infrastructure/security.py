import hashlib
import hmac
import secrets


class Sha256TokenService:
    """Random edit tokens. They carry 256 bits of entropy, so a fast hash is sufficient."""

    def generate(self) -> str:
        return secrets.token_urlsafe(32)

    def hash(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def verify(self, token: str, token_hash: str) -> bool:
        return hmac.compare_digest(self.hash(token), token_hash)
