from flask import Flask, render_template, request, jsonify

import json

from blockchain import Blockchain
from urllib.parse import unquote
import key
from block import Block
import datetime as dt

app = Flask(__name__)


dummy_public_key, dummy_private_key = key.generate_keys()
blockchain = Blockchain(dummy_public_key, dummy_private_key)

voterID = {}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_keys', methods=['GET'])
def generate_keys():

    voter_id = request.args.get('voter_id')
    
    response = key.generate_voter_keys(voter_id)
    if response == "You already have a key!":
        return jsonify({'message': response})
    else:
        public_key, private_key = response

   
    public_key_b64, private_key_b64 = key.key_pair_to_base64(public_key, private_key)

    
    return jsonify({'public_key': public_key_b64, 'private_key': private_key_b64})


@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    # Get form data
    public_key = request.form.get('public-key')
    private_key = request.form.get('private-key')
    candidate = request.form.get('candidate')

    try:
        restored_public_key, restored_private_key = key.base64_to_key_pair(public_key, private_key)
    except:
        return jsonify({'message': 'Invalid key pair'})

    
    if restored_public_key in voterID and voterID[restored_public_key] == restored_private_key:
        return jsonify({'message': 'This key pair has already been used for voting'})

    blockchain.add_block(Block(blockchain.get_latest_block().index + 1, candidate, dt.datetime.now(), blockchain.get_latest_block().hash, 
                                restored_public_key, restored_private_key))
    
    voterID[restored_public_key] = restored_private_key

    return jsonify({'message': 'Vote submitted successfully', 'candidate': candidate})


@app.route('/verify_vote') 
def verify_vote():
   
    chain_data = [block.to_dict() for block in blockchain.chain]

    data = {
        'chain': chain_data,
        'length': len(chain_data),
        }
    response = app.response_class(
        response = json.dumps(data,indent=2),
        status = 200,
        mimetype = 'application/json'
    )
    return response

@app.route('/verify_my_vote', methods=['GET'])
def verify_my_vote():
    private_key = request.args.get('private-vote-key')
    restored_private_key = key.base64_to_key(private_key)


    block = blockchain.find_block_by_private_key(restored_private_key.save_pkcs1().decode())
    
    if block:
        print("I exist")
        print(block.to_dict())
        return jsonify({'message': 'Vote verified successfully', 'block': block.data_dict()})
    else:
        return jsonify({'message': 'Vote not found'})


if __name__ == '__main__':
    app.run(debug=True)
