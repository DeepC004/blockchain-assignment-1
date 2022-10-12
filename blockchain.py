import hashlib
import json
from merkle import MerkleTools
from datetime import datetime
from random import randint

class Blockchain:

    def __init__(self):
        
        #all users who own a property(all nodes)
        self.users = dict()

        #to store transaction history associated with a property
        self.transaction_history = dict()

        #pool of unverified transactions, will be added to verified transactions post consensus algo run
        self.unverified_transactions = []
        
        #pool of verified transactions, will be added to verified transactions post consensus algo run
        self.verified_transactions = []
        
        #List to store blockchain
        self.chain=[]
        
        #Gensisblock
        self.new_block(prev_hash=1)
        
        #List consisting of votes of nodes in descending order
        self.orderminers=[]
        
        #List consisting of the nodes which can mine
        #need a method for adding new miners
        self.miners=[]
        
        #List of chosen miners for mining the block
        self.chosenminers=[]

    def new_block(self,previous_hash = None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'transactions': self.unverified_transactions,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.verified_transactions += self.unverified_transactions
        print(self.verified_transactions)
        self.unverified_transactions = []

        #appending the block at the end of the blockchain
        self.chain.append(block)
        return block  
        
    def add_user(self, user):
        self.users.update(user)

    def add_transaction(self, transaction):
        buyer = transaction["Buyer name"]
        seller = transaction["Seller name"]
        property = transaction["Property name"]
        if self.users[seller]["Property"].count(property) > 0:
            self.users[seller]["Property"].remove(property)
            self.users[buyer]["Property"].append(property)
            self.unverified_transactions.append(transaction)
        print(self.users)


    def update_history(self, transaction):
        buyer = transaction["Buyer name"]
        seller = transaction["Seller name"]
        property = transaction["Property name"]
        value = transaction["Property value"]
        print(buyer, seller, property, value)
        if property in self.transaction_history:
            self.transaction_history[property].append({
                "Buyer" : buyer,
                "Seller" : seller,
                "Value" : value
            })
        else:
            self.transaction_history[property] = [{
                "Buyer" : buyer,
                "Seller" : seller,
                "Value" : value
            }]
        print(self.transaction_history[property])
        
    def vote(self):
        for x in self.miners:
            y=list(x)
            y.append(x[1] * (randint(0,100)%25))#multiply stake(size of property list)
            self.orderminers.append(y)

        print(self.orderminers)     
        
    def result(self):
        self.orderminers = sorted(self.orderminers, key = lambda vote: vote[2],reverse = True)
        print(self.orderminers)

        for x in range(3):
            self.chosenminers.append(self.orderminers[x])
        print(self.chosenminers)

        