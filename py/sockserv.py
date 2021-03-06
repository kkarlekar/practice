import SocketServer
import socket
import threading
import base64
import binascii


mystack = []
mystack_mutex = threading.Lock()
mystack_cond = threading.Condition(mystack_mutex)

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
	def processRequest(self, data):
		val = long(binascii.hexlify(data))
		if val == 80:
			mystack_mutex.acquire()
			while not mystack:
				mystack_cond.wait()
			print "pop op"
			print "pppp"
			try:
				pop_val = mystack.pop()
			finally:
				mystack_mutex.release()
			#l = "0x%02X" % len(pop_val)
			l = "%02X" % len(pop_val)
			print "length {}".format(l)
			try:
				self.request.send(binascii.a2b_hex(l))
				self.request.send(pop_val)
			except:
				print "sending of pop value failed"
		else:
			print "push op length {}".format(val)
			data = self.request.recv(val)
			mystack_mutex.acquire()
			try:
				if len(mystack) < 100:
					mystack.append(data)
					send_data = binascii.a2b_hex("00")
				else:
					send_data = binascii.a2b_hex("")
			finally:
				mystack_cond.notifyAll()
				mystack_mutex.release()
			self.request.send(send_data)
			print "data {}".format(data)


	def handle(self):
		data = self.request.recv(1)
		cur_thread = threading.current_thread()
		#response = "{}: {}".format(cur_thread.name, data)
		self.processRequest(data)
		


class  ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

def client(ip, port, message):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip, port))
	try:
		sock.sendall(message)
		response = sock.recv(1024)
		print "Received {}".format(response)
	finally:
		sock.close()

if __name__ == "__main__":
	HOST, PORT = "localhost", 8080

	ThreadedTCPServer.allow_reuse_address = True
	server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = False
	server_thread.start()

'''
	client(ip, port, "Hello World 1")
	client(ip, port, "Hello World 2")
	client(ip, port, "Hello world 3")
	server.shutdown()
'''


