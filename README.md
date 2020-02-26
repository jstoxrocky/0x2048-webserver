# 0x2048-webserver

The 0x2048 project is a decentralized game of 2048 played over a state channel between a server and users. 0x2048-webserver is the backend code hosting the server side endpoint logic for the the 0x2048 project. 


## 0x2048-Project

[Contracts](https://github.com/jstoxrocky/0x2048-contracts)

[Frontend](https://github.com/jstoxrocky/0x2048-frontend)

[Webserver](https://github.com/jstoxrocky/0x2048-webserver)

[Game](https://github.com/jstoxrocky/0x2048-game)


## Setup

```bash
$ pip install -r requirements.txt
$ python setup.py install
```

## Run

```bash
$ python setup.py install
$ python webserver/application.py
```

Endpoints are hosted at `http://localhost:5000/`

## Test

```bash
$ git submodule update --init --recursive
$ pytest
$ flake8
```


## Explanation
We assume that the API (webserver) and the client (frontend) do not trust eachother.

### Page Load
On page load, the client requests the game state and the arcade state. The game state is fetched from the API's Redis session cache and the arcade state is fetched from the arcade's Ethereum contract.

### Payment

#### API
When the client requests a new game, the API generates a random nonce and sends this to the client. The API stores this nonce in the client's Redis session cache.

#### Client
The client is expected to interact with a method in the Arcade's Ethereum contract that will (1) pay a fee, (2) store the client's Ethereum account address, and (3) store the nonce. The client is then expected to collect the transaction hash associated with the previous interaction with the Arcade's Ethereum contract, sign the nonce, and send back both the transaction hash and signed nonce to the API.

#### API
The API accepts a transaction hash and a signed value (nonce) from the client and extracts the signer's address from the signed value. The API then examines the transaction hash and waits for the transaction to be mined. When mining is successful, the API looks up the signer's address in the contract's mapping (address -> nonce) and confirms payment by ensuring that the signer's nonce in the contract matches the one stored in the Redis cache. At this point, the API has ensured that the client associated with the Redis session has paid the Arcade's Ethereum contract appropriately. The API flips the "paid" flag to "true" in the client's Redis session - allowing any gameplay to go forward.

### Gameplay

#### API
Upon payment confirmation, the API generates a blank game state and sends this to the client along with a signed message. The message is signed by the Arcade's private key and contains the client's Ethereum address (recovered from the initial signed nonce) and the client's current score in the game (initially zero). With each update of the game state via gameplay, the game's new state and is sent to the client along with an updated signed message.



docker build -t webserver . 
docker run -p 5000:5000 webserver