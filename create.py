from bitcoin import encode_pubkey, encode_privkey, \
                    scriptaddr, privtopub, is_privkey
from binascii import a2b_hex, hexlify
from hashlib import new
from struct import pack
from argparse import ArgumentParser

# Argument Parser
p = ArgumentParser(description='OP_CHECKLOCKTIMEVERIFY generator !')
p.add_argument('locktime', type=int, help='Block transaction until <locktime>')
p.add_argument('privkey', action='store', help='WIF Private Key')
args = p.parse_args()

# Opcodes
OP_CHECKLOCKTIMEVERIFY = 'b1'
OP_DROP = '75'
OP_CHECKSIG = 'ac'

def getRedeemScript(locktime, pubkey):
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

def main():
    # WIF Private key
    privkey = args.privkey

    if is_privkey(privkey):
        pubkey = encode_pubkey(privtopub(privkey), 'hex_compressed')
        # Block height
        locktime = args.locktime

        redeemscript = getRedeemScript(locktime, pubkey)

        # Bitcoin BIP-13 + Litecoin prefix
        p2sh_addr = scriptaddr(redeemscript, 50)

        print('> P2SH ADDRESS: %s' % p2sh_addr)
        print('> REDEEM SCRIPT: %s' % redeemscript)
    else:
        print('> ERROR - PRIVKEY FORMAT')

if __name__ == '__main__':
    main()
