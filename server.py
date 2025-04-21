from flask import Flask, request, jsonify
from blockchain import Blockchain
from uuid import uuid4

class BlockchainServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.blockchain = Blockchain()
        self.node_identifier = str(uuid4()).replace("-", "")
        
        self.register_routes()
    
    def register_routes(self):
        @self.app.route("/blockchain", methods=["GET"])
        def full_chain():
            response = {
                "chain": self.blockchain.chain,
                "length": len(self.blockchain.chain)
            }
            return jsonify(response), 200

        @self.app.route("/mine", methods=["GET"])
        def mine_block():
            self.blockchain.add_transaction(
                sender="0",  # 0 means new coins
                recipient=self.node_identifier,
                amount=1
            )

            last_block_hash = self.blockchain.hash_block(self.blockchain.last_block)

            index = len(self.blockchain.chain)
            nonce = self.blockchain.proof_of_work(
                index, 
                last_block_hash, 
                self.blockchain.current_transactions
            )

            block = self.blockchain.append_block(nonce, last_block_hash)

            response = {
                "message": "New block has been added (mined)",
                "index": block["index"],
                "hash_of_previous_block": block["hash_of_previous_block"],
                "nonce": block["nonce"],
                "transaction": block["transaction"]
            }

            return jsonify(response), 200

        @self.app.route("/transactions/new", methods=["POST"])
        def new_transaction():
            values = request.get_json()

            required_fields = ['sender', 'recipient', 'amount']
            if not all(k in values for k in required_fields):
                return "Missing required fields", 400
            
            index = self.blockchain.add_transaction(
                values["sender"],
                values["recipient"],
                values["amount"],
            )

            response = {"message": f"Transaction will be added to Block {index}"}
            return jsonify(response), 201

        @self.app.route("/nodes/add_nodes", methods=["POST"]) 
        def add_nodes():
            values = request.get_json()
            nodes = values.get('nodes')

            if nodes is None: 
                return "Error: Please supply a valid list of nodes", 400
            
            for node in nodes:
                self.blockchain.add_node(node)

            response = {
                "message": "New nodes have been added",
                "nodes": list(self.blockchain.nodes)
            }

            return jsonify(response), 200

        # Consensus algorithm
        @self.app.route("/nodes/sync", methods=["GET"])
        def sync():
            update = self.blockchain.update_blockchain()
            print(f"[DEBUG] Sync status: {update}")
            print(f"[DEBUG] Current chain length: {len(self.blockchain.chain)}")
            
            if update:
                response = {
                    "message": "Blockchain has been updated with the latest data",
                    "blockchain": self.blockchain.chain
                }
            else: 
                response = {
                    "message": "Our blockchain is already up to date",
                    "blockchain": self.blockchain.chain
                }

            return jsonify(response), 200

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port)