#! /usr/bin/env python3.6

import argparse
import hashlib

import os
import shutil

import time
from Crypto import Random
from Crypto.Cipher import AES

from termcolor import colored


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


def how_long_per_chunk(chunksize):
    toenc = b"" * chunksize
    c = AESCipher("password")
    ts = time.time()
    s = c.encrypt(toenc)
    tt = time.time() - ts
    return tt / 10


def getpassword(filename, mode, chunk):
    if mode == "e":
        mode = "encrypting"
    elif mode == "d":
        mode = "decrypting"

    # main calc
    file_size = os.path.getsize(filename)
    print("\n\n")
    if len(str(file_size)) <= 3:  # less than kilo byte
        print(colored(" Suggested chunk size: ", color="yellow") + "64 - 128")

    elif len(str(file_size)) > 3:  # less than mega byte
        if len(str(file_size)) <= 6:  # mega byte
            print(colored(" Suggested chunk size: ", color="yellow") + "256 - 512")
        elif len(str(file_size)) > 6:
            if len(str(file_size)) < 10:
                print(colored(" Suggested chunk size: ", color="yellow") + "1024 - 2048")
            else:
                print("\n what a huge file! ;)" + colored("\n Suggested chunk size: ", color="yellow") + "+4069")

    number_of_chunks = file_size / chunk
    time_per_chunk = how_long_per_chunk(chunk)
    total_time = perrty_time_to_sec(number_of_chunks * time_per_chunk)
    print("\n Estimated time for " + mode + " " + colored(filename, color="yellow") + " is about: " + colored(
        str(total_time), color="red") + colored("  [85% True time]", color="green"))
    while True:
        password = input("\n Password: ")
        if len(password) >= 8:
            if password is not None:
                return password
        else:
            print("\nDont use shitty password password should be greater than 8 chars\n")


def perrty_time_to_sec(time_in_sec):
    # 1.23 sec
    sec = str(time_in_sec).split(".")[0]
    less_than_sec = str(time_in_sec).split(".")[1]
    lts = int(less_than_sec[:2])
    lts_mil = round(float(less_than_sec[3] + "." + less_than_sec[3:]))

    return sec + "." + str(lts + lts_mil) + " sec"


def better_size(size_in_byte, dont_rount=False):
    if dont_rount:
        if len(str(size_in_byte)) > 3:  # kilo
            if len(str(size_in_byte)) > 6:  # mega
                s = str(size_in_byte)[:len(str(size_in_byte)) - 6]
                s = s + "." + str(size_in_byte)[len(s):] + " Mb"
                return s
            else:
                s = str(size_in_byte)[:len(str(size_in_byte)) - 3]
                s = s + "." + str(size_in_byte)[len(s):] + " Kb"
                return s
        else:
            return str(size_in_byte) + " byte"
    # do round
    else:
        if len(str(size_in_byte)) > 3:  # kilo
            if len(str(size_in_byte)) > 6:  # mega
                s = str(size_in_byte)[:len(str(size_in_byte)) - 6]
                s = s + "." + str(size_in_byte)[len(s):]
                s = round(float(s))
                return str(s) + " Mb"
            else:
                s = str(size_in_byte)[:len(str(size_in_byte)) - 3]
                s = s + "." + str(size_in_byte)[len(s):]
                s = round(float(s))
                return str(s) + " Kb"
        else:
            return colored(str(size_in_byte) + " byte", color="green")


def enc(file_in, file_out, chunk):
    password = getpassword(file_in, "e", chunk)
    size_before = 0
    size_after = 0
    cipher = AESCipher(password)
    if os.path.isfile(file_out):  # if result location is already in use
        shutil.move(file_out, file_out + ".backup")
    try:
        ts = time.time()
        with open(file_in, "rb") as fr:
            with open(file_out, "ab") as fo:
                while True:
                    block = fr.read(chunk)  # byte format
                    if block:
                        size_before += len(block)
                        ciphered_block = cipher.encrypt(block)  # take byte gives string
                        print("Encrypting block: " + colored(ciphered_block[:16].hex(),
                                                             color="green") + "  block size " + str(
                            len(block)) + " ----> " + str(len(ciphered_block)))
                        fo.write(ciphered_block)
                        size_after += len(ciphered_block)
                    else:
                        fo.close()
                        fr.close()
                        break
                print("\n\nEncryption finished:\n\nTotal time: " + perrty_time_to_sec(
                    time.time() - ts) + "\nsize before encryption: " +
                      better_size(size_before, True) + "\nsize after encryption: " + better_size(size_after,
                                                                                                 True) + "\n\n")
    except Exception as e:
        pass


def dec(file_in, file_out, dec_chunk):
    ts = time.time()
    password = getpassword(file_in, "d", dec_chunk)
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
                        print("Decrypting block: " + colored(block[:16].hex(), color="green") + "  block size " + str(
                            len(block)) + " ----> " + str(len(deced)))
                        fo.write(deced)
                        size_after += len(deced)
                    else:
                        fo.close()
                        fr.close()
                        break
                print("\n\nDecryption finished:\n\nTotal time: " + perrty_time_to_sec(
                    time.time() - ts) + "\nsize before decryption: " +
                      better_size(size_before, True) + "\nsize after decryption: " + better_size(size_after,
                                                                                                 True) + "\n\n")
    except Exception as e:
        pass


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
    enc(args.input, args.output, args.chunk)
elif args.mode == "d":
    dec(args.input, args.output, dec_chunk)
