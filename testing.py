import requests
from requests.api import delete


class Testing:
    def __init__(self):
        self.uri = 'http://localhost:12008/'

    def testBasicMethids(self):
        '''get, post, head, put, delete'''
        #get
        getReq = requests.get(self.uri)
        print(getReq.content)

        #head
        headReq = requests.head(self.uri)
        print(headReq.headers)

        #post
        postData = {'name':'sanket','surname':'khaire'}
        postReq = requests.post(self.uri,data=postData)
        print(postReq.headers,postReq.content)

        #put
        file = open('welcome.txt','rb')
        putData = file.read()
        putReq = requests.put(self.uri+'wel.txt',data=putData)
        print(putReq.headers)

        #delete
        delReq = requests.delete(self.uri+'wel.txt',data={'key':'value'})
        print(delReq.headers)




if __name__ == '__main__':
    tester = Testing()
    tester.testBasicMethids()