# fss-fileEncryption
Fast Simple Strong AES256-CBC Cryptography tool
```
usage: fss.py [-h] [-c] mode input output

positional arguments:
  mode             Encrypt= e & Decrypt= d
  input            Input file to encrypt or decrypt it
  output           Output of file to save results

optional arguments:
  -h, --help       show this help message and exit
  -c, --chunk  size of data chunks used in ENCRYPTION! (default 256 byte
                   per chunk)


```



* # Encrypting:
```
:~# ./fss.py e data.sth data.sth.enc -c 1024
> Password: Ex4mpl3_P@$$word
>
Encrypting block: bcb81737eab536d9d8d4c2855ec00cc79d620c6834e73cf8dbb5b5171b7e4c9f  block size 1024 ----> 1072
Encrypting block: 2661c90b845a3a2f8f206bd41448bdd7811166e9a0d36b02b4f9708368291c98  block size 1024 ----> 1072
Encrypting block: 1ec10b2a9974a98f6fc58e8d59e845a0ce85329c812092d33f63a31b71f511a8  block size 1024 ----> 1072
Encrypting block: bbdd3d87e62450c21df0507ce9525e662f02d39c40616794062dbcd827f0691d  block size 1024 ----> 1072
Encrypting block: ef373ade7cca8b9bcf5035df67c7851fa03052b263c7b1a0ff32800ee8bc88e7  block size 1024 ----> 1072
Encrypting block: d10f3fd38d3aedd112fcf5cda0181822d743ad0b66c8d9b6f4bc06d58101e73a  block size 1024 ----> 1072
Encrypting block: da3a739e427dfe09105adcac5a417bc9b9e9831864e6cd8df710982f8c4efb93  block size 1024 ----> 1072
Encrypting block: 671859bae8dcebbe9fb7034edc3053a2bb3049f5243cf757741d9f87c7a87652  block size 1024 ----> 1072
Encrypting block: d077edad71761c3a6857ca31323c00ab4280c77f231a1b9f06fa9dbf7eebea71  block size 1024 ----> 1072
Encrypting block: 0bad6307db2dfb5b5adfe4d75552e685b688156702e77dc75a202f4a234e66b4  block size 1024 ----> 1072

Encryption finished:

 size before encryption: 900515

 size after encryption: 942752
```


# Decrypting:
```
:~# ./fss.py d data.sth.enc data_new.sth -c 1024
> Password: Ex4mpl3_P@$$word
>
Decrypting block: bcb81737eab536d9d8d4c2855ec00cc79d620c6834e73cf8dbb5b5171b7e4c9f  block size 1072 ----> 1024
Decrypting block: 2661c90b845a3a2f8f206bd41448bdd7811166e9a0d36b02b4f9708368291c98  block size 1072 ----> 1024
Decrypting block: 1ec10b2a9974a98f6fc58e8d59e845a0ce85329c812092d33f63a31b71f511a8  block size 1072 ----> 1024
Decrypting block: bbdd3d87e62450c21df0507ce9525e662f02d39c40616794062dbcd827f0691d  block size 1072 ----> 1024
Decrypting block: ef373ade7cca8b9bcf5035df67c7851fa03052b263c7b1a0ff32800ee8bc88e7  block size 1072 ----> 1024
Decrypting block: d10f3fd38d3aedd112fcf5cda0181822d743ad0b66c8d9b6f4bc06d58101e73a  block size 1072 ----> 1024
Decrypting block: da3a739e427dfe09105adcac5a417bc9b9e9831864e6cd8df710982f8c4efb93  block size 1072 ----> 1024
Decrypting block: 671859bae8dcebbe9fb7034edc3053a2bb3049f5243cf757741d9f87c7a87652  block size 1072 ----> 1024
Decrypting block: d077edad71761c3a6857ca31323c00ab4280c77f231a1b9f06fa9dbf7eebea71  block size 1072 ----> 1024
Decrypting block: 0bad6307db2dfb5b5adfe4d75552e685b688156702e77dc75a202f4a234e66b4  block size 1072 ----> 1024

 Decryption finished:

 size before encryption: 942752

 size after encryption: 900515
```
# Note:

you can use any chunk size you want, but be reasonable about your choices

the default 256 chunk size is okay up to 6 mb

my suggestion for chunk size is:  `64 < x < 8192`

you can use bigger chunk size for faster result

Keep in mind this mini-program is just a very simple example for who seeking cryptography lessons

Dont use this for sensitive data or veryBigFiles like more than 2Gb
