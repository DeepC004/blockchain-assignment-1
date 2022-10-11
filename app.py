import json
from django.http import response
from flask import Flask, jsonify, request

from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/add/user/', methods=['POST'])
def add_user():
    user = request.get_json()
    blockchain.add_user(user)
    print(blockchain.users)
    return jsonify(user),201

@app.route('/add/transaction/', methods=['POST'])
def add_transaction():
    transaction = request.get_json()
    blockchain.add_transaction(transaction)
    blockchain.update_history(transaction)
    return jsonify("Transaction completed"),201

@app.route('/history/', METHODS=['POST'])
def transaction_history():
    property = request.get_json()
    return jsonify(blockchain.transaction_history[property]),201


if __name__ == "__main__":
    app.run(debug=True)
