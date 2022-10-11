import hashlib
import json
from datetime import datetime

class Blockchain:

    def __init__(self):
        
        #all users who own a property
        self.users = dict()

        #to store transaction history associated with a property
        self.transaction_history = dict()

        #pool of unverified transactions, will be added to verified transactions post consensus algo run
        self.unverified_transactions = []

        
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