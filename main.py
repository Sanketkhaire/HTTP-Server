
import socket

class TCPServer:
    """Base server class for handling TCP connections. 
    The HTTP server will inherit from this class.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
      

    def start(self):
        """Method for starting the server"""

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at", s.getsockname())
	
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            # For the sake of this tutorial, 
            # we're reading just the first 1024 bytes sent by the client.
            data = conn.recv(1024) 

            response = self.handle_request(data)

            conn.sendall(response)
            conn.close()

    def handle_request(self, data):
        """Handles incoming data and returns a response.
        Override this in subclass.
        """
        return data
        
class HTTPServer(TCPServer):
	def __init__(self, host='127.0.0.1', port=8000,allowedMethods=['GET','HOST']):
		self.allowedMethods = allowedMethods
		self.isService = True
		self.isSystemOk = True
		
		TCPServer.__init__(self,host,port)

	def handle_request(self, data):
		raw_data = data.decode()
		http_req = HTTPRequest(raw_data)
		
		isCorrect, status_code = self.checkForErrors(http_req.headers_request,raw_data)
		
		print(isCorrect,status_code,"yes")
		
		headers_req = http_req.headers_request
		
		if "Accept" in headers_req:
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
				
				for i in range(len(type_list)):
					type_list[i] = type_list[i].split("-")
				
				####
				#checking if object is available in the given language
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
				
				for i in range(len(type_list)):
					type_list[i] = type_list[i].split("-")
				
				####
				#checking if object is available in the given language
				####
					
					
		else:
			isCorrect = False
			status_code = 406
			
		
		if "Accept-Encoding" in headers_req:
			accept = http_req["Accept"]
			accept_options = accept.split(",")
			q_val = {}
			
			for entry in accept_options:
				entry = entry.split(";")
				if(len(entry) == 1):
					q_val[entry[0]] = 1
				else:
					q_val[entry[0]] = entry[1]
				encoding_list = [k for k,v in sorted(q_val.items(), key=lambda item: item[1])]
				
				for i in range(len(type_list)):
					type_list[i] = type_list[i].split("-")
				
				####
				#checking if object is available in the given language
				####
					
					
		else:
			isCorrect = False
			status_code = 406
			
				
		
		
		
		return data
		
		
	def checkForErrors(self,headers_req, data):
		if(self.isService == False):
			return False,503
		elif(len((headers_req["request_line"])[1]) > 2000):
			return False,414
		elif(len((data.split("/r/n/r/n"))[0]) > 10000):
			return False,431
		elif(not self.isImplemented(headers_req)):
			return False,501
		elif(not self.checkExpect(headers_req)):
			return False,417
		elif(not isSystemOk):
			return False,500
		elif(not self.isMethodAllowed(headers_req["request_line"][0])):
			return False,405
		elif(headers_req["Expect"] == " 100-continue"):
			return True,100
		elif(self.isPayloadLarge(data,headers_req)):
			return False,413
		elif(not self.isMediaTypeSupported(headers_req["Content-Type"], headers_req["Content_Encoding"])):
			return False,415
		elif(self.isBadrequest(headers_req)):
			return False,400
		elif(self.isForbidden(headers_req)):
			return False,403
		elif(headers_req["request_line"][0] == "TRACE"):
			return True,200
		elif(headers_req["request_line"][0] == "OPTIONS"):
			return True,200
		
		
		return True,0
		
		
	def isImplemented(self,headers_req):
	
		valid_headers = ["Accept",
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
		"Allow"]
		
		headers_list = list(headers_req.keys())
		for header in headers_list[1:]:
			if(header not in valid_headers):
				print(header)
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
		
	
class HTTPRequest:
	def __init__(self, data):
		self.method = None
		self.uri = None
		self.http_version = "HTTP/1.1"
		self.headers_request = self.parse(data)
	
	
	#parsing the http request
	def parse(self,raw_data):
	
		headers = raw_data.split("\r\n")
		
		request_line = headers[0]
		request_line_list = request_line.split(" ")
		self.method = request_line_list[0]
		self.uri = request_line_list[1]
		self.http_version = request_line_list[2]
		
		headers = headers[1:]
		print("parse")
		print(*headers, sep="\n")
		headers_list = {}
		
		for header in headers:
			if(header == ""):
				break
			temp = header.split(":")
			headers_list[temp[0]] = temp[1]
		
		headers_list["request_line"] = request_line_list
			
		return headers_list
		
		
		

if __name__ == '__main__':
    server = HTTPServer()
    server.start()
    
    
    
    
    
    
    
    
    
    
    
