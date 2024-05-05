
import hashlib
import datetime as dt
import rsa


class Block:
    def __init__(self, index,data, time, previous_key, public_key, private_key=None):
        self.index = index
        self.data = data
        self.time = time
        self.previous_key = previous_key
        self.public_key = public_key.save_pkcs1().decode('utf-8')
        # self.public_key = self.public_key.replace("-----BEGIN RSA PUBLIC KEY-----\n", "").replace("\n-----END RSA PUBLIC KEY-----\n", "")


        if private_key:
            self.private_key = private_key.save_pkcs1().decode('utf-8')
            # self.private_key = private_key_str.replace("-----BEGIN RSA PRIVATE KEY-----\n", "").replace("\n-----END RSA PRIVATE KEY-----\n", "")
        else:
            self.private_key = None


        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(str(self.index).encode() + str(self.data).encode() + str(self.time).encode() + str(self.previous_key).encode()).hexdigest()
    
 
    def sign_block(self, private_key):
        if private_key:
            signature = rsa.sign(self.hash.encode(), rsa.PrivateKey.load_pkcs1(self.private_key.encode()), 'SHA-1')
            return signature
        return None
        
    def to_dict(self):
        return {
            'index': self.index,
            'data': self.data,
            'time': self.time.strftime("%Y-%m-%d %H:%M:%S"),
            'previous_key': self.previous_key,
            'hash': self.hash,
        }
    def data_dict(self):
        return self.data