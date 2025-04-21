# Simple Blockchain Implementation

This is a simple blockchain implementation with a Flask web server.

## Project Structure

- `blockchain.py` - Contains the Blockchain class implementation
- `server.py` - Contains the Flask application and route definitions
- `run.py` - Main entry point to run the application
- `utils.py` - Utility functions
- `test_nodes.py` - Script to test node synchronization

## How to Run

1. Start the first node:

   ```
   python run.py 5000
   ```

2. Start the second node:

   ```
   python run.py 5001
   ```

3. Test synchronization between nodes:
   ```
   python test_nodes.py localhost:5000 localhost:5001
   ```

## API Endpoints

- `GET /blockchain` - Get the full blockchain
- `GET /mine` - Mine a new block
- `POST /transactions/new` - Create a new transaction
- `POST /nodes/add_nodes` - Register new nodes
- `GET /nodes/sync` - Synchronize with other nodes
