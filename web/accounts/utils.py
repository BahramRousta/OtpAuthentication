import hashlib
from typing import Optional, Any
from pyotp import TOTP


class Totp(TOTP):

    def __init__(self, s: str, digits: int = 6, digest: Any = hashlib.sha1, name: Optional[str] = None,
                 issuer: Optional[str] = None, interval: int = 1) -> None:
        self.interval = interval
        super().__init__(s, digits, digest, name, issuer, interval)


def generate_otp():
    totp = Totp('base32secret3232')
    code = totp.now()
    return code


PHONE_PAtTERN_REGEX = r"09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}"
MAIL_PATTERN_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'