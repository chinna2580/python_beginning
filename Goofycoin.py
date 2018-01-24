import datetime as dt
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256

class chain:
	def __init__(self, id, spender, recipient, coins, transaction_message, spent_flag, parent_id, spender_signature):
		self.id = id
		self.is_corrupted = 0
		self.coins = coins
		self.next = None
		self.prev = None
		self.spender = spender
		self.recipient = recipient
		self.parent_id = parent_id
		self.transaction_message = transaction_message
		self.spent_flag = spent_flag	 #0-not spent, 1-spent
		self.timestamp = dt.datetime.now() #.strftime("Created on %d %b,%y(%A) at %I:%M:%S %p")	#dt.date.today().weekday()
		self.spender_signature = spender_signature

class block:
	def __init__(self):
		self.head = None
		self.id = 0

	def generate_block_id(self):
		self.id += 1
		return self.id

	def add_transaction_ledger(self, block_id, spender, recipient, coins, transaction_message, spent_flag, parent_id, spender_signature):
		#### if you have 0 bitcoin, you can't pay as you have spent all bitcoin ####
		if coins == 0:
			spentflag = 1
		current_block = chain(block_id, spender, recipient, coins, transaction_message, spent_flag, parent_id, spender_signature)
		############################

		hash_pointer = self.head
		if hash_pointer == None:
			self.head = current_block
		else:
			while hash_pointer.next != None:
				hash_pointer = hash_pointer.next
			hash_pointer.next = current_block
	def show_transaction_history(self):
		print '============Transaction History===========\n['
		hash_pointer_temp = self.head
		while hash_pointer_temp != None:# '!=' is equivalent to 'is not'
			#using SHA256 for shortening long public and private keys and signature also...
			print '''
				  {
				     ID: ''', hash_pointer_temp.id,'''
				     Is Valid: ''', self.is_a_valid_ledger(hash_pointer_temp.id),'''
				     Spenders Public Key: ''', SHA256.new(hash_pointer_temp.spender.exportKey('PEM')).hexdigest(),'''
				     Recipient Public Key: ''', SHA256.new(hash_pointer_temp.recipient.exportKey('PEM')).hexdigest(),'''
				     Parent Block: ''', hash_pointer_temp.parent_id,'''
				     Coins: ''', hash_pointer_temp.coins,'''
				     Transaction: ''', hash_pointer_temp.transaction_message,'''
				     Timestamp: ''', hash_pointer_temp.timestamp,'''
				     Spent: ''', hash_pointer_temp.spent_flag,'''
				     Spender Signature:''',SHA256.new(str(hash_pointer_temp.spender_signature)).hexdigest(),'''
				  }
				'''
			hash_pointer_temp = hash_pointer_temp.next
		print ']'

	def is_a_valid_ledger(self, block_id):
		if self.list_block_by_id(block_id).is_corrupted:
			return False
		else:
			return True

	def list_block_by_id(self, block_id):
		hash_pointer_temp = self.head
		while hash_pointer_temp != None:
			if hash_pointer_temp.id == block_id:
				return hash_pointer_temp
			hash_pointer_temp = hash_pointer_temp.next


	def get_current_block(self):
		hash_pointer_temp = self.head
		while hash_pointer_temp.next != None:
			hash_pointer_temp = hash_pointer_temp.next
		return hash_pointer_temp

def main():

	def generate_user_keys():
		prng = Random.new().read
		key = RSA.generate(2048,prng)
		public_key = key.publickey()
		secret_key = key
		keys = [public_key, secret_key]
		return keys

	def generate_goofy_coin():
		coin_count = int(raw_input('Enter no. of coins to create: '))
		users['goofy'][1] = users['goofy'][1] + coin_count
		transaction_message = "Added "+ str(coin_count) + " coins to Goofy"
		block_id = block_instance.generate_block_id()
		coin_to_be_signed = str(block_id) + str(users['goofy'][0][1])+ transaction_message + str(coin_count)
		sign = sign_coin(users['goofy'][0][1], coin_to_be_signed)
		block_instance.add_transaction_ledger(block_id, users['goofy'][0][0],users['goofy'][0][0], coin_count, transaction_message,0,None,sign)
		print(str(coin_count)+"'s has been generated and added to Goofy's account")

	def sign_coin(spender_private_key, coins):
		digest = SHA256.new(coins).hexdigest()
		signature = spender_private_key.sign(digest,'')
		return signature

	def verify_signature(spender_public_key, coins, signature):
		digest = SHA256.new(coins).hexdigest()
		return spender_public_key.verify(digest, signature)

	def match_signature(sender_public_key,data,signature):
		digest = SHA256.new(data).hexdigest()
		return sender_public_key.verify(digest,signature)


	def make_a_transaction():
		spender_user = raw_input('From which User is the Debit? ').lower()
		recipient_user = raw_input('Transfer to User?').lower()
		trans_coins = int(raw_input('Enter No of coins? '))
		if spender_user not in users:
			print "User:",spender_user,"don't exist!"
			# ch = raw_input('Add user(Y/N)?')
			# if ch.lower() == 'y':
			# 	add_user()
			return
		if recipient_user not in users:
			print "User:",recipient_user,"don't exist!"
			# ch = raw_input('Add user(Y/N)?')
			# if ch.lower() == 'y':
			# 	add_user()
			return
		if users[spender_user][1] == 0:
			print spender_user,"have 0 Coins in his account !"
			return
		hash_pointer_temp = block_instance.head
		while hash_pointer_temp != None:
			if hash_pointer_temp.recipient == users[spender_user][0][0] and hash_pointer_temp.spent_flag == 0 and trans_coins <= hash_pointer_temp.coins:
				current_coins = hash_pointer_temp.coins
				hash_pointer_temp.spent_flag = 1
				parent_id = hash_pointer_temp.id
				users[spender_user][1] = users[spender_user][1] - trans_coins
				users[recipient_user][1] = users[recipient_user][1] + trans_coins
				break
			else:
				hash_pointer_temp = hash_pointer_temp.next

			if hash_pointer_temp == None:
				print spender_user,' is trying to spend more than what they have !'
				return

		receipt_transaction = spender_user +' transferred '+ str(trans_coins) +' coins to '+ recipient_user
		spender_transaction = spender_user +' Current Coins are '+str(current_coins - trans_coins) # +' coins to '+spender_user

		recipient_block_id = block_instance.generate_block_id()
		spender_block_id = block_instance.generate_block_id()

		# coins_to_be_signed1 = str(recipient_block_id)+str(users[sender][0][1])+transaction1+str(amt)
		# coins_to_be_signed2 = str(spender_block_id)+str(users[sender][0][1])+transaction2+str(current_amt-amt)

		coins_to_be_signed1 = str(recipient_block_id) + str(users[spender_user][0][0]) + str(receipt_transaction) + str(trans_coins)
		coins_to_be_signed2 = str(spender_block_id) + str(users[spender_user][0][0]) + str(spender_user) + str(current_coins - trans_coins)

		signed1 = sign_coin(users[spender_user][0][1], coins_to_be_signed1)
		signed2 = sign_coin(users[recipient_user][0][1], coins_to_be_signed2)


		block_instance.add_transaction_ledger(recipient_block_id,users[spender_user][0][0],users[recipient_user][0][0],trans_coins, receipt_transaction, 0, parent_id,signed1)
		block_instance.get_current_block().prev = block_instance.list_block_by_id(parent_id)

		block_instance.add_transaction_ledger(spender_block_id,users[spender_user][0][0],users[spender_user][0][0],current_coins-trans_coins, spender_transaction, 0, parent_id, signed2)
		block_instance.get_current_block().prev = block_instance.list_block_by_id(parent_id)

	def transact():
		sender = raw_input('Enter Sender: ').lower()
		receiver = raw_input('Enter Receiver:').lower()
		amt = int(raw_input('Enter amount: '))

		if sender not in users:
			print "User:",sender,"don't exist!"
			# ch = raw_input('Add user(Y/N)?')
			# if ch.lower() == 'y':
			# 	add_user()
			# return

		if receiver not in users:
			print "User:",receiver,"don't exist!"
			# ch = raw_input('Add user(Y/N)?')
			# if ch.lower() == 'y':
			# 	add_user()
			# return


		#### precheck balance then only go forward ####
		if users[sender][1] == 0:
			print sender,"have 0 balance !"
			return

		######## work on cryptography

		############################

		t = block_instance.head
		while t != None:
			#comparing pulbic keys of the two nodes
			if t.recipient == users[sender][0][1] and t.spent_flag == 0 and amt <= t.coins:
				current_amt = t.coins
				t.spent_flag = 1
				parent_block_id = t.id
				###### local reference ######
				users[sender][1] = users[sender][1]-amt
				users[receiver][1] = users[receiver][1]+amt
				#############################
				break
			else:
				t = t.next

			if t == None:
				print sender,' is trying to spend more than what they have !'
				return
		#############################



		#### we can add block before verifying the transaction by meeting certain conditions or during the time of adding block...

		transaction1 = sender+' paid '+str(amt)+' coins to '+receiver
		transaction2 = sender+' paid '+str(current_amt-amt)+' coins to '+sender

		id1 = block_instance.generate_block_id()
		id2 = block_instance.generate_block_id()
		data_for_signature1 = str(id1)+str(users[sender][0][1])+transaction1+str(amt)
		data_for_signature2 = str(id2)+str(users[sender][0][1])+transaction2+str(current_amt-amt)

		sign1 = sign_coin(users[sender][0][0],data_for_signature1)
		sign2 = sign_coin(users[sender][0][0],data_for_signature2)


		block_instance.add_transaction_ledger(id1,users[sender][0][1],users[receiver][0][1],amt,transaction1,0,parent_block_id,sign1)
		block_instance.get_current_block().prev = block_instance.list_block_by_id(parent_block_id)

		block_instance.add_transaction_ledger(id2,users[sender][0][1],users[sender][0][1],current_amt-amt,transaction2,0,parent_block_id,sign2)
		block_instance.get_current_block().prev = block_instance.list_block_by_id(parent_block_id)

	def verify_transaction_block():
		vid = int(raw_input('Enter the block id(to verify): '))
		found = block_instance.list_block_by_id(vid)
		print(found)
		if found == None:
			print "Block don't exist !"
			return
		# if found.prev == None:
		# 	print 'Transaction is valid !'
		# else:

		current_signature = found.spender_signature
		print(current_signature)
		current_transaction = found.transaction_message
		print(current_transaction)
		current_amt = found.coins
		print(current_amt)
		current_sender = found.spender
		print(current_sender)
		current_id = found.id
		print(current_id)

		while found.prev != None:
			# ########### finding sender name to get its private key from the local data structure(dictionary) ###########
			# for i in users:
			# 	if users[i][0][1] == found.sender:
			# 		sender_name = i
			# 		break
			# ###########################################

			data_for_signature = str(current_id)+str(current_sender)+current_transaction+str(current_amt)
			# sign = calculate_signature(users[sender_name][0][0],data_for_signature)

			if match_signature(current_sender,data_for_signature,current_signature):
				found = found.prev
			else:
				print 'Transaction is NOT VALID !here'
				return
			current_signature = found.spender_signature
			print(current_signature)
			current_transaction = found.transaction_message
			print(current_transaction)
			current_amt = found.coins
			print(current_amt)
			current_sender = found.spender
			print(current_sender)
			current_id = found.id
			print(current_id)

		data_for_signature = str(current_id)+str(current_sender)+current_transaction+str(current_amt)
		print("here before match_signature")
		print(match_signature(current_sender,data_for_signature,current_signature))
		if match_signature(current_sender,data_for_signature,current_signature):
			print 'Transaction is VALID !'
		else:
			print 'Transaction is NOT VALID !'
	# def verify_block_transaction():
	# 	validate_block_id = int(raw_input('Enter the block Transaction id(to verify): '))
	# 	validate_block = block_instance.list_block_by_id(validate_block_id)
	# 	if validate_block == None:
	# 		print "Tranasaction Block don't exist !!!! Please Cross verify the Transaction ID you Entered"
	# 		return
	# 	current_block_signature = validate_block.spender_signature
	# 	current_block_transaction_msg = validate_block.transaction_message
	# 	current_block_coins = validate_block.coins
	# 	current_block_spender = validate_block.spender
	# 	current_block_id = validate_block.id

	# 	while found.prev != None:
	# 		# ########### finding sender name to get its private key from the local data structure(dictionary) ###########
	# 		# for i in users:
	# 		# 	if users[i][0][1] == found.sender:
	# 		# 		sender_name = i
	# 		# 		break
	# 		# ###########################################

	# 		data_for_signature = str(current_id)+str(current_sender)+current_transaction+str(current_amt)
	# 		# sign = calculate_signature(users[sender_name][0][0],data_for_signature)

	# 		if match_signature(current_sender,data_for_signature,current_signature):
	# 			found = found.prev
	# 		else:
	# 			print 'Transaction is NOT VALID !'
	# 			return
	# 		current_signature = found.signature
	# 		current_transaction = found.transaction
	# 		current_amt = found.amount
	# 		current_sender = found.sender
	# 		current_id = found.id

	# 	data_for_signature = str(current_id)+str(current_sender)+current_transaction+str(current_amt)
	# 	if match_signature(current_sender,data_for_signature,current_signature):
	# 		print 'Transaction is VALID !'
	# 	else:
	# 		print 'Transaction is NOT VALID !'

	# 	# while validate_block.prev != None:
	# 	# 	# ########### finding sender name to get its private key from the local data structure(dictionary) ###########
	# 	# 	# for i in users:
	# 	# 	# 	if users[i][0][1] == found.sender:
	# 	# 	# 		sender_name = i
	# 	# 	# 		break
	# 	# 	# ###########################################

	# 	# 	validate_transaction = str(current_block_id)+str(current_block_spender)+current_block_transaction_msg+str(current_block_coins)
	# 	# 	# sign = calculate_signature(users[sender_name][0][0],data_for_signature)

	# 	# 	if verify_signature(current_block_spender,validate_transaction, current_block_signature):
	# 	# 		validate_block = validate_block.prev
	# 	# 	else:
	# 	# 		print 'Transaction is NOT VALID !'
	# 	# 		return
	# 	# 	current_block_signature = validate_block.signature
	# 	# 	current_block_transaction_msg = validate_block.transaction
	# 	# 	current_block_coins = validate_block.amount
	# 	# 	current_block_spender = validate_block.sender
	# 	# 	current_block_id = validate_block.id

	# 	# validate_transaction = str(current_block_id)+str(current_block_spender)+current_block_transaction_msg+str(current_block_coins)
	# 	# if verify_signature(current_block_spender,validate_transaction,current_block_signature):
	# 	# 	print 'Yayy!!! Entered Transaction is VALID !'
	# 	# else:
	# 	# 	print 'Sorry!!! That is an Invalid Transaction !'


	# Create users and assign initial coins to them as Zero
	users={
	'goofy':[generate_user_keys(), 0],
	"suresh": [generate_user_keys(), 0] # ,
	# 'naresh':[generate_user_keys(), 0],
	# 'mahesh':[generate_user_keys(), 0]
	}
	print(users)
	block_instance = block()
	generate_goofy_coin()
	block_instance.show_transaction_history()
	transact()
	block_instance.show_transaction_history()
	# make_a_transaction()
	# block_instance.show_transaction_history()
	verify_transaction_block()
if __name__ == '__main__':
	main()