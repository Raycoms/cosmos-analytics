import time

import requests
import bech32
import hashlib
import base64

from cosmos.apikeys import api_keys


def bech32_to_base64(bech32_address):

    # Decode the Bech32 address to raw bytes
    hrp, data = bech32.bech32_decode(bech32_address)
    raw_bytes = bech32.convertbits(data, 5, 8, pad=False)

    return base64.b64encode(bytes(raw_bytes)).decode('utf-8')
start = 22877994 #21983096
end = 22983096

f = open("tx2.txt", "a")


index = 0;

ignore = ['/ibc.core.client.v1.MsgUpdateClient', '/ibc.core.channel.v1.MsgAcknowledgement', '/cosmos.gov.v1beta1.MsgVote', '/ibc.core.channel.v1.MsgRecvPacket']

for i in range(start, end):
    suffix1 = f"/cosmos/tx/v1beta1/txs/block/{i}"

    #todo: try catch around this
    response = None
    try:
        response = requests.request("GET", api_keys[index % len(api_keys)] + suffix1, headers={}, data={})
    except:
        print("woopsy")
        api_keys.pop(index % len(api_keys))

    if response.status_code == 429:
        print(api_keys[index % len(api_keys)])
        api_keys.pop(index % len(api_keys))

    index += 1
    while not response or response.status_code != 200:
        time.sleep(0.075)
        try:
            response = requests.request("GET", api_keys[index % len(api_keys)] + suffix1, headers={}, data={})
        except:
            print("woopsy")
            api_keys.pop(index % len(api_keys))
        index += 1


    #txs-> body->messages->
    #@type = '/ibc.applications.transfer.v1.MsgTransfer'
    # token->amount (only if "uatom")

    #'/cosmos.bank.v1beta1.MsgSend'
    # amount-> (only if "uatom")
    # amount-> {'amount': '150000000', 'denom': 'ibc/F663521BF1836B00F5F177680F74BFB9A8B5654A694D0D2BC249E03CF2509013'}

    # value translation = 1090 -> 0.001090 (remove 6 zeros)

    # Append all the validator addresses that voted for this block here.

    jsonresponse = response.json()
    blocktime = jsonresponse['block']['header']['time']

    thisblockamount = 0

    for tx in jsonresponse['txs']:
        for msg in tx['body']['messages']:
            if msg['@type'] == '/ibc.applications.transfer.v1.MsgTransfer':
                if msg['token']['denom'] == 'uatom':
                    thisblockamount += float(msg['token']['amount']) / 1000000 * 4.5
                elif msg['token']['denom'] == 'ibc/F663521BF1836B00F5F177680F74BFB9A8B5654A694D0D2BC249E03CF2509013':
                    thisblockamount += float(msg['token']['amount']) / 1000000
                else:
                    print(f"xxx denom1: {msg['token']['denom']}")
            elif msg['@type'] == '/cosmos.bank.v1beta1.MsgSend':
                for amnt in msg['amount']:
                    if amnt['denom'] == 'uatom':
                        thisblockamount += float(amnt['amount']) / 1000000 * 4.5
                    elif amnt['denom'] == 'ibc/F663521BF1836B00F5F177680F74BFB9A8B5654A694D0D2BC249E03CF2509013':
                        thisblockamount += float(amnt['amount']) / 1000000
                    else:
                        print(f"xxx denom2: {amnt['denom']}")
            elif msg['@type'] == '/cosmos.bank.v1beta1.MsgMultiSend':
                for amnt in msg['outputs']:
                    for coins in amnt['coins']:
                        if coins['denom'] == 'uatom':
                            thisblockamount += float(coins['amount']) / 1000000 * 4.5
                        elif coins['denom'] == 'ibc/F663521BF1836B00F5F177680F74BFB9A8B5654A694D0D2BC249E03CF2509013':
                            thisblockamount += float(coins['amount']) / 1000000
                        else:
                            print(f"xxx denom2: {coins['denom']}")
            elif "Transfer" in msg['@type'] or "Send" in msg['@type']:
                print(f"--------------------------------------------------- {msg['@type']}")


    print(f"{i} {blocktime} {thisblockamount}")
    f.write(f"{i} {blocktime} {thisblockamount}\n")

    # Cycle through naturally as well, not only on failure
    index += 1

f.close()
#print(response.text)



