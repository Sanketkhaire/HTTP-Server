

class HTTPRequest:
	def __init__(self, data):
		self.method = None
		self.uri = None
		self.http_version = "HTTP/1.1"
		self.headers_request = self.parse(data)
	
	
	#parsing the http request
	def parse(self,data):
		
		headers = data.split("\r\n")
		request_line = headers[0]
		request_line_list = request_line.split(" ")
		self.method = request_line_list[0]
		self.uri = request_line_list[1]
		self.http_version = request_line_list[2]
		
		headers = headers[1:]
		headers_list = {}
		
		for header in headers:
			if(header == ""):
				break
			temp = header.split(": ")
			headers_list[temp[0]] = temp[1].strip()
		
		headers_list["request_line"] = request_line_list
			
		return headers_list