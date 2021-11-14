from os import getpid
import socket
from err import *
import threading
from requestparser import HTTPRequest
from response import *
import serverconfig
from time import sleep
from logs import logger
from datetime import datetime


DOCUMENT_ROOT = serverconfig.DOCUMENT_ROOT
PORT_NUMBER = serverconfig.PORT_NUMBER
COOKIE_LOG = 'cookie.txt'
MAX_CONNECTION = int(serverconfig.MAX_CONNECTION)

class TCPServer:

	def __init__(self, host, port):
		self.host = host
		self.port = port

	def connection(self,conn,addr):
		logger.debug(f'New thread{threading.active_count()} {addr}',{'process':os.getpid(),'thread':threading.get_ident()})
		time = 5
		while True:
			conn.settimeout(time)
			try:
				data = b""
				empty = 0
				while(len(data) == 0 and empty <= 10000):
					data = conn.recv(10000000)
					empty += 1
				if empty > 10000:
					conn.close()
					break
				
				headers = self.get_headers(data)
				content = headers["data"]
				headers['addr'] = addr
				isRequestTimeout = False
				if "Content-Length" in headers:
					isRequestTimeout = True
					length = int(headers["Content-Length"])
					while(length > len(content)):
						content += conn.recv(10000000)

				isRequestTimeout = False
				
				response,resource,isClose = self.handle_request(content,headers,data+content)
				
				# if isClose:
				# 	conn.send(response.encode('ISO-8859-1')+resource)
				# 	conn.close()
				# 	break	

				if resource:
					conn.send(response.encode('ISO-8859-1')+resource)
				else:
					conn.send(response.encode('ISO-8859-1'))

				if isClose:
					conn.close()
					break

				if "Connection" in headers and headers["Connection"] == "keep-alive":
					if 'Keep-Alive' in headers:
						time = int(headers['Keep-Alive'])
					else:
						time = 10
					continue
				else:
					conn.close()
					break

						
			except socket.timeout:
				if(isRequestTimeout):
					response,resource,isClose  = self.handle_request(None,headers,data+content)
					conn.send(response.encode('ISO-8859-1')+resource)
					conn.close()

				conn.close()
				break
		logger.debug(f'Finished{addr}',{'process':os.getpid(),'thread':threading.get_ident()})
		
      

	def start(self):
		logger.debug('SERVER STARTED',{'process':os.getpid(),'thread':threading.get_ident()})
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((self.host, int(self.port)))
		s.listen(10)
		
		#print("\nListening at", s.getsockname())
        
		while True:
			conn, addr = s.accept()
			#print("Connected by", addr)
			
			th = threading.Thread(target=self.connection,args=(conn,addr,))
			th.start()
			if threading.active_count() > MAX_CONNECTION:
				logger.debug('max-connections crossed , sleeping',{'process':os.getpid(),'thread':threading.get_ident()})
				sleep(3)
		


			
	def handle_request(self, data,headers,request):
		return data
	
	def get_headers(self,data):
		pass

        
class HTTPServer(TCPServer):
	def __init__(self, host='127.0.0.1', port=PORT_NUMBER,allowedMethods=['GET','HEAD','POST','PUT','DELETE']):
		self.allowedMethods = allowedMethods
		self.isService = True
		self.isSystemOk = True
		
		TCPServer.__init__(self,host,port)

	def get_headers(self,data):
		if b'\r\n\r\n' in data: 
			raw_data = data[:data.index(b"\r\n\r\n")]
			entity = data[data.index(b"\r\n\r\n")+4:]
		else:
			raw_data = data
			entity = b""
		http_req = HTTPRequest(raw_data.decode("ISO-8859-1"))
		http_req.headers_request["data"] = entity
		
		return http_req.headers_request

	def handle_request(self, data,headers_req,request):
		headers_req = headers_req
		headers_req["data"] = data

		isError, status_code = self.checkForErrors(headers_req,request.decode("ISO-8859-1"))
		
		if "Accept-Encoding" in headers_req:
			accept = headers_req["Accept-Encoding"]
			accept_options = accept.split(",")
			q_val = {}
			encoding_list = []
			for entry in accept_options:
				entry = entry.split(";")
				if(len(entry) == 1):
					q_val[entry[0]] = 1.0
				else:
					q_val[entry[0]] = float(entry[1].split('=')[1])
			encoding_list = [k for k,v in sorted(q_val.items(), key=lambda item: item[1],reverse=True)]

			headers_req["Accept-Encoding"] = encoding_list
			
		
		httpResponseObject = httpresponse(headers_req,isError,status_code)
		httpResponse,resource = httpResponseObject.build_response()

		sendResponse = httpResponse["protocol"] + " " + str(httpResponse["status_code"]) + " " + httpResponse["reason_phrase"] + "\r\n"
		for key,value in httpResponse["headers"].items():
			sendResponse += str(key)+": "+str(value)+"\r\n"
		
		close = False
		if 'Connection' in httpResponse["headers"] and httpResponse["headers"]["Connection"] == "Close":
			close = True
		sendResponse += "\r\n"
		#sendResponse = bytes(sendResponse,'utf-8')
	
		return sendResponse,resource,close
		
		
	def checkForErrors(self,headers_req, data):
		if(headers_req['request_line'][2] not in ['HTTP/1.1','HTTP/1.0']):
			return True,505
		elif(self.isService == False):
			return True,503
		elif (headers_req["data"] == None):
			return True,408
		elif(len((headers_req["request_line"])[1]) > 2000):
			return True,414
		elif(len((data.split("\r\n\r\n"))[0]) > 16000):
			return True,431
		elif(not self.isImplemented(headers_req)):
			return True,501
		elif(not self.isSystemOk):
			return True,500
		elif(not self.isMethodAllowed(headers_req["request_line"][0])):
			return True,405
		elif(self.isPayloadLarge(headers_req)):
			return True,413
		elif(self.isForbidden(headers_req)):
			return True,403
		elif(headers_req['request_line'][0] in ['POST','PUT'] and 'Content-Length' not in headers_req):
			return True,411
		
		'''
		elif(not self.checkExpect(headers_req)):
			return True,417
		elif(self.isBadrequest(headers_req)):
			return True,400
		elif(not self.isMediaTypeSupported(headers_req["Content-Type"], headers_req["Content_Encoding"])):
			return True,415
		elif("Expect" in headers_req and headers_req["Expect"] == "100-continue"):
			return False,100
		'''

		return False,None
		
		
	def isImplemented(self,headers_req):
		valid_headers = ["Accept",
		"Expect",
		"Accept-Language",
		"Accept-Charset",
		"Content-Encoding",
		"Accept-Encoding",
		"Content-Length",
		"Content-MD5",
		"Content-Type",
		"Content-Type",
		"Date",
		"Host",
		"If-Modified-Since",
		"If-Range",
		"If-Match",
		"If-Unmodified-Since",
		"Range",
		"User-Agent",
		"Accept-Ranges",
		"Content-Location",
		"ETag",
		"Expires",
		"Last-Modified",
		"Location",
		"Server",
		"Set-Cookie",
		"Cookie",
		"Transfer-Encoding",
		"Connection",
		"Referer",
		"Keep-Alive",
		"Postman-Token",
		"Allow"]
		
		headers_list = list(headers_req.keys())
		headers_list.remove("request_line")
		headers_list.remove("data")
		headers_list.remove("addr")
		for header in headers_list:
			if(header not in valid_headers):
				return False
		
		return True
	
	#def check_headers(
		
	def checkExpect(self,headers_req):
		return True
		
	def isMethodAllowed(self,method):
		if(method in self.allowedMethods):
			return True
		else :
			return False
	
	
	def isPayloadLarge(self,headers_req):
		if(headers_req["request_line"][0] == "HEAD"):
			return False
		elif(len(headers_req['data']) > 5000000):
			return True 

	def isMediaTypeSupported(self,Cont_type, cont_encod):
		return True

	def isForbidden(self,headers):
		return False
	
if __name__ == '__main__':
	server = HTTPServer()
	server.start()
    
    
