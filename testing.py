import requests
from socket import *
import time


class Testing:
    def __init__(self):
        self.uri = 'http://localhost:12008/'

    def testBasicMethods(self):
        '''get, post, head, put, delete'''
        #get
        getReq = requests.get(self.uri)
        print(getReq.content)

        #head
        headReq = requests.head(self.uri)
        print(headReq.headers)

        #post
        postData = {'name':'sanket','surname':'khaire'}
        postReq = requests.post(self.uri,data = postData)
        print(postReq.headers,postReq.content)

        #put
        file = open('welcome.txt','rb')
        putData = file.read()
        putReq = requests.put(self.uri+'wel.txt',data=putData)
        print(putReq.headers)

        #delete
        delReq = requests.delete(self.uri+'wel.txt',data={'key':'value'})
        print(delReq.headers)


    def hardGETtesting(self):
        headers_dict = {'If-Unmodified-Since' : 'Tue, 09 Nov 2021 23:06:38 GMT'}

        getReq1 = requests.get(self.uri+'lp.webp',headers=headers_dict)
        print(getReq1.headers)
        print()
        time.sleep(1)

        headers_dict = {'If-Unmodified-Since' : 'Sun, 07 Nov 2021 23:06:38 GMT'}

        getReq2 = requests.get(self.uri+'lp.webp',headers=headers_dict)
        print(getReq2.headers)
        print()
        time.sleep(1)

        headers_dict = {'If-Modified-Since' : 'Fri, 05 Nov 2021 23:06:38 GMT'}

        getReq3 = requests.get(self.uri+'lp.webp',headers=headers_dict)
        print(getReq3.headers)
        print()

        headers_dict = {'If-Modified-Since' : 'Wed, 10 Nov 2021 13:06:38 GMT'}

        getReq4 = requests.get(self.uri+'lp.webp',headers=headers_dict)
        print(getReq4.headers)
        print()
        
        headers_dict = {'Accept-Encoding' : 'gzip', 
                        'Accept':'image/png',
                        'Accept-Charset': 'UTF-8'
                        }

        getReq5 = requests.get(self.uri+'lp.webp',headers=headers_dict)
        print(getReq5.headers)
        print()

        headers_dict = {'Accept-Encoding' : 'gzip', 
                        'Accept':'image/png',
                        'Accept-Charset': 'UTF-16'
                        }

        getReq6 = requests.get(self.uri+'lp.webp',headers=headers_dict)
        print(getReq6.headers)
        print()

        headers_dict = {'If-Match' : getReq3.headers['ETag']}
        getReq7 = requests.get(self.uri+'lp.webp',headers=headers_dict)
        print(getReq7.headers)
        print()

        headers_dict = {'If-Match' : getReq5.headers['ETag']+'9'}
        getReq8 = requests.get(self.uri+'lp.webp',headers=headers_dict)
        print(getReq8.headers)
        print()


    def checkQValue(self):
        headers_dict = {'Accept-Encoding' : 'gzip;q=0.8,deflate',
                        'Accept':'*/*;q=0.8,text/plain;q=0.9'}
        getReq = requests.get(self.uri+'random.txt',headers=headers_dict)
        print(getReq.headers)

    def hardPOSTChecking(self):

        postData = {'college':'COEP','Place':'Pune'}
        postReq = requests.post(self.uri,files = postData)
        print(postReq.headers,postReq.content)

        postData = {'college':'IIT','Place':'Bombay'}
        postReq = requests.post(self.uri,files = postData)
        print(postReq.headers,postReq.content)
    
    def permissionsChecking(self):
        
        #requesting a resource on which read permission is forbidden
        getReq = requests.get(self.uri+'secret.txt')
        print(getReq.content)

        #requesting to modify a resource on which write permission is forbidden
        putData = {'name':'s','surname':'khaire'}
        putReq = requests.put(self.uri + 'secret.txt',data = putData)
        print(putReq.headers,putReq.content)

    def PUTDataOutOfLimit(self):

        request = ("TRACE /img.jpeg HTTP/1.1\r\n"+
        "User-Agent: PostmanRuntime/7.28.4"+
        "Postman-Token: 45ff3ae3-8b6b-43ee-b0ad-906b7c675af8\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Content-Encoding: gzip\r\n"+
        "Content-Type: image/jpeg\r\n\r\n")

        serverName = '127.0.0.1'
        serverPort = 12008
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverName,serverPort))


        clientSocket.send(request.encode())
        modifiedSentence = clientSocket.recv(1024)
        print('From Server: ', modifiedSentence.decode())

    def wrongHTTPVersion(self):
        request = ("GET /viratk.jpeg HTTP/2.0\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Postman-Token: 45ff3ae3-8b6b-43ee-b0ad-906b7c675af8\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Accept-Encoding: gzip\r\n"+
        "Accept-Type: image/jpeg\r\n\r\n")

        serverName = '127.0.0.1'
        serverPort = 12008
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverName,serverPort))


        clientSocket.send(request.encode())
        modifiedSentence = clientSocket.recv(1024)
        print('From Server: ', modifiedSentence.decode())

    def largeRequestLine(self):
        request = ("GET /viratkMYDEARSONMARCUSYOUHAVENOWBEENSTUDYINGINTRODUCTIONTHEIMPORTANCEOFCOMBININGGREEKANDLATINSTUDIESAFULLYEARUNDERCRATIPPUSANDTHATTOOINATHENSANDYOUSHOULDBEFULLYEQUIPPEDWITHTHEPRACTICALPRECEPTSANDTHEPRINCIPLESOFPHILOSOPHYSOMUCHATLEASTONEMIGHTEXPECTEROMTHEPREEMINENCENOTONLYOFYOURTEACHERBUTALSOOFTHECITYTHEFORMERISABLETOENRICHYOUWITHLEARNINGTHELATTERTOSUPPLYYOUWITHMODELSNEVERTHELESSJUSTASIFORMYOWNIMPROVEMENTHAVEALWAYSCOMBINEDGREEKANDLATINSTUDIESANDIHAVEDONETHISNOTONLYINTHESTUDYOFPHILOSOPHYBUTALSOINTHEPRACTICEOFORATORYSOIRECOMMENDTHATYOUSHOULDDOTHESAMESOTHATYOUMAYHAVEEQUALCOMMANDOFBOTHLANGUAGESMYDEARSONMARCUSYOUHAVENOWBEENSTUDYINGINTRODUCTIONTHEIMPORTANCEOFCOMBININGGREEKANDLATINSTUDIESAFULLYEARUNDERCRATIPPUSANDTHATTOOINATHENSANDYOUSHOULDBEFULLYEQUIPPEDWITHTHEPRACTICALPRECEPTSANDTHEPRINCIPLESOFPHILOSOPHYSOMUCHATLEASTONEMIGHTEXPECTEROMTHEPREEMINENCENOTONLYOFYOURTEACHERBUTALSOOFTHECITYTHEFORMERISABLETOENRICHYOUWITHLEARNINGTHELATTERTOSUPPLYYOUWITHMODELSNEVERTHELESSJUSTASIFORMYOWNIMPROVEMENTHAVEALWAYSCOMBINEDGREEKANDLATINSTUDIESANDIHAVEDONETHISNOTONLYINTHESTUDYOFPHILOSOPHYBUTALSOINTHEPRACTICEOFORATORYSOIRECOMMENDTHATYOUSHOULDDOTHESAMESOTHATYOUMAYHAVEEQUALCOMMANDOFBOTHLANGUAGESMYDEARSONMARCUSYOUHAVENOWBEENSTUDYINGINTRODUCTIONTHEIMPORTANCEOFCOMBININGGREEKANDLATINSTUDIESAFULLYEARUNDERCRATIPPUSANDTHATTOOINATHENSANDYOUSHOULDBEFULLYEQUIPPEDWITHTHEPRACTICALPRECEPTSANDTHEPRINCIPLESOFPHILOSOPHYSOMUCHATLEASTONEMIGHTEXPECTEROMTHEPREEMINENCENOTONLYOFYOURTEACHERBUTALSOOFTHECITYTHEFORMERISABLETOENRICHYOUWITHLEARNINGTHELATTERTOSUPPLYYOUWITHMODELSNEVERTHELESSJUSTASIFORMYOWNIMPROVEMENTHAVEALWAYSCOMBINEDGREEKANDLATINSTUDIESANDIHAVEDONETHISNOTONLYINTHESTUDYOFPHILOSOPHYBUTALSOINTHEPRACTICEOFORATORYSOIRECOMMENDTHATYOUSHOULDDOTHESAMESOTHATYOUMAYHAVEEQUALCOMMANDOFBOTHLANGUAGESMYDEARSONMARCUSYOUHAVENOWBEENSTUDYINGINTRODUCTIONTHEIMPORTANCEOFCOMBININGGREEKANDLATINSTUDIESAFULLYEARUNDERCRATIPPUSANDTHATTOOINATHENSANDYOUSHOULDBEFULLYEQUIPPEDWITHTHEPRACTICALPRECEPTSANDTHEPRINCIPLESOFPHILOSOPHYSOMUCHATLEASTONEMIGHTEXPECTEROMTHEPREEMINENCENOTONLYOFYOURTEACHERBUTALSOOFTHECITYTHEFORMERISABLETOENRICHYOUWITHLEARNINGTHELATTERTOSUPPLYYOUWITHMODELSNEVERTHELESSJUSTASIFORMYOWNIMPROVEMENTHAVEALWAYSCOMBINEDGREEKANDLATINSTUDIESANDIHAVEDONETHISNOTONLYINTHESTUDYOFPHILOSOPHYBUTALSOINTHEPRACTICEOFORATORYSOIRECOMMENDTHATYOUSHOULDDOTHESAMESOTHATYOUMAYHAVEEQUALCOMMANDOFBOTHLANGUAGES.jpeg HTTP/1.1\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Postman-Token: 45ff3ae3-8b6b-43ee-b0ad-906b7c675af8\r\n"+
        "Host: 127.0.0.1:12008\r\n"+
        "Accept-Encoding: gzip\r\n"+
        "Accept-Type: image/jpeg\r\n\r\n")

        serverName = '127.0.0.1'
        serverPort = 12008
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientSocket.connect((serverName,serverPort))


        clientSocket.send(request.encode())
        modifiedSentence = clientSocket.recv(1024)
        print('From Server: ', modifiedSentence.decode())


    def mediaTypeTest(self):

        file = open('rich.rtf','rb')

        dataToSend = file.read()

        request = ("PUT /richie.rtf HTTP/1.1\r\n"+
        "User-Agent: PostmanRuntime/7.28.4\r\n"+
        "Postman-Token: 45ff3ae3-8b6b-43ee-b0ad-906b7c675af8\r\n"+
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
        print('From Server: ', modifiedSentence.decode())



if __name__ == '__main__':
    tester = Testing()
    #tester.hardGETtesting()
    #tester.hardPOSTChecking()
    #tester.chec()
    #tester.wrongHTTPVersion()
    #tester.largeRequestLine()
    tester.mediaTypeTest()