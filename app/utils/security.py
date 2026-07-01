import base64
import hashlib
import hmac
import secrets



PASSWORD_HASH_ALGORITHM = "pbkdf2_sha256"
PASSWORD_HASH_DIGEST = "sha256"
PASSWORD_HASH_ITERATIONS = 600_000
PASSWORD_SALT_BYTES = 16


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(PASSWORD_SALT_BYTES)
    password_hash = hashlib.pbkdf2_hmac(
        PASSWORD_HASH_DIGEST,
        password.encode("utf-8"),
        salt,
        PASSWORD_HASH_ITERATIONS,
    )

    salt_text = base64.urlsafe_b64encode(salt).decode("ascii")
    hash_text = base64.urlsafe_b64encode(password_hash).decode("ascii")
    return f"{PASSWORD_HASH_ALGORITHM}${PASSWORD_HASH_ITERATIONS}${salt_text}${hash_text}"


def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations_text, salt_text, expected_hash_text = password_hash.split("$", 3)
    except ValueError:
        return False

    if algorithm != PASSWORD_HASH_ALGORITHM:
        return False

    try:
        iterations = int(iterations_text)
        salt = base64.urlsafe_b64decode(salt_text.encode("ascii"))
        expected_hash = base64.urlsafe_b64decode(expected_hash_text.encode("ascii"))
    except (ValueError, TypeError):
        return False

    actual_hash = hashlib.pbkdf2_hmac(
        PASSWORD_HASH_DIGEST,
        plain_password.encode("utf-8"),
        salt,
        iterations,
    )
    return hmac.compare_digest(actual_hash, expected_hash)


def create_secure_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_token_hash(token: str, token_hash: str) -> bool:
    return hmac.compare_digest(hash_token(token), token_hash)


