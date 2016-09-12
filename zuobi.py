#coding=utf-8
#!/usr/bin/python
import urllib.request
import base64
from Crypto.Cipher import AES

iv = "5PLOEQ87Z5LM9K2U"
key = "L2HGM84N24V5UYRB"

f = urllib.request.urlopen('http://api.auto-learning.com/v3/guess-you-like')
dataBytes = f.read()
json = dataBytes.decode('utf8')
f.close()
de = base64.decodestring(dataBytes)

print(de)
# print(json)
# print(first)