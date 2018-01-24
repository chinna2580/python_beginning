# class Coin:
# 	created_by = 'created_by'
# 	timestamp = 'timestamp'
# 	value = 'value'
# 	used = 'used'

# instance = Coin()
# print(instance.created_by)
# print(instance.timestamp)
# print(instance.value)
# print(instance.used)

# my_set = {
# 	'created_by': '',
# 	"timestamp" : '',
# 	"value" : '',
# 	"used" : ''
# }
# print(my_set)
# my_set['created_by'] = "suresh"
# my_set['timestamp'] = 'timestamp'
# my_set['value'] = '50'
# my_set['used'] = '30/11'
# print(my_set)
# print(my_set['created_by'])

class Userkeys:
 user_1 = '\xcd\xf0\x0c\xcb\x88Y\xd8\x1e\x15\xd5\xc3\xb3F(\x88\xda'
 user_2 = '\x0b\x0fC\xd8\xe5\x03\x8e-\r\xf7\xc3\xa1\xa8\xf56\x11'
 user_3 = 'Wol\x10R\x8a\x85\xd6\x8b\xbdIiR\xa5\xae\xfb'
 user_4 = '\x82\x93\xb0\xb7\x9b\xa2\xe1|\xd6\x9d\x986^\xd7\xd1\x15'

import base64
from Crypto.Cipher import AES
import os

private_info = raw_input("Ask user for something.")

def encryption(private_info):
	BLOCK_SIZE = 16
	PADDING = '('

	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
	EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

	# secret = os.urandom(BLOCK_SIZE)
	# print('encryption key is:', secret)

	keys = Userkeys()
	cipher = AES.new(keys.user_1)

	encoded = EncodeAES(cipher, private_info)
	print('Encypted String:', encoded)

encryption(private_info)