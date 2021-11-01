
import socket
import os
from err import *
import time
from datetime import datetime
from email.utils import formatdate
import mimetypes
import gzip
import zlib
import brotli
from Error_codes import status_codes
from pathlib import Path
import traceback
import uuid
from hashlib import md5

DOCUMENT_ROOT = str(Path().resolve())


class TCPServer:

	def __init__(self, host, port):
		self.host = host
		self.port = port
      

	def start(self):

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((self.host, self.port))
		s.listen(10)
		
		print("Listening at", s.getsockname())
        
		while True:
			conn, addr = s.accept()
			print("Connected by", addr)
			data = conn.recv(10485760) 
			data1 = conn.recv(10485760) 
			#print(data,data1)
			data = data+data1

			response,resource = self.handle_request(data)
			conn.send(response.encode('ISO-8859-1'))
			if resource:
				conn.send(resource)
			conn.close()
	
	def handle_request(self, data):
		return data

        
class HTTPServer(TCPServer):
	def __init__(self, host='127.0.0.1', port=12004,allowedMethods=['GET','HEAD','POST','PUT','DELETE']):
		self.allowedMethods = allowedMethods
		self.isService = True
		self.isSystemOk = True
		
		TCPServer.__init__(self,host,port)

	def handle_request(self, data):
		raw_data = data.decode("ISO-8859-1")
		http_req = HTTPRequest(raw_data)
		
		isError, status_code = self.checkForErrors(http_req.headers_request,raw_data)
		
		print(isError,status_code,"yes")
		
		headers_req = http_req.headers_request
		headers_req["request"] = data
		
		'''if "Accept" in headers_req:
			accept = http_req["Accept"]
			accept_options = accept.split(",")
			q_val = {}
			
			for entry in accept_options:
				entry = entry.split(";")
				if(len(entry) == 1):
					q_val[entry[0]] = 1
				else:
					q_val[entry[0]] = entry[1]
				type_list = [k for k,v in sorted(q_val.items(), key=lambda item: item[1])]
				
				for i in range(len(type_list)):
					type_list[i] = type_list[i].split("/")
				
				####
				#checking if filetype is available in the given type and subtype
				####
				
		else:
			isCorrect = False
			status_code = 406
		
		if "Accept-Language" in headers_req:
			accept = http_req["Accept"]
			accept_options = accept.split(",")
			q_val = {}
			
			for entry in accept_options:
				entry = entry.split(";")
				if(len(entry) == 1):
					q_val[entry[0]] = 1
				else:
					q_val[entry[0]] = entry[1]
				lang_list = [k for k,v in sorted(q_val.items(), key=lambda item: item[1])]
				
				for i in range(len(lang_list)):
					lang_list[i] = lang_list[i].split("-")
				
				####
				#checking if object is available in the given language
				####
					
					
		else:
			isCorrect = False
			status_code = 406
		'''
		
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
		return sendResponse,resource
		
		
	def checkForErrors(self,headers_req, data):
		if(self.isService == False):
			return True,503
		elif(len((headers_req["request_line"])[1]) > 2000):
			return True,414
		elif(len((data.split("/r/n/r/n"))[0]) > 10000):
			return True,431
		elif(not self.isImplemented(headers_req)):
			return True,501
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
		
	
class HTTPRequest:
	def __init__(self, data):
		self.method = None
		self.uri = None
		self.http_version = "HTTP/1.1"
		self.headers_request = self.parse(data)
	
	
	#parsing the http request
	def parse(self,data):
		
		#print('sanket='+data)
		headers = data.split("\r\n")
		
		request_line = headers[0]
		request_line_list = request_line.split(" ")
		self.method = request_line_list[0]
		self.uri = request_line_list[1]
		self.http_version = request_line_list[2]
		
		headers = headers[1:]
		print("parse")
		headers_list = {}
		
		for header in headers:
			if(header == ""):
				break
			temp = header.split(":")
			headers_list[temp[0]] = temp[1].strip()
		
		headers_list["request_line"] = request_line_list
		headers_list["data"] = data[data.index("\r\n\r\n")+4:]
		#print(headers_list)
			
		return headers_list
		


class httpresponse:
	def __init__(self,headers,isError,status_code):
		self.headers = headers
		self.isError = isError
		self.status_code = status_code
		self.response = {"headers" :{}}
		self.resource = None
		
	'''Content-type,content-length,content-location content-md5, Date, keep-Alive, Allow, Connection, Transfer-Encoding, Set-Cookie, Server, location, last-modified, expires, Etag,  '''
	
	def build_response(self):
		method = self.headers["request_line"][0]
		
		self.response["protocol"] = "HTTP/1.1"
		self.response["headers"]["Date"] = formatdate(timeval=None, localtime=False, usegmt=True)
		self.response["headers"]["Server"] = "MY_HTTP_SERVER"
		
		self.response["status_code"] = None
		
		
		if(not self.isError and self.status_code ==  100):
			self.response = {}
			self.response["protocol"] = "HTTP/1.1"
			self.response["status_code"] = 100
			self.response["reason_phrase"] = status_codes[100][0]
			self.response["headers"] = {}
			print("10000000000000")
			#return self.response,self.resource
		elif(self.isError):
			self.response = {}
			self.error_response()
		elif(method == "GET"):
			self.GET_response()
		elif(method == "HEAD"):
			self.HEAD_response()
		elif(method == "POST"):
			self.POST_response()
		elif(method == "PUT"):
			self.PUT_response()
		elif(method == "DELETE"):
			self.DELETE_response()
			
		return self.response,self.resource
		
			
	def GET_response(self):
	
		'''
	Get headers :  If-Modified-Since
	If-Range
	If-Unmodified-Since'''

		try:	
			uri = self.headers["request_line"][1]
			
			filePath = "/"
			

			if(uri == "/"):
				filePath = "/index.html"
			else:
				filePath = uri.split("?")[0]
				
			fileName = filePath.split("/")[-1]
			filePath = DOCUMENT_ROOT + "/" + fileName
			
			if(not os.path.exists(filePath)):
				self.isError = True
				self.status_code = 404
				self.response = {}
				self.error_response()
				return self.response
				
			else:
				
				filep = open(filePath,'rb')
				
				self.resource = filep.read()
				filep.close()
				
				last_modified_time = os.path.getmtime(filePath)
				last_modified = time.strftime("%a, %d %b %Y %H:%M:%S GMT",time.gmtime(last_modified_time))
				
				content_length = len(self.resource)
				content_type = mimetypes.guess_type(fileName)[0]
				Etag = '"'+str(int(last_modified_time)) + str(len(self.resource))+'"'
				preconditionFlag = True
				
				if "If-Match" in self.headers:
					etags_list = self.headers["If-Match"].split(",")
					
					if ("*" in etags_list or Etag in etags_list):
						preconditionFlag = True
					else:
						preconditionFlag = False
						self.isError = True
						self.status_code = 412
						self.response = {}
						self.error_response()
						return self.response
				
				if "If-Modified-Since" in self.headers and preconditionFlag:
					
					check_date = self.headers["Date"]
					check_date = time.strptime(check_date, "%a, %d %b %Y %H:%M:%S GMT")
					
					if time.mktime(check_date) > last_modified_time:
						preconditionFlag = False
						self.isError = False
						self.response["status_code"] = self.status_code = 304
						self.response["reason_phrase"] = status_codes[304][0]
						self.response["headers"]["Etag"] = Etag
						self.resource = None
						return self.response
				
				if "If-Unmodified-since" in self.headers and "If-Match" not in self.headers and preconditionFlag:
					
					check_date = self.headers["Date"]
					check_date = time.strptime(check_date, "%a, %d %b %Y %H:%M:%S GMT")
					
					if time.mktime(check_date) < last_modified_time:
						preconditionFlag = False
						self.isError = True
						self.status_code = 412
						self.error_response()
						return self.response
					
				if "Accept-Encoding" in self.headers and not "*" in self.headers["Accept-Encoding"]:
					
					if self.headers["Accept-Encoding"] == "gzip":
						self.resource = gzip.compress(self.resource)
						
						self.response["headers"]["Content-Encoding"] = "gzip"
						self.response["headers"]["Content-Length"] = len(self.resource)
						
					elif self.headers["Accept-Encoding"] == "deflate":
						self.resource = zlib.compress(self.resource)
						
						self.response["headers"]["Content-Encoding"] = "deflate"
						self.response["headers"]["Content-Length"] = len(self.resource)
					
					elif self.headers["Accept-Encoding"] == "br":
						self.resource = brotli.compress(self.resource)
						
						self.response["headers"]["Content-Encoding"] = "br"
						self.response["headers"]["Content-Length"] = len(self.resource) 
						
				
				self.response["headers"]["Accept-Ranges"] = "bytes"
				
				if "Ranges" in self.headers:
					
					condition = True
					if "If-Range" in self.headers:
						if self.headers["If-Range"][0] == '"' and self.headers["If-Range"][0] == '"':
							if self.headers["If-Range"] != Etag:
								condition = False
						else:
							range_date = self.headers["If-Range"]
							range_date = time.strptime(check_date, "%a, %d %b %Y %H:%M:%S GMT")
							if time.mktime(range_date) > last_modified_time:
								condition = False
					
					if condition:
						range_list = self.headers["Ranges"].split(",")
						for i in range(len(range_list)):
							range_list[i] = range_list[i].split("-")
						
						new_res = b''
						cont_len = 0
						
						for range_ in range_list:
							new_res += self.resource[int(range_[1]):int(range_[0])]
							cont_len +=  int(range_[1]) - int(range_[0])
						
						self.response["headers"]["Content-Length"] = cont_len
						self.resource = new_res


				self.response["headers"]["Last-Modified"] = last_modified
				self.response["headers"]["ETag"] = Etag
				self.response["status_code"] = 200
				self.response["reason_phrase"] = status_codes[100][0]
				if "Content-Length" not in self.response["headers"]:
					self.response["headers"]["Content-Length"] = content_length
				if "Content-Type" not in self.response["headers"]:
					self.response["headers"]["Content-Type"] = content_type
					if "text" in content_type:
						self.response["headers"]["Content-Type"] += "; charset=UTF-8"
					
				if "Connection" not in self.headers:
					self.response["headers"]["Connection"] = "Close"
				elif self.headers["Connection"] == "Close":
					self.response["headers"]["Connection"] = "Close"
				else:
					self.response["headers"]["Connection"] = "Keep-Alive"
				
				self.response["headers"]["Content-md5"] = md5(self.resource).hexdigest() 

				expires_date = last_modified_time + 432000
				curr = datetime.timestamp(datetime.now())
				if expires_date < curr:
					expires_date = "0"
				else:
					expires_date = time.strftime("%a, %d %b %Y %H:%M:%S GMT",time.gmtime(expires_date))

				self.response["headers"]["Expires"] = expires_date

				return self.response,self.resource
				

		except Exception as e:
			traceback.print_exc()
			print(e)
			self.response = {}
			self.status_code = 404
			self.error_response()


		
	def error_response(self):
		'''status-line, Date, Server, Content-Length, Connection, Content-Type, transfer-encoding'''
		
		#self.response["headers"]["
		print("nooo")
		self.response["protocol"] = "HTTP/1.1"
		self.response["status_code"] = self.status_code
		self.response["reason_phrase"] = status_codes[self.status_code][0]
		print(self.response["reason_phrase"])
		self.response["headers"] = {}
		self.response["headers"]["Date"] = formatdate(timeval=None, localtime=False, usegmt=True)
		self.response["headers"]["Server"] = "MY_HTTP_SERVER"
		self.response["headers"]["Connection"] = "Close"
		self.response["headers"]["Content-Type"] = "text/html; charset=UTF_8"
		self.resource = generate_error_page(self.status_code, status_codes[self.status_code][0]).encode('utf-8')
		content_len = len(self.resource)
		self.response["headers"]["Content-Length"] = content_len
		if self.headers["request_line"][0] == "HEAD":
			self.resource = None
		return self.response
		 
		 
	def HEAD_response(self):
		self.GET_response()
		self.resource = None

	def POST_response(self):

		try:

			print("in post")
			uri = self.headers["request_line"][1]
			
			filePath = "/"
			

			if(uri == "/"):
				filePath = "/index.html"
			else:
				filePath = uri.split("?")[0]
				
			fileName = filePath.split("/")[-1]
			filePath = DOCUMENT_ROOT + "/" + fileName

			if(not os.path.exists(filePath)):
				self.status_code = 201
			else:
				self.status_code = 204

			post_data,isTrue = self.parse_type_POST()
			if(isTrue):
				file = open(filePath,'a')
				file.write(str(post_data))
				file.close()

			print("post__date=a", post_data)

			self.response["status_code"] = self.status_code
			self.response["reason_phrase"] = status_codes[self.status_code][0]

			if "Connection" not in self.headers:
					self.response["headers"]["Connection"] = "Close"
			elif self.headers["Connection"] == "Close":
					self.response["headers"]["Connection"] = "Close"
			else:
					self.response["headers"]["Connection"] = "Keep-Alive"
				
		
		except Exception as e:
			traceback.print_exc()
			print(e)
			self.response = {}
			self.status_code = 404
			self.error_response()

	def PUT_response(self):
		pass

	def DELETE_response(self):
		pass


	def parse_type_POST(self):
		if (self.headers["Content-Type"] == "application/x-www-form-urlencoded"):
			key_val = self.headers["data"].split('&')
			file_data = {}
			print("key-val ===" ,key_val)
			for entry in key_val:
				entry = entry.split('=')
				file_data[entry[0]] = entry[1]
			return file_data,"True"
					
		elif ("multipart/form-data" in self.headers["Content-Type"]):
			boundry = bytes('--'+self.headers["Content-Type"].split("=")[-1],'ISO-8859-1')
			raw_data = self.headers["request"][self.headers["request"].index(b"\r\n\r\n")+4:]
			multi_forms = raw_data.split(boundry)[1:-1]
			#print(boundry)
			#print("\nlst = ",multi_forms,"\n")
			
			total_data = {}
			isTrue = False
			for entry in multi_forms:
				lst = entry.split(b"\r\n\r\n")
				form_headers = lst[0].split(b"\r\n")[1:]
				if b"Content-Disposition" in form_headers[0]:	
					if b"form-data" in form_headers[0] and b"filename" not in form_headers[0]:
						isTrue = True
						received_data = lst[1].decode('ISO-8859-1')
						total_data[form_headers[0][form_headers[0].index(b' name=')+ 7].decode('ISO-8859-1')] = received_data

				if len(form_headers) > 1 and b"Content-Type" in form_headers[1]:
					print("i m in")
					filetype = form_headers[1].split(b':')[1].strip(b" ")
					if b"form-data" in form_headers[0] and b"filename" in form_headers[0]:
						filename = form_headers[0][form_headers[0].index(b"filename")+10:-1]

					elif b"file" in form_headers[0]:
						filename = form_headers[0][form_headers[0].index(b"filename")+10:-1]
					
					filepath = DOCUMENT_ROOT+'/'+filename.decode()
					self.status_code = 200

					if b"text" in filetype:
						print("txt")
						received_data = lst[1].decode('ISO-8859-1')
						file = open(filepath,'a')
						file.write(str(received_data))
						file.close()
					
					elif b"application" in filetype or b"image" in filetype or b"audio" in filetype or b"video" in filetype:
						print("encoded")
						received_data = lst[1]
						file = open(filepath,'ab')
						file.write(received_data)
						file.close()
			
			return total_data,isTrue

		
if __name__ == '__main__':
    server = HTTPServer()
    server.start()
    
    
    
    
    
    
    
