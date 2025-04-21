import sys
from server import BlockchainServer

if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000
        
    server = BlockchainServer()
    server.run(port=port)
    
    print(f"Blockchain node running on port {port}")