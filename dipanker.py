from base64 import b64encode, b64decode
import os
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import time

COIN_SIZE = 64

public_keys = {}
private_keys = {}

goofy_key = RSA.generate(bits=2048, e=65537)
public_keys['goofy'] = goofy_key.publickey()
private_keys['goofy'] = goofy_key

amit_key = RSA.generate(bits=2048, e=65537)
public_keys['amit'] = amit_key.publickey()
private_keys['amit'] = amit_key

import json


def encode_data(data_tuple):
    string_tuple = tuple(str(data) for data in data_tuple)
    json_tuple = json.dumps(string_tuple)
    encoded_tuple = json_tuple.encode()
    return encoded_tuple


def sign_coin(private_key_loc, data):
    '''
  this function signs a coin with the private key
  of the sender
  :param private_key_loc:
  :param data:
  :return:
  '''
    signer = PKCS1_v1_5.new(private_key_loc)
    digest = SHA256.new()
    # It's being assumed the data is base64 encoded, so it's decoded before updating the digest
    digest.update(b64decode(data))
    sign = signer.sign(digest)
    return b64encode(sign)


def generate_goofy_coin():
    '''
  This function generates goofy coins
  :return: unique id of the goofy coin
  '''
    coin_id = "CreateCoin" + str(os.urandom(COIN_SIZE))
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
        print "True"
        return True
    print "False"
    return False


def sign_transfer_coin(spender_sk, coin_id, recipient_pk):
    encoded_data = encode_data((coin_id,
                                recipient_pk))  # base64.b64encode((coin_id, recipient_pk)) #
    signed_transaction = sign_coin(spender_sk, encoded_data)
    return signed_transaction  # self.secret_key.sign(encoded_data)


def genesis_block(spender, coin, recipient_pk):
    prev_block = coin
    spender_pk = public_keys[spender]
    sign = sign_transfer_coin(private_keys[spender], coin, recipient_pk)
    genesis_block_data = {
        'created_by': 'Goofy',
        'Goofy_public_key': public_keys[spender],
        'transferred_to': recipient_pk,
        'time_stamp': time.time(),
        'used': 'false'
    }
    print genesis_block_data
    return genesis_block_data


def add_transaction(transaction_statement):
    transaction_statement = transaction_statement.strip().split()
    payer = transaction_statement[0].rstrip(':')
    payee = transaction_statement[-1]
    Coin_Id = transaction_statement[2]
    try:
        payer_public_key = public_keys[payer.lower()]
    except KeyError:
        print "payer does not exist"
    else:
        print "payer public key successfully found"
    try:
        payee_public_key = public_keys[payee.lower()]
    except KeyError:
        print "payee does not exist"
    else:
        print "payee public key successfully found"
    print payee_public_key, payer_public_key
    # find if the payer owns the coin or not
    # if yes create transaction, if no tell it does not exist


def runner_program():
    '''
  This is the main program that will take as input the transaction statements
  and create the data structure based on that
  :return: void
  '''
    while (1):
        s = raw_input()
        if s in ['Exit']:
            break
        print s
        add_transaction(s)


def main():
    new_coin = generate_goofy_coin()
    signed_data = sign_coin(private_keys['goofy'], new_coin)
    verify_signed_data = verify_signed_coin(public_keys['goofy'], signed_data,
                                            new_coin)
    genesis_data = genesis_block("goofy", new_coin, public_keys['amit'])
    runner_program()


if __name__ == '__main__':
    main()