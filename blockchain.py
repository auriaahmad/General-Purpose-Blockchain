# module 1 create block chain

import datetime
import hashlib
import json
from urllib import response
from flask import Flask, jsonify

#part 1 bulding a block chain (architechure of BC)
class Blockchain:
    def __init__(self):
        self.chain=[] #a list for chain
        self.create_block(proof=1, previous_hash='0') #genesis block
        
    #The __init__ method is the Python equivalent of the C++ 
    #constructor in an object-oriented approach. 
    #The __init__ function is called every time an object 
    #is created from a class. The __init__ method 
    #lets the class initialize the object's 
    #attributes and serves no other purpose. It is only used within classes.
    
    def create_block(self, proof, previous_hash):
        block = {
                'index' : len(self.chain)+1,
                'timestamp' : str(datetime.datetime.now()),
                'proof' : proof,
                'previous_hash': previous_hash
            }
        self.chain.append(block)
        return block
        
    def get_previous_block(self):
        return self.chain[-1] #last block of chain
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest(); 
             # to convert (something, such as a body of information)
             #from one system of communication into another especially
             #we are encoding the hash string for sha format
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # the functions to check everything is write at block chain 

    # 1 previus hash of each block is equal to previous block 
    # 2 correct proof of work ('0000') => proof of each work is valid with
    #       our proof of work problem defined in proof of work function
    # 
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof =block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest(); 
            if hash_operation[:4]!='0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    

#part 2 mining our block chain
 
#creating a flask web app
app = Flask(__name__)
# creating a block chain
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message':'congo! you just mined a block',
        'index':block['index'],
        'timestamp':block['timestamp'],
        'proof':block['proof'],
        'previous_hash':block['previous_hash'],
    }
    return jsonify(response),200