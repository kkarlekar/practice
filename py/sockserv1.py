"""
Thread pool extensions to SocketServer.
"""


import Queue
import socket
import SocketServer
import sys
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
		



class ThreadPoolMixin:
    """
    Mixin to use a fixed pool of threads to handle requests.
    .. note::
       When shutting down the server, please ensure you call this mixin's
       `join()` to shut down the pool along with the server's `shutdown()`
       method. The order in which these are performed is not significant,
       but both actions must be performed.
    """

    # Size of pool.
    pool_size = 100

    # How long to wait on an empty queue, in seconds. Can be a float.
    timeout_on_get = 0.5

    def __init__(self):
        self._request_queue = Queue.Queue(self.pool_size)
        # This beastie serves a different purpose than __shutdown_request
        # and __is_shut_down: those are superprivate so we can't touch them,
        # and even if we could, they're not really useful in shutting down
        # the pool.
        self._shutdown_event = threading.Event()
        for _ in xrange(self.pool_size):
            thread = threading.Thread(target=self.process_request_thread)
            thread.setDaemon(1)
            thread.start()

    def process_request_thread(self):
        """Same as in BaseServer, but as a thread."""
        while True:
            try:
                request, client_address = self._request_queue.get(
                    timeout=self.timeout_on_get,
                )
            except Queue.Empty:
                # You wouldn't believe how much crap this can end up leaking,
                # so we clear the exception.
                sys.exc_clear()
                if self._shutdown_event.isSet():
                    return
                continue
            try:
                self.finish_request(request, client_address)
                self.shutdown_request(request)
            except:
                self.handle_error(request, client_address)
                self.shutdown_request(request)
            self._request_queue.task_done()

    def process_request(self, request, client_address):
        """Queue the given request."""
        self._request_queue.put((request, client_address))

    def join(self):
        """Wait on the pool to clear and shut down the worker threads."""
        # A nicer place for this would be shutdown(), but this being a mixin,
        # that method can't safely do anything with that method, thus we add
        # an extra method explicitly for clearing the queue and shutting
        # down the workers.
        self._request_queue.join()
        self._shutdown_event.set()


class ThreadPoolTCPServer(ThreadPoolMixin, SocketServer.TCPServer):
    """Implementation of TCPServer with a thread pool for incoming requests."""

    def __init__(self, server_address, request_class, bind_and_activate=True):
        ThreadPoolMixin.__init__(self)
        SocketServer.TCPServer.__init__(
            self,
            server_address,
            request_class,
            bind_and_activate)


class ThreadPoolUDPServer(ThreadPoolMixin, SocketServer.UDPServer):
    """Implementation of UDPServer with a thread pool for incoming requests."""

    def __init__(self, server_address, request_class):
        ThreadPoolMixin.__init__(self)
        SocketServer.UDPServer.__init__(self, server_address, request_class)

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

	ThreadPoolTCPServer.allow_reuse_address = True
	server = ThreadPoolTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
	ip, port = server.server_address
	server.join()
	server.shutdown()

