from detectors import *
from decoders import *

def find_approach(content,l=0,md5=''):
	nl=l+1
	if l>10:
		print("Too deep--------------------------------Too deep--------------------------------Too deep")
		return []
	if type(content)==str:
		content=content.encode('utf-8')
	if md5=='':
		md5=binascii.hexlify(encode_md5(content)).decode('utf-8')
	types = detect(content)	
	methods = lookup_method(types)
	print(str(l)+indent(l)+" Types: "+str(types))
	print(str(l)+indent(l)+" Methods: "+str(methods))
	if methods==[]:
		approach = []
	else:
		for method in methods:
			print(str(l)+indent(l)+" Working with method: "+method)
			if "solved" in method:
				approach = [method]
				break
			else:
				newcontent = decode(content, method, md5)
				if newcontent == b'':
					approach = []
				else:
					newapproach = find_approach(newcontent,nl,md5)
					print(str(l)+indent(l)+" New approach: "+str(newapproach))
					if solvedapproach(newapproach):
						if "remove_spaces" in newapproach[len(newapproach)-2]:
							approach = [method]+["solved-onlyhex"]
						else:
							approach = [method]+newapproach
						break
					else:
						if "decode_hex" in method:
							approach = ["solved-onlyhex"]
	if solvedapproach(approach) and "remove_first8" in approach:
		approach[len(approach)-1]="solved-neediv"
	print(str(l)+indent(l)+ " Returning: "+str(approach))
	return approach
	
def detect(content):
	types = []
	if detect_utf8(content):
		print("Detected utf8")
		if detect_spaces(content):
			print("Detected spaces")
			if detect_binary_w_spaces(content):
				print("Detected binary_w_spaces")
				types.append("binary_w_spaces")
			elif detect_binary_w_other(content):
				print("Detected binary_w_other")
				types.append("binary_w_other")
			elif detect_hex_w_spaces(content):
				print("Detected hex_w_spaces")
				types.append("hex_w_spaces")
			elif detect_hexlike_w_spaces(content):
				print("Detected hexlike_w_spaces")
				types.append("hexlike_w_spaces")
			else:
				print("Must be utf8")
				types.append("utf8")
		else:
			print("No spaces")
			if detect_binary(content):
				print("Detected binary")
				types.append("binary")
			elif detect_hex(content):
				print("Detected hex")
				types.append("hex")
			elif detect_hexlike(content):
				print("Detected hexlike")
				types.append("hexlike")
			elif detect_mult4(content):
				print("Detected mult4")
				if detect_base64(content):
					print("Detected base64")
					types.append("base64")
				else:
					print("Must be utf8")
					types.append("utf8")
			else:
				print("Must be utf8")
				types.append("utf8")
	elif detect_utf8end(content):
		print("Detected utf8end")
		types.append("utf8end")
	elif detect_mult8(content):
		print("Detected mult8")
		types.append("mult8")
	return types

def lookup_method(types):
	methods=[]
	if ("utf8" in types) and not("hexlike_w_spaces" in types) and not("hexlike" in types) and not("hex_w_spaces" in types) and not("hex" in types) and not("base64" in types):
		methods=["solved"]
	elif ("utf8end" in types):
		methods.append("remove_first8")
	else:
		for type in types:
			if type=="binary":
				methods.append("decode_binary")
			if type=="binary_w_other":
				methods.append("remove_other")
			if type=="binary_w_spaces":
				methods.append("rotate_breaks")
			if type=="hex_w_spaces" or type=="hexlike_w_spaces" or type=="binary_w_spaces":
				methods.append("remove_spaces")
			if type=="hex":
				methods.append("decode_hex")
			if type=="hexlike":
				methods.append("decode_hexlike")
			if type=="base64":
				methods.append("decode_base64")
			if type=="mult8":
				methods.append("decode_des3ecb")
				methods.append("decode_des3cbc")
	return methods
	
def decode(content, method, md5=''):
	if method=="solved":
		return content
	if method=="remove_spaces":
		return remove_spaces(content)
	if method=="decode_hex":
		return decode_hex(content)
	if method=="decode_hexlike":
		return decode_hexlike(content)
	if method=="decode_base64":
		return decode_base64(content)
	if method=="decode_des3ecb":
		return decode_des3ecb(content,md5)
	if method=="decode_des3cbc":
		return decode_des3cbc(content,md5)
	if method=="remove_first8":
		return remove_first8(content)
	if method=="rotate_breaks":
		return rotate_breaks(content)
	if method=="decode_binary":
		return decode_binary(content)
	if method=="remove_other":
		return remove_other(content)
	return ""
	
def solve(content, approach=[], md5=''):
	if approach==[]:
		approach=find_approach(content)
	if type(content)==str:
		content=content.encode('utf-8')
	if md5=='':
		md5=binascii.hexlify(encode_md5(content)).decode('utf-8')
	if solvedapproach(approach):
		solution = content
		for method in approach:
			solution = decode(solution, method, md5)
		if "remove_first8" in approach:
			solution = b"????????"+solution
	else:
		solution=b""
	return solution
	
	
	
def find_keys(content, approach, md5=''):
	if type(content)==str:
		content=content.encode('utf-8')
	if md5=='':
		md5=binascii.hexlify(encode_md5(content)).decode('utf-8')
	keys=[]
	solution=content
	for method in approach:
		if "des3ecb" in method:
			key=find_key_des3ecb(solution,md5)
			keys.append(key)
		if "des3cbc" in method:
			key=find_key_des3cbc(solution,md5)
			keys.append(key)
		solution = decode(solution, method)
	return keys

def solvedapproach(approach):
	return len(approach)>0 and ("solved" in approach[len(approach)-1])
	
def indent(l):
	indent=""
	for i in range(0,l):
		indent+="\t"
	return indent