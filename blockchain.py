import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse

class Blockchain:
    difficulty_target = "0000"

    def __init__(self):
        self.nodes = set()
        self.chain = []
        self.current_transactions = []

        # Create genesis block
        genesis_hash = self.hash_block("genesis_block")
        self.append_block(
            hash_of_previous_block=genesis_hash,
            nonce=self.proof_of_work(0, genesis_hash, [])
        )

    def hash_block(self, block):
        """
        Create a SHA-256 hash of a block
        """
        if isinstance(block, str):
            return hashlib.sha256(block.encode()).hexdigest()
        block_encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_encoded).hexdigest()
    
    def add_node(self, address):
        """
        Add a new node to the list of nodes
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
            print(f"Added node: {parsed_url.netloc}")
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
            print(f"Added node: {parsed_url.path}")
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if block['hash_of_previous_block'] != self.hash_block(last_block):
                print(f"Invalid previous hash at block {current_index}")
                return False
            
            if not self.valid_proof(
                current_index,
                block['hash_of_previous_block'],
                block['transaction'],
                block['nonce']):
                print(f"Invalid proof of work at block {current_index}")
                return False
            
            last_block = block
            current_index += 1

        return True 
    
    def update_blockchain(self):
        """
        Consensus algorithm: replace our chain with the longest valid chain in the network
        """
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            try:
                if not node.startswith('http'):
                    node_url = f"http://{node}"
                else:
                    node_url = node
                
                response = requests.get(f"{node_url}/blockchain", timeout=3)
                
                if response.status_code == 200:
                    data = response.json()
                    length = data['length']
                    chain = data['chain']

                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain
                        print(f"Found valid longer chain from {node}, length: {length}")
                    else:
                        print(f"Chain from {node} not longer or invalid, length: {length}")
            except Exception as e:
                print(f"Error contacting node {node}: {e}")
                continue

        if new_chain:
            print("Replacing blockchain with new longer valid chain")
            self.chain = new_chain
            return True
        
        print("Current chain is already the longest valid chain")
        return False

    def proof_of_work(self, index, hash_of_previous_block, transactions):
        """
        Simple Proof of Work Algorithm:
         - Find a number 'nonce' such that hash(index|previous_hash|transactions|nonce) contains 4 leading zeros
        """
        nonce = 0

        while self.valid_proof(index, hash_of_previous_block, transactions, nonce) is False:
            nonce += 1
        
        return nonce
    
    def valid_proof(self, index, hash_of_previous_block, transactions, nonce):
        """
        Validates the Proof: Does hash(index|previous_hash|transactions|nonce) contain 4 leading zeros?
        """
        content = f'{index}{hash_of_previous_block}{transactions}{nonce}'.encode()
        content_hash = hashlib.sha256(content).hexdigest()
        return content_hash[:len(self.difficulty_target)] == self.difficulty_target
    
    def append_block(self, nonce, hash_of_previous_block):
        """
        Create a new Block in the Blockchain
        """
        block = {
            "index": len(self.chain),
            "timestamp": time(),
            "transaction": self.current_transactions,
            "nonce": nonce,
            "hash_of_previous_block": hash_of_previous_block, 
        }

        self.current_transactions = []

        self.chain.append(block)
        return block
    
    def add_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        """
        self.current_transactions.append({
            "amount": amount,
            "recipient": recipient,
            "sender": sender
        })

        return self.last_block['index'] + 1
    
    @property
    def last_block(self):
        """
        Returns the last Block in the chain
        """
        return self.chain[-1]