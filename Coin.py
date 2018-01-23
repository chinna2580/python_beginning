from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode 
import os
import base64
from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Hash import SHA256 
import time

  # from Crypto.PublicKey import RSA 
  # from Crypto.Signature import PKCS1_v1_5 
  # from Crypto.Hash import SHA256 
  # from base64 import b64decode

COIN_SIZE =64
new_key = RSA.generate(bits= 2048, e=65537)
public_key = new_key.publickey()
print(public_key)
private_key = new_key
print(private_key)

goofy = {}
goofy['public_key'] = public_key
goofy['private_key'] = private_key

user_1 = {}
user_1_key = RSA.generate(bits= 2048, e=65537)
user_1['public_key'] = new_key.publickey()
user_1['private_key']= new_key


user_2 = {}
user_2_key = RSA.generate(bits= 2048, e=65537)
user_2['public_key'] = new_key.publickey()
user_2['private_key'] = new_key


user_3 = {}
user_3_key = RSA.generate(bits= 2048, e=65537)
user_3['public_key'] = new_key.publickey()
user_3['private_key'] = new_key


user_4 = {}
user_4_key = RSA.generate(bits= 2048, e=65537)
user_4['public_key'] = new_key.publickey()
user_4['private_key'] = new_key

import json 

def encode_data(data_tuple):
    string_tuple = tuple( str(data) for data in data_tuple )
    json_tuple = json.dumps(string_tuple)
    encoded_tuple = json_tuple.encode()

    return encoded_tuple

def sign_coin(private_key_loc, data):
  # from Crypto.PublicKey import RSA 
  # from Crypto.Signature import PKCS1_v1_5 
  # from Crypto.Hash import SHA256 
 # rsakey = RSA.importKey(private_key_loc) 
  signer = PKCS1_v1_5.new(private_key_loc) 
  digest = SHA256.new() 
  # It's being assumed the data is base64 encoded, so it's decoded before updating the digest 
  digest.update(b64decode(data)) 
  sign = signer.sign(digest) 
  return b64encode(sign)

def generate_goofy_coin():
  coin_id = str(os.urandom(COIN_SIZE))
  coin_id = base64.b64encode(coin_id)
  return coin_id

def verify_signed_coin(public_key, signature, data):
  '''
  Verifies with a public key from whom the data came that it was indeed 
  signed by their private key
  param: public_key_loc Path to public key
  param: signature String signature to be verified
  return: Boolean. True if the signature is valid; False otherwise. 
  '''
  # from Crypto.PublicKey import RSA 
  # from Crypto.Signature import PKCS1_v1_5 
  # from Crypto.Hash import SHA256 
  # from base64 import b64decode
  signer = PKCS1_v1_5.new(public_key) 
  digest = SHA256.new() 
  # Assumes the data is base64 encoded to begin with
  digest.update(b64decode(data)) 
  if signer.verify(digest, b64decode(signature)):
      return True
  return False

def sign_transfer_coin(spender_sk, coin_id, recipient_pk):
  encoded_data = encode_data((coin_id, recipient_pk))# base64.b64encode((coin_id, recipient_pk)) # 
  signed_transaction = sign_coin(spender_sk, encoded_data)
  return signed_transaction # self.secret_key.sign(encoded_data)

def genesis_block(spender, coin, recipient_pk):
  prev_block = coin
  spender_pk = spender['public_key']
  sign = sign_transfer_coin(spender['private_key'], coin, recipient_pk)
  genesis_block_data = {
    'created_by': 'Goofy',
    'Goofy_public_key': spender['public_key'],
    'transferred_to': recipient_pk,
    'time_stamp': time.time(),
    'used': 'false'
  }
  return genesis_block_data

new_coin = generate_goofy_coin()
signed_data = sign_coin(private_key, new_coin)
verify_signed_data = verify_signed_coin(public_key, signed_data, new_coin)
genesis_data = genesis_block(goofy, new_coin, user_1['public_key'])
print(genesis_data)

# print(user_4['public_key'])
# print(user_4['private_key'])

# verify_signed_data = verify_signed_coin(user_4['public_key'], signed_data, new_coin)
# print(verify_signed_data)
