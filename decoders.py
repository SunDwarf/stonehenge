import binascii
import base64
from unidecode import unidecode
from Crypto.Cipher import DES3
from Crypto.Hash import MD5

def remove_spaces(text): # returns string
	return text.replace(" ","")
	
def hex2num(text): # returns value
	return binascii.unhexlify(text)

def decode_ascii(val): # returns string
	try:
		result = str(val,encoding='ascii')
	except UnicodeDecodeError:
		result = ''
	return result

def encode_ascii(text): # returns value
	return text.encode('ascii')

def decode_utf8(val): # returns string
	try:
		result = str(val,encoding='utf-8')
	except UnicodeDecodeError:
		result = ''
	return result
	
def encode_utf8(text): # returns value
	return text.encode('utf-8')

def decode_b64(val): # returns value
	return base64.b64decode(val)
	
def encode_b64(val): # returns value
	return base64.b64encode(val)
	
def encode_md5(val): # returns value
	m = MD5.new()
	m.update(val)
	return m.digest()

def decode_des3_ecb(ct, key): # takes values, returns value
	d = DES3.new(key,DES3.MODE_ECB)
	return d.decrypt(ct)

def decode_des3_cbc(ct, key, iv): # takes values, returns value
	d = DES3.new(key,DES3.MODE_CBC, iv)
	return d.decrypt(ct)

def add_n_after_20(text): # returns string
	result = ""
	for i in range(0, len(text)):
		result+=text[i]
		if (i+1)%20 == 0:
			result+='\n'
	return result
	
def utf2ascii(text): # returns text
	return unidecode(text)
	
def get_first8(val): # returns value
	return val[:8]

def remove_first8(val): # returns value
	return val[len(val)-8:]