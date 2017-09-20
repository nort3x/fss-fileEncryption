import argparse
import hashlib

import os
import shutil

from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):
    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + ((self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)).encode()

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


def getpassword():
    while True:
        password = input("Password: ")
        if len(password) >= 8:
            if password is not None:
                return password
        else:
            print("\nDont use shitty password password should be greater than 8 chars\n")


def enc(file_in, file_out, chunk):
    password = getpassword()
    size_before = 0
    size_after = 0
    cipher = AESCipher(password)
    if os.path.isfile(file_out):  # if result location is already in use
        shutil.move(file_out, file_out + ".backup")
    try:
        with open(file_in, "rb") as fr:
            with open(file_out, "ab") as fo:
                while True:
                    block = fr.read(chunk)  # byte format
                    if block:
                        size_before += len(block)
                        ciphered_block = cipher.encrypt(block)  # take byte gives string
                        print("Encrypting block: " + ciphered_block[:32].hex() + "  block size " + str(
                            len(block)) + " ----> " + str(len(ciphered_block)))
                        fo.write(ciphered_block)
                        size_after += len(ciphered_block)
                    else:
                        fo.close()
                        fr.close()
                        break
                print("\n\nEncryption finished:\nsize before encryption: " +
                      str(size_before) + "\nsize after encryption: " + str(size_after) + "\n\n")
    except Exception as e:
        print(e)


def dec(file_in, file_out, dec_chunk):
    password = getpassword()
    size_before = 0
    size_after = 0
    if os.path.isfile(file_out):  # if result location is already in use
        shutil.move(file_out, file_out + ".backup")
    cipher = AESCipher(password)
    try:
        with open(file_in, "rb") as fr:
            with open(file_out, "ab") as fo:
                while True:
                    block = fr.read(dec_chunk)  # byte format
                    if block:
                        size_before += len(block)
                        deced = cipher.decrypt(block)  # take byte gives byte
                        print("Decrypting block: " + block[:32].hex() + "  block size " + str(
                            len(block)) + " ----> " + str(len(deced)))
                        fo.write(deced)
                        size_after += len(deced)
                    else:
                        fo.close()
                        fr.close()
                        break
                print("\n\nDecryption finished:\nsize before encryption: " +
                      str(size_before) + "\nsize after encryption: " + str(size_after) + "\n\n")
    except Exception as e:
        print(e)


parser = argparse.ArgumentParser(description="  Simple AES256-cbc Cryptography tool ")
parser.add_argument("-c", "--chunk", metavar='\b',
                    help="size of data chunks used in ENCRYPTION! (default 256 byte per chunk)", default=256, type=int)
parser.add_argument("mode", help="   Encrypt= e & Decrypt= d")
parser.add_argument("input", help="  Input file to encrypt or decrypt it")
parser.add_argument("output", help="  Output of file to save results")
args = parser.parse_args()

# main handler
dec_chunk = args.chunk + (32 - (args.chunk % 32)) + 16  # ciphered + padding + IV
if args.mode == "e":
    enc(args.input, args.output,  args.chunk)
elif args.mode == "d":
    dec(args.input, args.output, dec_chunk)
