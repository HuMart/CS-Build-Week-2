import hashlib
import requests
import sys
from uuid import uuid4
from timeit import default_timer as timer
import time
import random

HEADERS = {"Authorization": "Token 5eb6cf7b74fecb698b5a9d227cce7f23d013bedd"} 
URL = "https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof"
# MINE = "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/"


def valid_proof(last_proof, proof, difficulty):
    # last_h = hashlib.sha256(f"{last_proof}".encode()).hexdigest()

    num = f"{last_proof}{proof}".encode()
    num_h = hashlib.sha256(num).hexdigest()

    return num_h[:difficulty] == "0" * difficulty

def proof_of_work(last_proof, difficulty):
    
    proof = random.randrange(0,10000)

    while valid_proof(last_proof, proof, difficulty) is False:
        proof += 1
    
    print("proof found")
    print(proof)
    return proof   

if __name__ == '__main__':
    
    node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"

    coin_mined = 0

    if id == "NONAME\n":
        print("Yuo must change your name")
        exit()
    while True:
        r = requests.get(url=node + "/last_proof/", headers=HEADERS)
        res = r.json()
        print(res)
        new_proof = proof_of_work(res.get('proof'), res.get('difficulty'))
        time.sleep(res.get('cooldown'))

        post_res = {"proof": new_proof}

        r = requests.get(url = node + "/last_proof/", headers = HEADERS)
        res = r.json()
        print(res)

        time.sleep(res.get('cooldown'))

        r = requests.post(url=node + "/mine/", headers = HEADERS, json=post_res)
        res = r.json()
        print(res)

        time.sleep(res.get('cooldown'))

        if res.get('messages') == "New Block Forged":
            coin_mined += 1

            print("totalcoins: " + str(coin_mined))
        else:
            print(res.get("messages"))
