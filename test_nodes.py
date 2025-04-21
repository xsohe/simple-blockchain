import requests
import json
import time
import sys

def test_blockchain_sync(node1, node2):
    """Test blockchain synchronization between two nodes"""
    print(f"Testing sync between {node1} and {node2}")
    
    # Step 1: Register nodes with each other
    print("\n1. Registering nodes with each other...")
    
    # Register node2 with node1
    register_response = requests.post(
        f"http://{node1}/nodes/add_nodes",
        json={"nodes": [f"http://{node2}"]}
    )
    print(f"Node1 registering Node2: {register_response.json()}")
    
    # Register node1 with node2
    register_response = requests.post(
        f"http://{node2}/nodes/add_nodes",
        json={"nodes": [f"http://{node1}"]}
    )
    print(f"Node2 registering Node1: {register_response.json()}")
    
    # Step 2: Mine a block on node1
    print("\n2. Mining a block on Node1...")
    mine_response = requests.get(f"http://{node1}/mine")
    print(f"Mine result: {mine_response.json()}")
    
    # Step 3: Check blockchain length on both nodes
    print("\n3. Checking blockchain length before sync...")
    node1_chain = requests.get(f"http://{node1}/blockchain").json()
    node2_chain = requests.get(f"http://{node2}/blockchain").json()
    
    print(f"Node1 chain length: {node1_chain['length']}")
    print(f"Node2 chain length: {node2_chain['length']}")
    
    # Step 4: Sync node2
    print("\n4. Syncing Node2...")
    sync_response = requests.get(f"http://{node2}/nodes/sync")
    print(f"Sync result: {sync_response.json()['message']}")
    
    # Step 5: Check blockchain length again
    print("\n5. Checking blockchain length after sync...")
    node1_chain = requests.get(f"http://{node1}/blockchain").json()
    node2_chain = requests.get(f"http://{node2}/blockchain").json()
    
    print(f"Node1 chain length: {node1_chain['length']}")
    print(f"Node2 chain length: {node2_chain['length']}")
    
    if node1_chain['length'] == node2_chain['length']:
        print("\nSYNC SUCCESSFUL! Both nodes have the same blockchain length.")
    else:
        print("\nSYNC FAILED! Nodes have different blockchain lengths.")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        node1 = sys.argv[1]
        node2 = sys.argv[2]
    else:
        node1 = "localhost:5000"
        node2 = "localhost:5001"
    
    test_blockchain_sync(node1, node2)