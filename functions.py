from binascii import hexlify
from struct import pack
from requests import get, post
from bitcoin import encode_pubkey, privtopub
from hashlib import sha256

# Opcodes
OP_CHECKLOCKTIMEVERIFY = 'b1'
OP_DROP = '75'
OP_CHECKSIG = 'ac'
COIN = 100000000

digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def broadcast(tx):
    url = 'https://explorer.cha.terahash.cl/api/tx/send'
    return post(url, data={'rawtx' : tx})

def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, 'big')

def check_addr(bc):
# http://rosettacode.org/wiki/Bitcoin/address_validation#Python
    try:
        bcbytes = decode_base58(bc, 25)
        return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
    except Exception:
        return False

def getRedeemScript(locktime, privkey):
    pubkey = encode_pubkey(privtopub(privkey), 'hex_compressed')

    # little-endian hex packing
    locktime = hexlify(pack('<i', locktime)).decode('utf-8')

    if locktime[6:] == '00':
        # locktime > 500.000.000 = block height
        locktime = '03' + locktime[:6]
    else:
        # locktime < 500.000.000 = timestamp
        locktime = '04' + locktime

    # 33 bytes hex-compressed pubkey
    pubkey = '21' + pubkey

    # PAY-TO-PUBKEY OP_CHECKLOCKTIMEVERIFY
    return locktime + OP_CHECKLOCKTIMEVERIFY + OP_DROP + pubkey + OP_CHECKSIG

def getBalance(addr):
    url = 'http://insight.chaucha.cl/api/addr/'
    unspent = get(url + addr + '/utxo').json()

    inputs = []
    balance = 0

    for i in unspent:
        if i['confirmations'] >= 6:
            input = {'output' : i['txid'] + ':' + str(i['vout']),
                     'value' : i['satoshis'],
                     'address' : i['address']}
            balance += i['satoshis']
            inputs.append(input)

    return [inputs, round(balance/COIN, 8)]

def getLen(string):
    return hex(int(len(string)/2))[2:]
