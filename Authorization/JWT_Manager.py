
# ---------------------- JWT -------------------------
import jwt

# Command to generate private key: openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

# Command to generate public key: openssl rsa -pubout -in private_key.pem -out public_key.pem

# Install cryptography library: pip install cryptography


class JWT_Manager:
    def __init__(self, private_key_path, public_key_path):
        with open(private_key_path, 'r') as f:
            self.private_key = f.read()
        
        with open(public_key_path, 'r') as f:
            self.public_key = f.read()

    def encode(self, data):
        try:
            encoded = jwt.encode(data, self.private_key, algorithm='RS256') 
            return encoded
        except Exception as error:
            print(f"Error: {error}")
            return None

    def decode(self, token):
        try:
            decoded = jwt.decode(token, self.public_key, algorithms=['RS256']) 
            return decoded
        except Exception as e:
            print(e)
            return None