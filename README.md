<p align="center">
 <img width=200px height=200px src="others/server.jpg" alt="logo"></a>
</p>

<h3 align="center">myHTTP Server</h3>

---

<p align="center">myHTTP server is a HTTP/1.1 compliant web server which handles common web requests.</p>

## 📝 Table of Contents

- [What is myHTTP?](#what)
- [How to use it?](#how)
- [Built Using](#built_using)
- [Author](#author)
- [References](#references)
 

## 👉 What is myHTTP? <a name = "what"></a>

myHTTP server is an implementation of RFC 2616 based HTTP/1.1 protocol which includes methods such as 'GET', 'HEAD', 'POST', 'PUT' and 'DELETE'


## 👉 How to use it? <a name = "how"></a>

### Configurations

Following configurations should be done if needed and serverconfig.py file must be run before starting the server.

```
DOCUMENT-ROOT = document root directory for serving requests
MAX-CONNECTION = maximum number of simultaneous connections possible
PORT = port number for serving requests
KEEP-ALIVE = to allow persistent connections or not
TIMEOUT = default timeout value for persistent connections
LOG-LEVEL = level of logging
LOG-DIRECTORY = directory where logs will be saved
ERROR-LOGS = file in which error logs will be saved
ACCESS-LOGS = file in which error logs will be saved
LOG-FORMAT = format of logging to be followed
COOKIE-FILE = file in which unique cookie number and number of times this cookie number was used is stored 
```

For starting the myHTTPserver :
```
./start.sh
```

For stopping the myHTTPserver :
```
./stop.sh
```

For restarting the myHTTPserver :
```
./restart.sh
```


## 👉 Built Using <a name = "built_using"></a>

- Python


## 👉 Author <a name = "author"></a>
- [@Sanket Khaire](https://github.com/Sanketkhaire)


## 👉 References <a name = "references"></a>

- RFC2616
- https://www.iana.org/assignments/media-types/media-types.xhtml       ----> for mediatypes and their extensions
- MDN docs
