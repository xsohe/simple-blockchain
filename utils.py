import json
import hashlib
from urllib.parse import urlparse

def serialize_block(block):
    """Convert block to serialized format"""
    return json.dumps(block, sort_keys=True)

def create_hash(block_string):
    """Create SHA-256 hash of a string"""
    return hashlib.sha256(block_string.encode()).hexdigest()

def validate_url(url):
    """Validate and normalize a URL"""
    parsed_url = urlparse(url)
    
    if parsed_url.netloc:
        return parsed_url.netloc
    elif parsed_url.path:
        return parsed_url.path
    else:
        return None