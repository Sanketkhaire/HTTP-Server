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
from uuid import uuid4
from hashlib import md5
from urllib.parse import parse_qs
from pandas import DataFrame
from logs import logger
import threading
import serverconfig

DOCUMENT_ROOT = serverconfig.DOCUMENT_ROOT
PORT_NUMBER = 12008
COOKIE_LOG = 'cookie.txt'

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

		if "Connection" not in self.headers:
					self.response["headers"]["Connection"] = "Close"
		elif self.headers["Connection"] == "Close":
				self.response["headers"]["Connection"] = "Close"
		else:
				self.response["headers"]["Connection"] = "Keep-Alive"

		
		if 'Cookie' not in self.headers:
			biscuit_id = uuid4().hex
			Max_Age = 5
			Path = '/'
			Domain = ''
			self.response['headers']['Set-Cookie'] = f'biscuit={biscuit_id}; Max-Age={Max_Age}; Path={Path}; Domain={Domain}'
			cookie_file = open(DOCUMENT_ROOT+'/cookie.txt','a')
			newcookie = f'[biscuit={biscuit_id} ,clientIP={self.headers["addr"][0]}, clientSocket={self.headers["addr"][1]}] : 1\n'
			cookie_file.write(newcookie)
			cookie_file.close()

		else:
			cookie_file = open(DOCUMENT_ROOT+'/cookie.txt','r')
			cookiedata = cookie_file.readlines()
			print(cookiedata)
			print(self.headers["Cookie"])
			for entryNo in range(len(cookiedata)):
				print("looooooooooooop")
				if self.headers['Cookie'] in cookiedata[entryNo]:
					print("innnnnnnnnn")
					cookie, count = cookiedata[entryNo].split(':')
					cookiedata[entryNo] = cookie + ': ' + str(int(count.strip()) + 1)+'\n'
					break
			cookie_file.close()
			cookie_file = open(DOCUMENT_ROOT+'/cookie.txt','w')
			cookie_file.writelines(cookiedata)
			cookie_file.close()
				


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

				if not os.access(filePath,os.R_OK):
					self.isError = False
					self.status_code = 405
					self.error_response()
					return self.response
				
				charset = None
				if "Accept-Charset" in self.headers:
					if self.headers["Accept-Charset"] in ['utf-8','ISO-8859-1']:
						charset = self.headers["Accept-Charset"]
					else:
						self.isError = True
						self.status_code = 406
						self.error_response()
						return self.response
				else:
					charset = 'ISO-8859-1'


				if "Accept" in self.headers:
					accept = self.headers["Accept"]
					accept_options = accept.split(",")
					q_val = {}
					
					for entry in accept_options:
						entry = entry.split(";")
						if(len(entry) == 1):
							q_val[entry[0]] = 1.0
						else:
							q_val[entry[0]] = float(entry[1].split('=')[1])
					
					print(q_val)
					type_list = [k for k,v in sorted(q_val.items(), key=lambda item: item[1],reverse=True)]
					print(type_list)
					file = fileName.split('.')[0]
					print("\n",file,"\n")
					isAvailable = False
					for i in type_list:
						if(i == '*/*'):
							print('i am in "*/*"')
							filep = open(filePath,'r')
							self.resource = bytes(filep.read(),charset)
							isAvailable = True
							break
						if os.path.exists(DOCUMENT_ROOT+'/'+file+'.'+i.split('/')[1]):
							filep = open(DOCUMENT_ROOT+'/'+file+'.'+i.split('/')[1],'r')
							self.resource = bytes(filep.read(),charset)
							isAvailable = True
							print("here")
							break
					
					if (not isAvailable):
						self.isError = False
						self.status_code = 406
						self.error_response()
						return self.response

						####
						#checking if filetype is available in the given type and subtype
						####
					
				else:
					filep = open(filePath,'r')
					self.resource = bytes(filep.read(),charset)

				#if "Accept-Charset" in self.headers :

			
				last_modified_time = os.path.getmtime(filePath)
				last_modified = time.strftime("%a, %d %b %Y %H:%M:%S GMT",time.gmtime(last_modified_time))
				
				content_length = len(self.resource)
				content_type = f'{mimetypes.guess_type(fileName)[0]}; charset={charset}'
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
				filePath = DOCUMENT_ROOT
			else:
				if '.' in uri:
					filePath = DOCUMENT_ROOT+uri.split('/')[-1]

			if(not os.path.exists(filePath)):
				self.status_code = 201
			else:
				self.status_code = 204

			post_data,isTrue = self.parse_type_POST()

			if(isTrue):
				if not os.access(DOCUMENT_ROOT+'/'+"logs.txt",os.W_OK):
					self.isError = True
					self.status_code = 403
					self.error_response()
					return self.response
				file = open(DOCUMENT_ROOT+'/logs.txt','a')
				file.write(str(post_data))
				file.close()

			print("post__date=a", post_data)

			self.response["status_code"] = self.status_code
			self.response["reason_phrase"] = status_codes[self.status_code][0]
				
		
		except Exception as e:
			traceback.print_exc()
			print(e)
			self.response = {}
			self.status_code = 404
			self.error_response()


	def PUT_response(self):
		try:

			filePath = DOCUMENT_ROOT + '/'+self.headers["request_line"][1]
			file = None
			if os.path.exists(filePath):
				if os.access(filePath,os.W_OK):
					file = open(filePath,'w')
					self.status_code = 204	
				else:
					self.isError = True
					self.status_code = 403
					self.error_response()
					return self.response
			
			else:
				self.status_code = 201

			print(len(self.headers["data"]))
			if 'text' in self.headers["Content-Type"]:
				file = open(filePath,'w')
				file.write(self.headers["data"].decode('ISO-8859-1'))
			else:
				file = open(filePath,'wb')
				file.write(self.headers["data"])

			self.response["status_code"] = self.status_code
			self.response["reason_phrase"] = status_codes[self.status_code][0]


		except Exception as e:
			logger.debug(e,{'process':os.getpid(),'thread':threading.get_ident()})
			self.response = {}
			self.status_code = 404
			self.error_response()
			

	def DELETE_response(self):
		try:
			filePath = DOCUMENT_ROOT + '/'+self.headers["request_line"][1]
			folder = DOCUMENT_ROOT
			if len(self.headers["request_line"][1].split('/')) > 2:
				for l in self.headers["request_line"][1].split('/')[1:-1]:
					folder += '/'+l

			if os.path.exists(filePath):
				if(os.access(folder,os.W_OK)):
					os.remove(filePath)
					self.status_code = 204
				else:
					self.isError = True
					self.status_code = 403
					self.error_response()
					return self.response

			else:
				self.isError = True
				self.status_code = 404
				self.error_response()
				return self.response

			self.response["status_code"] = self.status_code
			self.response["reason_phrase"] = status_codes[self.status_code][0]
			
		except Exception as e:
			traceback.print_exc()
			print(e)
			self.response = {}
			self.status_code = 404
			self.error_response()


	def parse_type_POST(self):
		if (self.headers["Content-Type"] == "application/x-www-form-urlencoded"):
			key_val = parse_qs(self.headers["data"].decode('ISO-8859-1'))
			file_data = DataFrame(key_val.items())
			self.status_code = 303
			self.response["headers"]["Location"] = f"http://127.0.0.1:{PORT_NUMBER}/welcome.txt"
			return file_data,"True"
					
		elif ("multipart/form-data" in self.headers["Content-Type"]):
			boundry = bytes('--'+self.headers["Content-Type"].split("=")[-1],'ISO-8859-1')
			raw_data = self.headers["data"]
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
						total_data[form_headers[0][form_headers[0].index(b' name=')+ 7:].decode('ISO-8859-1')] = received_data


				if len(form_headers) > 1 and b"Content-Type" in form_headers[1]:
					print("i m in")
					filetype = form_headers[1].split(b':')[1].strip(b" ")
					if b"form-data" in form_headers[0] and b"filename" in form_headers[0]:
						filename = form_headers[0][form_headers[0].index(b"filename")+10:-1]

					elif b"file" in form_headers[0]:
						filename = form_headers[0][form_headers[0].index(b"filename")+10:-1]
					
					filepath = DOCUMENT_ROOT+'/database/'+filename.decode()

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
		
			self.status_code = 303

			self.response["headers"]["Location"] = f"http://127.0.0.1:{PORT_NUMBER}/welcome.txt"
			
			return total_data,isTrue

		elif '.' in self.headers["request_line"][1]:
			path = '/'+self.headers["request_line"][1].split('/')[-1]
			file = open(DOCUMENT_ROOT+path,'a')
			file.write(self.headers["data"].decode())
			self.response["headers"]["Content-Location"] = f"/{path}"
			return None,False