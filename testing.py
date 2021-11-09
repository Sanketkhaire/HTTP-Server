import requests
from socket import *


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
        headers_dict = {'If-Unmodified-Since' : 'Sat, 06 Nov 2021 23:06:38 GMT',
                        'Accept-Encoding' : 'gzip'}
        getReq = requests.get(self.uri+'lp.png',headers=headers_dict)
        print(getReq.headers)

        headers_dict = {'Accept':'image/png', 
                        'If-Modified-Since' : 'Sat, 06 Nov 2021 23:06:38 GMT',
                        'If-Match' : getReq.headers['Etag'],
                        'Cookie' : getReq.headers['Set-Cookie'].split(';')[0]}

        getReq = requests.get(self.uri+'lp.webp',headers=headers_dict)
        print(getReq.headers)

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


if __name__ == '__main__':
    tester = Testing()
    #tester.hardGETtesting()
    #tester.hardPOSTChecking()
    #tester.chec()
    tester.PUTDataOutOfLimit()