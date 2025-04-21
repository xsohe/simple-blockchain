# Simple Blockchain Implementation

This is a simple blockchain implementation with a Flask web server.

## Project Structure

- `blockchain.py` - Contains the Blockchain class implementation
- `server.py` - Contains the Flask application and route definitions
- `run.py` - Main entry point to run the application
- `utils.py` - Utility functions
- `test_nodes.py` - Script to test node synchronization

## How to Run

1. Install flask:

   ```
   python -m pip install flask
   ```

2. Install requests:

   ```
   python -m pip install requests
   ```

3. Start the first node:

   ```
   python run.py 5000
   ```

4. Start the second node:

   ```
   python run.py 5001
   ```

5. Test synchronization between nodes:
   ```
   python test_nodes.py localhost:5000 localhost:5001
   ```

## API Endpoints

- `GET /blockchain` - Get the full blockchain

## Response

```
{
    "chain": [
        {
            "hash_of_previous_block": "a1c0749b5b39ae000916b037528fe92676b68cc28ce91dc6762e50698c98214e",
            "index": 0,
            "nonce": 130540,
            "timestamp": 1745243455.1048682,
            "transaction": []
        },
        {
            "hash_of_previous_block": "0dc3919efec82ed24b594f82d60fccf88e8b9be174985f97b217f3e4e6649a4d",
            "index": 1,
            "nonce": 92634,
            "timestamp": 1745243493.369519,
            "transaction": [
                {
                    "amount": 1,
                    "recipient": "d0e87a3f3c5445418e7d6ee0359da9de",
                    "sender": "0"
                }
            ]
        }
    ],
    "length": 2
}
```

- `GET /mine` - Mine a new block

## Response

```
{
    "hash_of_previous_block": "6d0631f570c6a1d261aae0629faa1f0fbd4001add8777c7c2731c9f02f25ef8d",
    "index": 3,
    "message": "New block has been added (mined)",
    "nonce": 181521,
    "transaction": [
        {
            "amount": 1,
            "recipient": "d0e87a3f3c5445418e7d6ee0359da9de",
            "sender": "0"
        }
    ]
}
```

- `POST /transactions/new` - Create a new transaction

## Raw Body

```
{
    "sender": "300f5ab619c7629bb6ddcbdfe81b43488b51001957d9b76ebd5d77ef9502a560",
    "recipient": "03c6ef6e2569b715a098611a24df2a020f2a625746d2084f93d8373eab3b802a",
    "amount": 10
}
```

## Response

```
{
    "message": "Transaction will be added to Block 4"
}
```

- `POST /nodes/add_nodes` - Register new nodes

## Raw Body add node for port 5000

```
{
    "nodes": [
        "http://127.0.0.1:5000"
    ]
}
```

## Raw Body add node for port 5001

```
{
    "nodes": [
        "http://127.0.0.1:5001"
    ]
}
```

- `GET /nodes/sync` - Synchronize with other nodes

## Response sync body from node 5000

```
{
    "blockchain": [
        {
            "hash_of_previous_block": "a1c0749b5b39ae000916b037528fe92676b68cc28ce91dc6762e50698c98214e",
            "index": 0,
            "nonce": 130540,
            "timestamp": 1745243455.1048682,
            "transaction": []
        },
        {
            "hash_of_previous_block": "0dc3919efec82ed24b594f82d60fccf88e8b9be174985f97b217f3e4e6649a4d",
            "index": 1,
            "nonce": 92634,
            "timestamp": 1745243493.369519,
            "transaction": [
                {
                    "amount": 1,
                    "recipient": "d0e87a3f3c5445418e7d6ee0359da9de",
                    "sender": "0"
                }
            ]
        },
        {
            "hash_of_previous_block": "750181fbdd4f7b5b336ba216d89e05b1b8450ecab00cb942c8cfa9c28317cd20",
            "index": 2,
            "nonce": 25493,
            "timestamp": 1745243621.173444,
            "transaction": [
                {
                    "amount": 10,
                    "recipient": "03c6ef6e2569b715a098611a24df2a020f2a625746d2084f93d8373eab3b802a",
                    "sender": "300f5ab619c7629bb6ddcbdfe81b43488b51001957d9b76ebd5d77ef9502a560"
                },
                {
                    "amount": 1,
                    "recipient": "d0e87a3f3c5445418e7d6ee0359da9de",
                    "sender": "0"
                }
            ]
        },
        {
            "hash_of_previous_block": "6d0631f570c6a1d261aae0629faa1f0fbd4001add8777c7c2731c9f02f25ef8d",
            "index": 3,
            "nonce": 181521,
            "timestamp": 1745245031.018613,
            "transaction": [
                {
                    "amount": 1,
                    "recipient": "d0e87a3f3c5445418e7d6ee0359da9de",
                    "sender": "0"
                }
            ]
        }
    ],
    "message": "Our blockchain is already up to date"
}
```

## Response sync body from node 5001

```
{
    "chain": [
        {
            "hash_of_previous_block": "a1c0749b5b39ae000916b037528fe92676b68cc28ce91dc6762e50698c98214e",
            "index": 0,
            "nonce": 130540,
            "timestamp": 1745243455.1048682,
            "transaction": []
        },
        {
            "hash_of_previous_block": "0dc3919efec82ed24b594f82d60fccf88e8b9be174985f97b217f3e4e6649a4d",
            "index": 1,
            "nonce": 92634,
            "timestamp": 1745243493.369519,
            "transaction": [
                {
                    "amount": 1,
                    "recipient": "d0e87a3f3c5445418e7d6ee0359da9de",
                    "sender": "0"
                }
            ]
        },
        {
            "hash_of_previous_block": "750181fbdd4f7b5b336ba216d89e05b1b8450ecab00cb942c8cfa9c28317cd20",
            "index": 2,
            "nonce": 25493,
            "timestamp": 1745243621.173444,
            "transaction": [
                {
                    "amount": 10,
                    "recipient": "03c6ef6e2569b715a098611a24df2a020f2a625746d2084f93d8373eab3b802a",
                    "sender": "300f5ab619c7629bb6ddcbdfe81b43488b51001957d9b76ebd5d77ef9502a560"
                },
                {
                    "amount": 1,
                    "recipient": "d0e87a3f3c5445418e7d6ee0359da9de",
                    "sender": "0"
                }
            ]
        }
    ],
    "length": 3
}
```
