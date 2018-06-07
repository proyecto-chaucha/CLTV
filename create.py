from bitcoin import encode_pubkey, scriptaddr, is_privkey
from functions import getRedeemScript
from argparse import ArgumentParser
from binascii import a2b_hex

# Argument Parser
p = ArgumentParser(description='OP_CHECKLOCKTIMEVERIFY generator !')
p.add_argument('locktime', type=int, help='Block transaction until <locktime>')
p.add_argument('privkey', action='store', help='WIF Private Key')
args = p.parse_args()

def main():
    # WIF Private key
    privkey = args.privkey

    if is_privkey(privkey):
        # Block height
        locktime = args.locktime

        redeemscript = getRedeemScript(locktime, privkey)

        # Bitcoin BIP-13 + Litecoin prefix
        p2sh_addr = scriptaddr(redeemscript, 50)

        print('> P2SH ADDRESS: %s' % p2sh_addr)
        print('> REDEEM SCRIPT: %s' % redeemscript)
    else:
        print('> ERROR - PRIVKEY FORMAT')

if __name__ == '__main__':
    main()
