import hashlib
from Importers.common_imports import *

def sha256_hash(obj):
    return hashlib.sha256(obj.encode()).hexdigest()

def getTimestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")