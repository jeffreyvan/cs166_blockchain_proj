#Python-RSa
import rsa 
import base64

class Voter:
    def __init__(self, id, has_generated_key):
        self.id = id
        self.has_generated_key = has_generated_key

voters =  [ Voter("Y11", False), Voter("Y22", False) ] 

def generate_keys():
    (public_key, private_key) = rsa.newkeys(64)
    return public_key, private_key

def generate_voter_keys(voter_id):
    for searchVoter in voters:
        #check if the voter has generated a key, if not generate a key
        if searchVoter.id == voter_id: 
            if searchVoter.has_generated_key == False:
                (public_key, private_key) = rsa.newkeys(512)
                searchVoter.has_generated_key = True
                return public_key, private_key
            else:
                return "You already have a key!"


    # (public_key, private_key) = rsa.newkeys(512)
    # return public_key, private_key

def key_pair_to_base64(public_key, private_key):
    public_key_str = public_key.save_pkcs1().decode()
    private_key_str = private_key.save_pkcs1().decode()
    public_key_b64 = base64.b64encode(public_key_str.encode()).decode()
    private_key_b64 = base64.b64encode(private_key_str.encode()).decode()
    return public_key_b64, private_key_b64

def base64_to_key_pair(public_key_b64, private_key_b64):
    # Ensure proper padding
    public_key_b64 += '=' * ((4 - len(public_key_b64) % 4) % 4)
    private_key_b64 += '=' * ((4 - len(private_key_b64) % 4) % 4)
    public_key_str = base64.b64decode(public_key_b64).decode()
    private_key_str = base64.b64decode(private_key_b64).decode()
    public_key = rsa.PublicKey.load_pkcs1(public_key_str.encode())
    private_key = rsa.PrivateKey.load_pkcs1(private_key_str.encode())
    return public_key, private_key

def base_64_to_key(private_key_b64):
    private_key_b64 += '=' * ((4 - len(private_key_b64) % 4) % 4)
    private_key_str = base64.b64decode(private_key_b64).decode()
    private_key = rsa.PrivateKey.load_pkcs1(private_key_str.encode())
    return private_key

def base64_to_key(private_key_b64):
    private_key_b64 += '=' * ((4 - len(private_key_b64) % 4) % 4)
    private_key_str = base64.b64decode(private_key_b64).decode()
    private_key = rsa.PrivateKey.load_pkcs1(private_key_str.encode())
    return private_key
