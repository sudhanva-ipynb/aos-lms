import hashlib


def sha256_hash(obj):
    return hashlib.sha256(obj.encode()).hexdigest()