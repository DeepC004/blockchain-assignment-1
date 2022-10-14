import json
from django.http import response
from flask import Flask, jsonify, request
from numpy import block

from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

#Function for mining a block, only witnesses are allowed to mine a block
@app.route('/mine', methods=['GET'])
def mine_block():
    #To ensure that only delegates elected by voting can mine a new block
    current_port = "localhost:"+ str(port)
    if(current_port in blockchain.witnesses):

        # To ensure that a new block is mined only if there are atleast 4 transactions
        if len(blockchain.unverified_transactions) >= 4:
            block = blockchain.new_block()

            response = {
                'message': "New block mined!",
                'index': block['index'],
                'transactions': block['transactions'],
                'previous_hash': block['previous_hash']
            }

            print(len(blockchain.unverified_transactions))
            return jsonify(response), 200

        else:
            response = {
                'message' : 'Not enough transactions to mine a new block and add to chain!'
            }
            print(len(blockchain.unverified_transactions))
            return jsonify(response),400
    else:
        response = {
            'message': 'You are not authorised to mine block! Only delegates can mine.'
        }
        return jsonify(response),400

#To add new users to the network
@app.route('/add/users/', methods=['POST'])
def add_users():
    users = request.get_json()
    blockchain.add_users(users)
    response = {
        'message' : ' The following users have been added',
        'users' : users
    }
    return jsonify(response),201

#To add new transactions to the network
@app.route('/add/transaction/', methods=['POST'])
def add_transaction():
    transaction = request.get_json()
    seller = transaction['seller']
    property = transaction['property']
    if blockchain.users[seller]['property'].count(property) > 0:
        blockchain.add_transaction(transaction)
        blockchain.update_history(transaction)
        return jsonify("Transaction completed"),201
    else:
        return jsonify("Seller does not own the mentioned properties"),201

#To see the history of all the transactions relating to a particular property
@app.route('/history/', methods=['POST'])
def transaction_history():
    property = request.get_json()
    return jsonify(blockchain.transaction_history[property]),201

#To view the blockchain
@app.route('/chain/', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

#To initiate the voting process
@app.route('/voting/', methods=['GET'])
def voting():
    
    #Only primary node can conduct the voting process
    if port == 5000:
        blockchain.vote()
        blockchain.result()

        response = {
            'message' : 'The voting results are as follows:',
            'nodes' : blockchain.orderstakers
        }

        return jsonify(response), 200
    
    else:
        response = {
            'message' : 'You are not authorised to conduct the voting process'
        }
        return jsonify(response), 400

#To see the witnesses chosen for mining the current block
#If voting process is not complete then display the required message
@app.route('/witnesses/', methods=['GET'])
def view_delegates():
    response = {
        'message' : 'The following delegates have been chosed to mine the current block',
        'witnesses' : blockchain.witnesses
    }
    return jsonify(response), 200

#To add stakers to the current list of stakers for mining of current block
@app.route('/add/stakers/', methods=['POST'])
def add_stakers():
    stakers = request.get_json()
    blockchain.add_stakers(stakers)
    response = {
        'message' : 'The following stakers have been added',
        'stakers' : stakers
    }
    return jsonify(response), 201

#To remove a particular staker from the current list of stakers 
@app.route('/remove/staker/', methods=['POST'])
def remove_staker():
    staker = request.get_json()
    if blockchain.stakers.has_key(staker):
        blockchain.stakers.pop(staker, 'The following user is not a staker')
    response = {
        'message' : 'The following user has been removed',
        'staker' : staker
    }
    return jsonify(response), 201

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='Listening on port')
    args = parser.parse_args()
    port = args.port
    app.run(host = '0.0.0.0', port = port, debug=True)
