import socket
import os
from _thread import *
import mysql.connector

# for crc

def xor(a, b):
   
	# initialize result
	result = []
   
	# Traverse all bits, if bits are
	# same, then XOR is 0, else 1
	for i in range(1, len(b)):
		if a[i] == b[i]:
			result.append('0')
		else:
			result.append('1')
   
	return ''.join(result)
   
   
# Performs Modulo-2 division
def mod2div(divident, divisor):
   
	# Number of bits to be XORed at a time.
	pick = len(divisor)
   
	# Slicing the divident to appropriate
	# length for particular step
	tmp = divident[0 : pick]
   
	while pick < len(divident):
   
		if tmp[0] == '1':
   
			# replace the divident by the result
			# of XOR and pull 1 bit down
			tmp = xor(divisor, tmp) + divident[pick]
   
		else:   # If leftmost bit is '0'
  
			# If the leftmost bit of the dividend (or the
			# part used in each step) is 0, the step cannot
			# use the regular divisor; we need to use an
			# all-0s divisor.
			tmp = xor('0'*pick, tmp) + divident[pick]
   
		# increment pick to move further
		pick += 1
   
	# For the last n bits, we have to carry it out
	# normally as increased value of pick will cause
	# Index Out of Bounds.
	if tmp[0] == '1':
		tmp = xor(divisor, tmp)
	else:
		tmp = xor('0'*pick, tmp)
   
	checkword = tmp
	return checkword
   
# Function used at the sender side to encode
# data by appending remainder of modular division
# at the end of data.
def encodeData(data, key):
   
	l_key = len(key)
   
	# Appends n-1 zeroes at end of data
	appended_data = data + '0'*(l_key-1)
	remainder = mod2div(appended_data, key)
   
	# Append remainder in the original data
	codeword = data + remainder
	return codeword



mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="udp")

mycursor = mydb.cursor()

mycursor.execute("select * from client")
result = mycursor.fetchall()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '192.168.0.112'
port = 4000
ThreadCount = 0

try:
	s.bind((host, port))
except socket.error as e:
	print(str(e))

print('Waitiing for a Connection..')


# def threaded_client(addr, data, myres):
#     while True:
#         # bdata = input("-> ")
#         car = [myres[1], myres[2]]
#         caddr = tuple(car)
#         sdata = "data sent to the other device"
#         s.sendto(data.encode('utf-8'), caddr)
#         s.sendto(sdata.encode('utf-8'), addr)

#     # myres[1], myres[2].close()
#     addr.close()


dt, ad = s.recvfrom(1024)
while True:
	input_string = input("Enter data you want to send->")
	idata =(''.join(format(ord(x), 'b') for x in input_string))
	print (idata)
	key = "1001"
	ans = encodeData(idata,key)
	print(ans)  
	s.sendto(ans.encode('utf-8'),ad)

	data, address = s.recvfrom(1024)
	ad = address[0]
	print(ad, type(ad))
	if (any(ad in i for i in result)):
		print("ip is present in Database")
	else:
		sql = "INSERT INTO client (ip_addr,port) VALUES(%s,%s)"
		val = (address[0], address[1])
		mycursor.execute(sql, val)
		mydb.commit()
		print("ip saved in database...")

	mycursor.execute("SELECT * FROM client WHERE ip_addr = %s", (ad,))
	myresult = mycursor.fetchone()
	cs = myresult[3]
	mycursor.execute("SELECT * FROM client WHERE c_id = %s", (cs,))
	myres = mycursor.fetchone()


	data = data.decode('utf-8')
	print("From connected user" + str(address[0]) + str(address[1]) + " : " + data)

	# s.sendto(data.encode('utf-8'), (myres[1], myres[2]))
	# sdata = "data sent to the other device"
	# s.sendto(sdata.encode('utf-8'), address)


	# s.send(,address)
	# start_new_thread(threaded_client, (address, data, myres))
	# ThreadCount += 1
	# print('Thread Number: ' + str(ThreadCount))

s.close()
