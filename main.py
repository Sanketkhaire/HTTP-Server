from os import getpid
import socket
from err import *
import threading
from requestparser import HTTPRequest
from response import *
import serverconfig
import logging
from logs import logger
from datetime import datetime


DOCUMENT_ROOT = serverconfig.DOCUMENT_ROOT
PORT_NUMBER = 12008
COOKIE_LOG = 'cookie.txt'

class TCPServer:

	def __init__(self, host, port):
		self.host = host
		self.port = port

	def connection(self,conn,addr):
		print("THREAD STARTED")
		print("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
		logger.debug('SERVER STARTED',{'process':os.getpid(),'thread':threading.get_ident()})
		conn.settimeout(10)
		
		while True:
			try:
				data = b""
				while(len(data) == 0):
					data = conn.recv(10000000)
				print("\nno ",data," no\n")
				headers = self.get_headers(data)
				content = headers["data"]
				if "Content-Length" in headers:
					length = int(headers["Content-Length"])
					while(length > len(content)):
						print("yes")
						content += conn.recv(10000000)
						print(len(content))
				headers['addr'] = addr
				response,resource = self.handle_request(content,headers,data+content)
				print("between")
				conn.send(response.encode('ISO-8859-1'))
				if resource:
					print("done")
					conn.send(resource)
				if "Connection" in headers and headers["Connection"] == "keep-alive":
					print("sssssssssssssssssssssssssssssssss")
					continue
				else:
					conn.close()
					break
						
			except socket.timeout:
				print("khaire")
				conn.close()
				break
      

	def start(self):

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((self.host, self.port))
		s.listen(10)
		
		print("Listening at", s.getsockname())
        
		while True:
			conn, addr = s.accept()
			print("Connected by", addr)
			th = threading.Thread(target=self.connection,args=(conn,addr))
			th.start()

			
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
		raw_data = data.decode("ISO-8859-1")
		http_req = HTTPRequest(raw_data)
		http_req.headers_request["data"] = data[data.index(b"\r\n\r\n")+4:]
		return http_req.headers_request

	def handle_request(self, data,headers_req,request):
		isError, status_code = self.checkForErrors(headers_req,request.decode("ISO-8859-1"))
		
		print(isError,status_code,"yes")
		
		headers_req = headers_req
		headers_req["data"] = data
		
		
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
			encoding_list = [k for k,v in sorted(q_val.items(), key=lambda item: item[1])]

			print("Encoding list --------------",encoding_list)
			headers_req["Accept-Encoding"] = encoding_list[0]
	
				####
				#checking if object is available in the given language
				####
								
		else:
			logger.error(status_codes[406][1],{'process':os.getpid(),'thread':threading.get_ident()})
			isError = False
			status_code = 406
			
		
		httpResponseObject = httpresponse(headers_req,isError,status_code)
		httpResponse,resource = httpResponseObject.build_response()

		sendResponse = httpResponse["protocol"] + " " + str(httpResponse["status_code"]) + " " + httpResponse["reason_phrase"] + "\r\n"
		print(httpResponse)
		for key,value in httpResponse["headers"].items():
			sendResponse += str(key)+": "+str(value)+"\r\n"
		
		sendResponse += "\r\n"
		print(type(resource))
		#sendResponse = bytes(sendResponse,'utf-8')
		print(sendResponse)
		print(getpid())
		return sendResponse,resource
		
		
	def checkForErrors(self,headers_req, data):
		if(self.isService == False):
			return True,503
		elif(len((headers_req["request_line"])[1]) > 2000):
			return True,414
		elif(len((data.split("/r/n/r/n"))[0]) > 10000000):
			return True,431
		elif(not self.isImplemented(headers_req)):
			return False,None
		elif(not self.checkExpect(headers_req)):
			return True,417
		elif(not self.isSystemOk):
			return True,500
		elif(not self.isMethodAllowed(headers_req["request_line"][0])):
			return True,405
		elif(self.isPayloadLarge(data,headers_req)):
			return True,413
		elif(self.isForbidden(headers_req)):
			return True,403
		elif(headers_req["request_line"][0] == "TRACE"):
			return False,200
		elif(headers_req["request_line"][0] == "OPTIONS"):
			return False,200
		
		'''
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
		"Accept-Language"
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
		"Transfer-Encoding",
		"Connection",
		"Referer",
		"Keep-Alive",
		"Postman-Token",
		"Allow"]
		
		headers_list = list(headers_req.keys())
		headers_list.remove("request_line")
		headers_list.remove("data")
		for header in headers_list:
			if(header not in valid_headers):
				print("header",header)
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
	
	
	def isPayloadLarge(self,data,headers_req):
		data_list = data.split("/r/n/r/n")
		
		if(headers_req["request_line"] == "HEAD"):
			return False
		elif(len(data_list) <= 1):
			return False
		elif(len(data_list[1]) > 100000):
			return True 

	def isMediaTypeSupported(self,Cont_type, cont_encod):
		return True

	def isForbidden(self,headers):
		return False
	
if __name__ == '__main__':
	server = HTTPServer()
	server.start()
    
    
