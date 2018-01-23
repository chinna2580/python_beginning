# from Crypto.Cipher import AES
# from Crypto.Signature import PKCS1_v1_5
# from Crypto.Hash import SHA
# import base64
# import os

# COIN_SIZE = 64

# def generate_goofy_coin():
# 	coin_id = str(os.urandom(COIN_SIZE))
# 	coin_id = base64.b64encode(coin_id)
# 	return coin_id

# def sign(message, priv_key):
# 	signer = PKCS1_v1_5.new(priv_key)
# 	digest = SHA.new()
# 	digest.update(message)
# 	return signer.sign(digest)
#  #  signer = PKCS1_v1_5.new(priv_key)
# 	# digest = SHA.new()
#  #  digest.update(message)
#  #  return signer.sign(digest)

# coin_id = str(generate_goofy_coin())
# secret = os.urandom(COIN_SIZE)
# # secret_key = SHA.new(secret)
# # secret.sign(coin_id)
# sign(coin_id, secret)
# # print(secret.sign(coin_id))

from Crypto.PublicKey import RSA 

new_key = RSA.generate(bits, e=65537) 
public_key = new_key.publickey().exportKey("PEM") 
private_key = new_key.exportKey("PEM") 
return private_key, public_key