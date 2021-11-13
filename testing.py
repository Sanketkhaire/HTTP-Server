import requests
from socket import *
import time
from rich import print, style


class Testing:
    def __init__(self):
        self.uri = 'http://localhost:12008/'

    def testBasicMethods(self):
        '''get, post, head, put, delete'''
        #get
        getReq = requests.get(self.uri,headers={'Connection':'Close'})
        print("[#fe8484]SIMPLE GET REQUEST")
        print("GET "+self.uri+" HTTP/1.1")
        self.displayAll(getReq)

        #head
        headReq = requests.head(self.uri,headers={'Connection':'Close'})
        print("[#fe8484]SIMPLE HEAD REQUEST")
        print("HEAD "+self.uri+" HTTP/1.1")
        self.displayAll(headReq)

        #post
        postData = {'name':'sanket','surname':'khaire'}
        postReq = requests.post(self.uri+'newentry',allow_redirects=False ,headers={'Connection':'Close','Content-Type':'text/plain'},data = postData)
        print("[#fe8484]SIMPLE POST REQUEST")
        print("POST "+self.uri+" HTTP/1.1")
        self.displayAll(postReq)

        #put
        file = open('welcome.txt','rb')
        putData = file.read()
        putReq = requests.put(self.uri+'wel.txt',headers={'Connection':'Close'},data=putData)
        print("[#fe8484]SIMPLE PUT REQUEST")
        print("PUT "+self.uri+" HTTP/1.1")
        self.displayAll(putReq)

        #delete
        delReq = requests.delete(self.uri+'wel.txt',headers={'Connection':'Close'},data={'key':'value'})
        print("[#fe8484]SIMPLE DELETE REQUEST")
        print("DELETE "+self.uri+" HTTP/1.1")
        self.displayAll(delReq)


    def hardGETtesting(self):
        '''Tuesday 02 November 2021 12∶06∶58 PM'''
        
        headers_dict = {'If-Unmodified-Since' : 'Wed, 03 Nov 2021 23:00:00 GMT'}

        getReq1 = requests.get(self.uri+'lp.jpg',headers=headers_dict)
        print("[#fe8484]GET REQUEST WITH 'If-Unmodified-Since' header :")
        print("GET "+self.uri+'lp.jpg'+" HTTP/1.1")
        self.displayAll(getReq1)
        time.sleep(1)

        headers_dict = {'If-Unmodified-Since' : 'Mon, 01 Nov 2021 10:00:00 GMT'}

        getReq2 = requests.get(self.uri+'lp.jpg',headers=headers_dict)
        print("[#fe8484]GET REQUEST WITH 'If-Unmodified-Since' header :")
        print("GET "+self.uri+'lp.jpg'+" HTTP/1.1")
        self.displayAll(getReq2)
        time.sleep(1)

        headers_dict = {'If-Modified-Since' : 'Wed, 03 Nov 2021 23:00:00 GMT'}

        getReq3 = requests.get(self.uri+'lp.jpg',headers=headers_dict)
        print("[#fe8484]GET REQUEST WITH 'If-Modified-Since' header :")
        print("GET "+self.uri+'lp.jpg'+" HTTP/1.1")
        self.displayAll(getReq3)

        headers_dict = {'If-Modified-Since' : 'Mon, 01 Nov 2021 23:00:00 GMT'}

        getReq4 = requests.get(self.uri+'lp.jpg',headers=headers_dict)
        print("[#fe8484]GET REQUEST WITH 'If-Modified-Since' header :")
        print("GET "+self.uri+'lp.jpg'+" HTTP/1.1")
        self.displayAll(getReq4)
        
        headers_dict = {'Accept-Encoding' : 'gzip', 
                        'Accept':'image/png',
                        'Accept-Charset': 'UTF-8'
                        }

        getReq5 = requests.get(self.uri+'lp.jpg',headers=headers_dict)
        print("[#fe8484]GET REQUEST WITH Accept, Accept-Encoding,Accept-Charset header :")
        print("GET "+self.uri+'lp.jpg'+" HTTP/1.1")
        self.displayAll(getReq5)

        headers_dict = {'Accept-Encoding' : 'gzip', 
                        'Accept':'image/png',
                        'Accept-Charset': 'UTF-16'
                        }

        getReq6 = requests.get(self.uri+'lp.jpg',headers=headers_dict)
        print("[#fe8484]GET REQUEST WITH Accept, Accept-Encoding,Accept-Charset header :")
        print("GET "+self.uri+'lp.jpg'+" HTTP/1.1")
        self.displayAll(getReq6)

        headers_dict = {'If-Match' : getReq3.headers['ETag']}
        getReq7 = requests.get(self.uri+'lp.jpg',headers=headers_dict)
        print("[#fe8484]GET REQUEST WITH 'If-Match' header :")
        print("GET "+self.uri+'lp.jpg'+" HTTP/1.1")
        self.displayAll(getReq7)

        headers_dict = {'If-Match' : getReq5.headers['ETag']+'9'}
        getReq8 = requests.get(self.uri+'lp.jpg',headers=headers_dict)
        print("[#fe8484]GET REQUEST WITH 'If-Match' header :")
        print("GET "+self.uri+'lp.jpg'+" HTTP/1.1")
        self.displayAll(getReq8)


    def checkQValue(self):
        headers_dict = {'Accept-Encoding' : 'gzip;q=0.8,deflate',
                        'Accept':'*/*;q=0.8,text/plain;q=0.9','Connection':'Close'}
        getReq = requests.get(self.uri+'random.txt',headers=headers_dict)
        print("[#fe8484]GET REQUEST WITH METHODS INCLUDING q-values :")
        print("GET "+self.uri+'random.txt'+" HTTP/1.1")
        self.displayAll(getReq)
        


    def hardPOSTChecking(self):
        
        print("[#fe8484]POST REQUEST with sending file and after that redirecting to the uri mentioned in 'LOCATION' HEADER:")
        file = open('filee.pdf','rb')
        postData = file.read()
        print("[#fe8484]readirection not allowed")
        print("POST "+self.uri+" HTTP/1.1")
        postReq = requests.post(self.uri,allow_redirects=False,files = {"file.pdf":postData})
        self.displayAll(postReq)

        print("[#fe8484]readirection for same allowed")
        print("POST "+self.uri+" HTTP/1.1")
        postReq = requests.post(self.uri,files = {"file.pdf":postData})
        self.displayAll(postReq)

    
    def permissionsChecking(self):
        
        #requesting a resource on which read permission is forbidden
        print("[#fe8484]GET request for a resource where read permission is not allowed")
        getReq = requests.get(self.uri+'secret.txt')
        print("GET "+self.uri+'secret.txt'+" HTTP/1.1")
        self.displayAll(getReq)

        #requesting to modify a resource on which write permission is forbidden
        print("[#fe8484]PUT request for a resource where write permission is not allowed")
        putData = {'name':'s','surname':'khaire'}
        putReq = requests.put(self.uri + 'secret.txt',data = putData)
        print("PUT "+self.uri+'secret.txt'+" HTTP/1.1")
        self.displayAll(putReq)

    def wrongMethodTest(self):

        print("[#fe8484]Requesting with wrong method :")

        request = ("TRACE /img.jpeg HTTP/1.1\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Connection: Close\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Content-Encoding: gzip\r\n"+
        "Content-Type: image/jpeg\r\n\r\n")

        serverName = '127.0.0.1'
        serverPort = 12008
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverName,serverPort))

        clientSocket.send(request.encode())
        modifiedSentence = clientSocket.recv(1024)
        clientSocket.close()
        print("Request :")
        print(request)
        print("Response :")
        print(modifiedSentence.decode())
        print('\n\n')


    def wrongHTTPVersion(self):

        print("[#fe8484]Requesting with wrong HTTP version :")
        request = ("GET /viratk.jpeg HTTP/2.0\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Accept-Charset: UTF-8\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Accept-Encoding: gzip\r\n"+
        "Accept: image/jpeg\r\n\r\n")

        serverName = '127.0.0.1'
        serverPort = 12008
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverName,serverPort))

        clientSocket.send(request.encode())
        modifiedSentence = clientSocket.recv(1024)
        clientSocket.close()
        print("Request :")
        print(request)
        print("Response :")
        print(modifiedSentence.decode())
        print('\n\n')


    def largeRequestLine(self):

        print("[#fe8484]Length of request line out of bound :")
        request = ("GET /viratkMYDEARSONMARCUSYOUHAVENOWBEENSTUDYINGINTRODUCTIONTHEIMPORTANCEOFCOMBININGGREEKANDLATINSTUDIESAFULLYEARUNDERCRATIPPUSANDTHATTOOINATHENSANDYOUSHOULDBEFULLYEQUIPPEDWITHTHEPRACTICALPRECEPTSANDTHEPRINCIPLESOFPHILOSOPHYSOMUCHATLEASTONEMIGHTEXPECTEROMTHEPREEMINENCENOTONLYOFYOURTEACHERBUTALSOOFTHECITYTHEFORMERISABLETOENRICHYOUWITHLEARNINGTHELATTERTOSUPPLYYOUWITHMODELSNEVERTHELESSJUSTASIFORMYOWNIMPROVEMENTHAVEALWAYSCOMBINEDGREEKANDLATINSTUDIESANDIHAVEDONETHISNOTONLYINTHESTUDYOFPHILOSOPHYBUTALSOINTHEPRACTICEOFORATORYSOIRECOMMENDTHATYOUSHOULDDOTHESAMESOTHATYOUMAYHAVEEQUALCOMMANDOFBOTHLANGUAGESMYDEARSONMARCUSYOUHAVENOWBEENSTUDYINGINTRODUCTIONTHEIMPORTANCEOFCOMBININGGREEKANDLATINSTUDIESAFULLYEARUNDERCRATIPPUSANDTHATTOOINATHENSANDYOUSHOULDBEFULLYEQUIPPEDWITHTHEPRACTICALPRECEPTSANDTHEPRINCIPLESOFPHILOSOPHYSOMUCHATLEASTONEMIGHTEXPECTEROMTHEPREEMINENCENOTONLYOFYOURTEACHERBUTALSOOFTHECITYTHEFORMERISABLETOENRICHYOUWITHLEARNINGTHELATTERTOSUPPLYYOUWITHMODELSNEVERTHELESSJUSTASIFORMYOWNIMPROVEMENTHAVEALWAYSCOMBINEDGREEKANDLATINSTUDIESANDIHAVEDONETHISNOTONLYINTHESTUDYOFPHILOSOPHYBUTALSOINTHEPRACTICEOFORATORYSOIRECOMMENDTHATYOUSHOULDDOTHESAMESOTHATYOUMAYHAVEEQUALCOMMANDOFBOTHLANGUAGESMYDEARSONMARCUSYOUHAVENOWBEENSTUDYINGINTRODUCTIONTHEIMPORTANCEOFCOMBININGGREEKANDLATINSTUDIESAFULLYEARUNDERCRATIPPUSANDTHATTOOINATHENSANDYOUSHOULDBEFULLYEQUIPPEDWITHTHEPRACTICALPRECEPTSANDTHEPRINCIPLESOFPHILOSOPHYSOMUCHATLEASTONEMIGHTEXPECTEROMTHEPREEMINENCENOTONLYOFYOURTEACHERBUTALSOOFTHECITYTHEFORMERISABLETOENRICHYOUWITHLEARNINGTHELATTERTOSUPPLYYOUWITHMODELSNEVERTHELESSJUSTASIFORMYOWNIMPROVEMENTHAVEALWAYSCOMBINEDGREEKANDLATINSTUDIESANDIHAVEDONETHISNOTONLYINTHESTUDYOFPHILOSOPHYBUTALSOINTHEPRACTICEOFORATORYSOIRECOMMENDTHATYOUSHOULDDOTHESAMESOTHATYOUMAYHAVEEQUALCOMMANDOFBOTHLANGUAGESMYDEARSONMARCUSYOUHAVENOWBEENSTUDYINGINTRODUCTIONTHEIMPORTANCEOFCOMBININGGREEKANDLATINSTUDIESAFULLYEARUNDERCRATIPPUSANDTHATTOOINATHENSANDYOUSHOULDBEFULLYEQUIPPEDWITHTHEPRACTICALPRECEPTSANDTHEPRINCIPLESOFPHILOSOPHYSOMUCHATLEASTONEMIGHTEXPECTEROMTHEPREEMINENCENOTONLYOFYOURTEACHERBUTALSOOFTHECITYTHEFORMERISABLETOENRICHYOUWITHLEARNINGTHELATTERTOSUPPLYYOUWITHMODELSNEVERTHELESSJUSTASIFORMYOWNIMPROVEMENTHAVEALWAYSCOMBINEDGREEKANDLATINSTUDIESANDIHAVEDONETHISNOTONLYINTHESTUDYOFPHILOSOPHYBUTALSOINTHEPRACTICEOFORATORYSOIRECOMMENDTHATYOUSHOULDDOTHESAMESOTHATYOUMAYHAVEEQUALCOMMANDOFBOTHLANGUAGES.jpeg HTTP/1.1\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Connection: keep-alive\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Accept-Encoding: gzip\r\n"+
        "Accept-Type: image/jpeg\r\n\r\n")

        serverName = '127.0.0.1'
        serverPort = 12008
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverName,serverPort))

        clientSocket.send(request.encode())
        modifiedSentence = clientSocket.recv(1024)
        clientSocket.close()
        print("Request :")
        print(request)
        print("Response :")
        print(modifiedSentence.decode())
        print('\n\n')



    def payloadOutOfLimit(self):
        
        print("[#fe8484]Length of payload(entity) out of bound :")
        file = open('bfile.mp3','rb')
        dataToSend = file.read()

        request = ("PUT /song.mp3 HTTP/1.1\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Content-Type: audio/mpeg\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Connection: keep-alive\r\n"+
        "Keep-Alive: 20\r\n"+
        f"Content-Length: {len(dataToSend)}\r\n\r\n" ) 

        serverName = '127.0.0.1'
        serverPort = 12008
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverName,serverPort))

        clientSocket.send(request.encode()+dataToSend)
        modifiedSentence = clientSocket.recv(1024)
        clientSocket.close()
        print("Request :")
        print(request)
        print("Response :")
        print(modifiedSentence.decode())
        print('\n\n')



    def mediaTypeTest(self):

        print("[#fe8484]Request with Media-Type which is not serviced at server:")
        file = open('rich.rtf','rb')

        dataToSend = file.read()

        request = ("PUT /richie.rtf HTTP/1.1\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Connection: keep-alive\r\n"+
        "Keep-Alive: 20\r\n"+
        f"Content-Length: {len(dataToSend)}\r\n\r\n" ) 

        serverName = '127.0.0.1'
        serverPort = 12008
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverName,serverPort))

        clientSocket.send(request.encode()+dataToSend)
        modifiedSentence = clientSocket.recv(1024)
        clientSocket.close()
        print("Request :")
        print(request)
        print("Response :")
        print(modifiedSentence.decode())
        print('\n\n')


    def requestTimeout(self):

        print("[#fe8484]Requesting put data with wrong content length causing timeout:")
        file = open('aud.mp3','rb')
        dataToSend = file.read()

        request = ("PUT /aud.mp3 HTTP/1.1\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Content-Length: 900000\r\n"+
        "Connection: keep-alive\r\n"+
        "Keep-Alive: 20\r\n"+
        "Content-Type: audio/mpeg\r\n\r\n")

        serverName = '127.0.0.1'
        serverPort = 12008
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverName,serverPort))

        clientSocket.send(request.encode()+dataToSend)
        modifiedSentence = clientSocket.recv(1024)
        clientSocket.close()
        print("Request :")
        print(request)
        print("Response :")
        print(modifiedSentence.decode())
        print('\n\n')



    def testWithoutContentLength(self):

        print("[#fe8484]Requesting to put data without content-Length:")
        file = open('aud.mp3','rb')
        dataToSend = file.read()

        request = ("PUT /aud.mp3 HTTP/1.1\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Connection: keep-alive\r\n"+
        "Keep-Alive: 20\r\n"+
        "Content-Type: audio/mpeg\r\n\r\n")

        serverName = '127.0.0.1'
        serverPort = 12008
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverName,serverPort))

        clientSocket.send(request.encode()+dataToSend)
        modifiedSentence = clientSocket.recv(1024)
        clientSocket.close()
        print("Request :")
        print(request)
        print("Response :")
        print(modifiedSentence.decode())
        print('\n\n')


    def wrongHeaders(self):

        file = open('random.txt','rb')
        dataToSend = file.read()

        print("[#fe8484]Requesting with wrong HTTP header :")
        request = ("GET /random.txt HTTP/1.1\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Place: Pune\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Accept-Encoding: gzip\r\n"+
        "Accept: text/plain\r\n\r\n")

        serverName = '127.0.0.1'
        serverPort = 12008
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverName,serverPort))

        clientSocket.send(request.encode()+dataToSend)
        modifiedSentence = clientSocket.recv(1024)
        clientSocket.close()
        print("Request :")
        print(request)
        print("Response :")
        print(modifiedSentence.decode())
        print('\n\n')


    def putWithPrecondition(self):
        print("[#fe8484]PUT request with 'If-Unmodified_Since' header:")
        file = open('lp.jpg','rb')
        dataToSend = file.read()

        request = ("PUT /img1.jpeg HTTP/1.1\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Content-Type: image/jpeg\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Connection: keep-alive\r\n"+
        "If-Unmodified-Since: Thu, 04 November 2021 12∶00∶00 GMT\r\n"
        "Keep-Alive: 20\r\n"+
        f"Content-Length: {len(dataToSend)}\r\n\r\n") 

        serverName = '127.0.0.1'
        serverPort = 12008
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverName,serverPort))

        clientSocket.send(request.encode()+dataToSend)
        modifiedSentence = clientSocket.recv(1024)
        print("Request :")
        print(request)
        print("Response :")
        print(modifiedSentence.decode())
        print('\n\n')

        print("[#fe8484]PUT request with 'If-Match' header:")
        request = ("PUT /img2.jpeg HTTP/1.1\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Content-Type: image/jpeg\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Connection: keep-alive\r\n"+
        'If-Match: "111111111111"\r\n'
        "Keep-Alive: 20\r\n"+
        f"Content-Length: {len(dataToSend)}\r\n\r\n")

        clientSocket.send(request.encode()+dataToSend)
        modifiedSentence = clientSocket.recv(1024)
        clientSocket.close()
        print("Request :")
        print(request)
        print("Response :")
        print(modifiedSentence.decode())
        print('\n\n')

    def displayAll(self,res):
        req = dict(res.request.headers)
        for header in req:
            print(header+': '+req[header])
        
        print("\n",res.status_code,res.reason)
        for header in dict(res.headers):
            print(header+': '+res.headers[header])
        
        print('\n\n')


        
if __name__ == '__main__':
    print("\n\n[#2BC1AC]------------------   TESTING BEGINS HERE  --------------------\n\n")
    time.sleep(1)
    testingTool = Testing()
    testingTool.testBasicMethods()
    testingTool.hardGETtesting()
    testingTool.hardPOSTChecking()
    testingTool.checkQValue()
    testingTool.wrongHTTPVersion()
    testingTool.largeRequestLine()
    testingTool.mediaTypeTest()
    testingTool.requestTimeout()
    testingTool.testWithoutContentLength()
    testingTool.payloadOutOfLimit()
    testingTool.wrongHeaders()
    testingTool.putWithPrecondition()
