from sys import exit
from Crypto.Util.number import bytes_to_long, inverse
# Local implementation of get_primes to avoid import error
import random

def get_primes(bits):
    """
    Generates two distinct random primes of specified bit length.
    """
    from Crypto.Util.number import getPrime
    p = getPrime(bits)
    q = getPrime(bits)
    while p == q:
        q = getPrime(bits)
    return p, q

e = 65537

def gen_key(k):
    """
    Generates RSA key with k bits
    """
    p,q = get_primes(k//2)
    N = p*q
    d = inverse(e, (p-1)*(q-1))

    return ((N,e), d)

def encrypt(pubkey, m):
    N,e = pubkey
    return pow(bytes_to_long(m.encode('utf-8')), e, N)

def main(flag):
    pubkey, _privkey = gen_key(1024)
    encrypted = encrypt(pubkey, flag) 
    return (pubkey[0], encrypted)

if __name__ == "__main__":
    flag = open('flag.txt', 'r').read()
    flag = flag.strip()
    N, cypher  = main(cypher=flag)
    print("N:", N)
    print("e:", e)
    print("cyphertext:", cypher)
    exit()

