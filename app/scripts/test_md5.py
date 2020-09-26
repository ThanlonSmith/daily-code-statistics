import hashlib

hash = hashlib.md5(b'123456')
hash.update(b'123456')
ret = hash.hexdigest()
print(ret)
