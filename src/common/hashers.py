import hashlib
import pandas as pd
import numpy as np
import uuid


# Convert md5 hash into guid
def md5_to_guid(md5):
    if not (pd.isnull(md5)):
        md5 = str.lower(md5).replace("-", "")
        output = md5[0:8] + '-'
        output += md5[8:12] + '-'
        output += md5[12:16] + '-'
        output += md5[16:20] + '-'
        output += md5[20:]
    else:
        output = np.nan
    return uuid.UUID(output)


# Convert guid to an MD5 hash
def guid_to_md5(guid):
    if not (pd.isnull(guid)):
        output = str.lower(guid).replace("-", "")

    else:
        output = np.nan
    return output

# Get md5 hash of a file
def get_md5_hash_of_file(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# Get md5 file guid
def get_md5_hash_guid(filepath=None):
    md5_file_hash = get_md5_hash_of_file(filepath=filepath)
    md5_file_guid = md5_to_guid(md5_file_hash)
    return md5_file_guid


def get_md5_of_string(content: str):
    """
    Returns a md5 hash of a string as a guid
    """
    md5_hash = hashlib.md5(content.encode()).hexdigest()

    return md5_to_guid(md5_hash)
