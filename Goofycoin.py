import datetime as dt
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256

class GoofyDS:
	def __init__(self,id,sender,receiver,amount,transaction,spentflag,parent_block_id,signature):
		self.id = id
		self.dirty = 0
		self.amount = amount
		self.next = None
		self.prev = None
		self.sender = sender
		self.receiver = receiver
		self.parent_block_id = parent_block_id
		self.transaction = transaction
		self.spentflag = spentflag
		self.timestamp = dt.datetime.now().strftime("Created on %d %b,%y(%A) at %I:%M:%S %p")
		self.signature = signature


class chains:
	def __init__(self):
		self.head=None
		self.id=0

	def blockid(self):
		self.id+=1
		return self.id

	def ischainempty(self):
		return self.head == None

	def addblock(self,block_id,sender,receiver,amount,transaction,spentflag,parent_block_id,signature):
		if amount == 0:
			spentflag = 1
		temp=GoofyDS(block_id,sender,receiver,amount,transaction,spentflag,parent_block_id,signature)
		h=self.head
		if h == None:
			self.head = temp
		else:
			while h.next != None:
				h=h.next
			h.next=temp

	def getlatestblock(self):
		t = self.head
		while t.next != None:
			t = t.next
		return t


	def getblock_by_id(self,vid):
		t = self.head
		while t != None:
			if t.id == vid:
				return t
			t = t.next

	def isvalid(self,vid):
		if self.getblock_by_id(vid).dirty:
			return False
		else:
			return True

	def printchain(self):
		print 'Transaction Ledgers\n['
		t=self.head
		while t != None:
			print '''
			  {
			     Block ID: ''',t.id,'''
			     Is Valid: ''',self.isvalid(t.id),'''
			     Senders Public Key: ''',SHA256.new(t.sender.exportKey('PEM')).hexdigest(),'''
			     Receivers Public Key: ''',SHA256.new(t.receiver.exportKey('PEM')).hexdigest(),'''
			     Parent: ''',t.parent_block_id,'''
			     Coins: ''',t.amount,'''
			     Transaction message: ''',t.transaction,'''
			     Timestamp: ''',t.timestamp,'''
			     Spent: ''',t.spentflag,'''
			     Signature:''',SHA256.new(str(t.signature)).hexdigest(),'''
			  }
			'''
			t=t.next
		print ']'



def main():

	def getkeys():
		prng = Random.new().read
		key = RSA.generate(2048,prng)
		private_key = key
		public_key = key.publickey()
		keys=[private_key,public_key]
		return keys

	def show_users():
		if not users:
			print 'No users are there in system !'
		else:
			for i in users:
				print i,' has ',users[i][1],' GoofyCoins in total'

	def transfer_coins():
		sender = raw_input('Enter Sender Name: ').lower()
		receiver = raw_input('Enter Receiver Name:').lower()
		amt = int(raw_input('Enter Coins: '))

		if sender not in users:
			print "User:",sender,"don't exist!"
			return

		if receiver not in users:
			print "User:",receiver,"don't exist!"
			return

		if users[sender][1] == 0:
			print sender,"have 0 coins !"
			return

		t = chain.head
		while t != None:
			if t.receiver == users[sender][0][1] and t.spentflag == 0 and amt <= t.amount:
				current_amt = t.amount
				t.spentflag = 1
				parent_block_id = t.id
				users[sender][1] = users[sender][1]-amt
				users[receiver][1] = users[receiver][1]+amt
				break
			else:
				t = t.next

			if t == None:
				print sender,' has Insufficient Coins!!!'
				return

		transaction1 = sender+' transferred '+str(amt)+' coins to '+receiver
		transaction2 = sender+' transferred '+str(current_amt-amt)+' coins to '+sender

		id1 = chain.blockid()
		id2 = chain.blockid()
		data_for_signature1 = str(id1)+str(users[sender][0][1])+transaction1+str(amt)
		data_for_signature2 = str(id2)+str(users[sender][0][1])+transaction2+str(current_amt-amt)

		sign1 = sign_coin(users[sender][0][0],data_for_signature1)
		sign2 = sign_coin(users[sender][0][0],data_for_signature2)


		chain.addblock(id1,users[sender][0][1],users[receiver][0][1],amt,transaction1,0,parent_block_id,sign1)
		chain.getlatestblock().prev = chain.getblock_by_id(parent_block_id)

		chain.addblock(id2,users[sender][0][1],users[sender][0][1],current_amt-amt,transaction2,0,parent_block_id,sign2)
		chain.getlatestblock().prev = chain.getblock_by_id(parent_block_id)

	def show_all_blocks():
		chain.printchain()

	def generate_goofy_coin():
		no = int(raw_input('Enter no. of coins: '))
		users['goofy'][1]=users['goofy'][1]+no
		transaction = 'Goofy created '+str(no)+' more coins in the system!'

		id = chain.blockid()
		data_for_signature = str(id)+str(users['goofy'][0][1])+transaction+str(no)
		sign = sign_coin(users['goofy'][0][0],data_for_signature)

		chain.addblock(id,users['goofy'][0][1],users['goofy'][0][1],no,transaction,0,None,sign)


	def sign_coin(sender_private_key,data):
		digest = SHA256.new(data).hexdigest()
		signature = sender_private_key.sign(digest,'')
		return signature


	def match_signature(sender_public_key,data,signature):
		digest = SHA256.new(data).hexdigest()
		return sender_public_key.verify(digest,signature)


	def verify():
		vid = int(raw_input('Enter the block id to verify the transaction: '))
		found = chain.getblock_by_id(vid)
		if found == None:
			print "Block don't exist !"
			return

		current_signature = found.signature
		current_transaction = found.transaction
		current_amt = found.amount
		current_sender = found.sender
		current_id = found.id

		while found.prev != None:

			data_for_signature = str(current_id)+str(current_sender)+current_transaction+str(current_amt)

			if match_signature(current_sender,data_for_signature,current_signature):
				found = found.prev
			else:
				print 'Transaction is Invalid, Please try Again!!!'
				return
			current_signature = found.signature
			current_transaction = found.transaction
			current_amt = found.amount
			current_sender = found.sender
			current_id = found.id

		data_for_signature = str(current_id)+str(current_sender)+current_transaction+str(current_amt)
		if match_signature(current_sender,data_for_signature,current_signature):
			print 'Yeyy!! Transaction is VALID!!!'
		else:
			print 'Transaction is Invalid, Please try Again!!!'

	def update_block():
		cb = int(raw_input('Enter block id to Update: '))
		bk = chain.getblock_by_id(cb)
		bk.amount = 1234
		bk.dirty = 1


	def validate_chain():
		t = chain.head
		if t == None:
			print 'Chain is empty, Create some Coins using Option 1 !'
			return
		while t != None:
			if not chain.isvalid(t.id):
				print 'blockChain is Invalid !'
				return
			t = t.next
		print 'blockChain is VALID !'

	users={
	'goofy':[getkeys(),0],
	'suresh':[getkeys(),0],
	'naresh':[getkeys(),0],
	'ganesh':[getkeys(),0]
	}
	chain = chains()


	while(True):
		print '''
======== Operations =============	
	1.Create coin      		
	2.Transfer Coins    	
	3.Show Transaction History   	
	4.Show users Coins
	5.Verify Transaction
	6.Update a block    
	7.Check Chain   
	8.Exit  '''
		try:
			ch=int(raw_input())
		except Exception:
			print 'Please enter choice no. !'
			continue
		myswitch={
		1:generate_goofy_coin,
		2:transfer_coins,
		3:show_all_blocks,
		4:show_users,
		5:verify,
		6:update_block,
		7:validate_chain,
		8:exit
		}
		try:
			myswitch.get(ch)()
		except Exception:
			print 'Invalid entry, Try again !'



if __name__ == '__main__':
	main()