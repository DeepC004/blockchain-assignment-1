import hashlib
import json
import random
import string

from matplotlib.colors import cnames
from merkle import MerkleTools
from random import randint
from datetime import datetime

from xarray import MergeError

class Blockchain:

    def __init__(self):
        
        #all users who own a property
        self.users = dict()
        #to store transaction history associated with a property
        self.transaction_history = dict()

        #pool of unverified transactions, will be added to verified transactions post consensus algo run
        self.unverified_transactions = []

        #pool of verified transactions, will be added to verified transactions post consensus algo run
        self.verified_transactions = []

        #List to store blockchain
        self.chain=[]

        #Gensisblock - contains no transactions
        self.new_block(previous_hash=1)

        #Final rankings list at the end of voting process
        self.orderstakers = dict()

        #List of users who have chosen to participate by staking a share of 
        #their property
        self.stakers = dict()

        #List of chosen stakers who have the authority to mine the current block
        self.witnesses  = dict()

    def new_block(self,previous_hash = None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'transactions': self.unverified_transactions,
            'previous_hash': self.rand_hash() if previous_hash==1 else self.hash(self.last_block),
            'merkle_root': self.rand_hash() if previous_hash==1 else self.hash(self.last_block)
        }
        self.verified_transactions += self.unverified_transactions
        print(self.verified_transactions)
        self.unverified_transactions = []

        #appending the block at the end of the blockchain
        self.chain.append(block)
        return block  
        
    def add_users(self, users):
        self.users.update(users)
        print(self.users)

    def add_stakers(self, stakers):
        self.stakers.update(stakers)

    def add_transaction(self, transaction):
        buyer = transaction['buyer']
        seller = transaction['seller']
        property = transaction['property']
        self.users[seller]['property'].remove(property)
        self.users[buyer]['property'].append(property)
        self.unverified_transactions.append(transaction)
        print(transaction)
        return self.last_block['index']+1

    def update_history(self, transaction):
        buyer = transaction['buyer']
        seller = transaction['seller']
        property = transaction['property']
        value = transaction['value']
        print(buyer, seller, property, value)
        if property in self.transaction_history:
            self.transaction_history[property].append({
                'buyer' : buyer,
                'seller' : seller,
                'value' : value
            })
        else:
            self.transaction_history[property] = [{
                'buyer' : buyer,
                'seller' : seller,
                'value' : value
            }]
        print(self.transaction_history)

    def rand_hash(self):
        N=128
        res = ''.join(random.choices(string.ascii_letters, k=N))
        res = res.encode()
        return hashlib.sha256(res).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        transactions = block['transactions']
        transactions.append(block['previous_hash'])
        print(transactions)
        mt = MerkleTools()
        for transaction in transactions:
            mt.add_leaf(transaction)
        mt.make_tree()
        return mt.get_merkle_root()

#look into format of stakers and x
    def vote(self):
        self.stakers = self.users
        for user, _ in self.stakers.items():
            self.orderstakers[user] = 0
        for _, value in self.stakers.items():
            candidate,_ = random.choice(list(self.stakers.items()))
            length = len(value['property'])
            x = length*randint(0, length)
            self.orderstakers[candidate] += x  

    def result(self):
        print(self.orderstakers)
        self.orderstakers = dict(sorted(self.orderstakers.items(), key = lambda kv: (kv[1], kv[0]), reverse=True))

        self.witnesses = dict(list(self.orderstakers.items())[0:3])
        print(self.witnesses)
