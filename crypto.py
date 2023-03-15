from Crypto.Cipher import AES

KEY_LENGTH = 16

def pass2key(password,f):
    key = password.ljust(KEY_LENGTH)
    key = key.encode(f)
    return key

def encrypt_data(password,data,f):
    key = pass2key(password,f)
    cipher = AES.new(key,AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    nonce = cipher.nonce
    encrypted_data = nonce+tag+ciphertext
    return encrypted_data

def decrypt_data(password,encrypted_data,f):
    key = pass2key(password,f)
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    cipher = AES.new(key,AES.MODE_EAX,nonce)
    data = cipher.decrypt_and_verify(ciphertext,tag)
    return data