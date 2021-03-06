from argparse import ArgumentParser
from binascii import a2b_hex
from struct import unpack
from functions import *
from bitcoin import scriptaddr, deserialize, serialize, \
                    multisign, is_privkey,  mktx

p = ArgumentParser(description='OP_CHECKLOCKTIMEVERIFY tx creator !')
p.add_argument('locktime', type=int, help='nLockTime')
p.add_argument('privkey', action='store', help='WIF Private Key')
p.add_argument('address', action='store', help='Output address')
args = p.parse_args()

def main():
    locktime = args.locktime
    privkey = args.privkey
    address = args.address

    script = getRedeemScript(locktime, privkey)
    ins, balance = getBalance(scriptaddr(script, 50))
    len_inputs = len(ins)

    tx = ''

    if balance > 0 and check_addr(address) and is_privkey(privkey):
        # Fee
        fee = round(base_fee + fee_per_input * len_inputs, 8)

        # Outputs
        out_value = int((balance - fee) * COIN)
        outs = [{'address' : address, 'value' : out_value}]

        # Make unsigned transaction
        tx = mktx(ins, outs)

        # Append nLockTime and reset nSequence
        unpacked = deserialize(tx)
        unpacked['locktime'] = locktime
        for i in range(len_inputs):
            unpacked['ins'][i]['sequence'] = 0
        tx = serialize(unpacked)

        # get all signatures
        sigs = []
        for i in range(len_inputs):
            sigs.append(multisign(tx, i, script, privkey))

        # sign inputs
        unpacked = deserialize(tx)
        for i in range(len_inputs):
            unpacked['ins'][i]['script'] = getLen(sigs[i]) + sigs[i]
            unpacked['ins'][i]['script'] += getLen(script) + script
        tx = serialize(unpacked)

    print('> BALANCE (%s): %f' % (scriptaddr(script, 50), balance))

    if len(tx) > 0:
        txid = broadcast(tx)
        print('> RESPONSE: %s' % txid.text)

if __name__ == '__main__':
    main()
