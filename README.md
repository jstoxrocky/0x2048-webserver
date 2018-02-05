# 0x2048-frontend

The 0x2048 project is a decentralized game of 2048 played over a state channel between a server and users. 0x2048-webserver is the backend code hosting the server side endpoint logic for the the 0x2048 project. 


## 0x2048-Project

[Contracts](https://github.com/jstoxrocky/0x2048-contracts)

[Frontend](https://github.com/jstoxrocky/0x2048-frontend)

[Webserver](https://github.com/jstoxrocky/0x2048-webserver)

[Game](https://github.com/jstoxrocky/0x2048-game)


## Setup

```bash
S pip install -r requirements.txt
$ python setup.py install
```

## Run

```bash
$ python webserver/application.py
```

Endpoints are hosted at `http://localhost:5000/`

## Test

```bash
$ pytest
```
