import time

import requests
import bech32
import hashlib
import base64

from apikeys import api_keys

def bech32_to_base64(bech32_address):

    # Decode the Bech32 address to raw bytes
    hrp, data = bech32.bech32_decode(bech32_address)
    raw_bytes = bech32.convertbits(data, 5, 8, pad=False)

    return base64.b64encode(bytes(raw_bytes)).decode('utf-8')
start = 22993189 #21983096
end = 23762850

f = open("output.txt", "a")


index = 0;

for i in range(start, end):
    suffix1 = f"/cosmos/base/tendermint/v1beta1/blocks/{i}"
    suffix2 = f"/cosmos/base/tendermint/v1beta1/validatorsets/{i}"

    #todo: try catch around this
    response = requests.request("GET", api_keys[index % len(api_keys)] + suffix1, headers={}, data={})
    index += 1
    while response.status_code != 200:
        time.sleep(0.075)
        print(response)
        response = requests.request("GET", api_keys[index % len(api_keys)] + suffix1, headers={}, data={})
        index += 1

    # Append all the validator addresses that voted for this block here.
    voters = []
    for vote in response.json()["sdk_block"]["last_commit"]["signatures"]:
        thevote = vote['validator_address']
        if thevote:
            voters.append(thevote)

    totalvotingpower = 0
    validators = {}
    params = {"pagination.limit": str(100)}
    while True:

        response = requests.get(api_keys[index % len(api_keys)] + suffix2, params)
        index += 1
        while response.status_code != 200:
            time.sleep(0.075)
            response = requests.get(api_keys[index % len(api_keys)] + suffix2, params)
            index += 1

        for validator in response.json()['validators']:
            localvotingpower = int(validator['voting_power'])
            totalvotingpower += localvotingpower
            address = bech32_to_base64(validator['address'])
            validators[address] = localvotingpower
            #print(address)

        total = int(response.json().get("pagination", {}).get("total"))
        if len(validators) >= total:
            break  # No more pages
        else:
            params["pagination.offset"] = str(len(validators))

    #print("-------------------")

    votingshare = 0
    whoopsies = 0
    for voter in voters:
        if voter in validators:
            votingshare += validators[voter]
        else:
            whoopsies+=1
            print(voter)

    print(f"{i} {votingshare/totalvotingpower} {len(voters)} {len(validators)} {whoopsies}")
    f.write(f"{i} {votingshare/totalvotingpower} {len(voters)} {len(validators)} {whoopsies}\n")

    # Cycle through naturally as well, not only on failure
    index += 1

f.close()
#print(response.text)



