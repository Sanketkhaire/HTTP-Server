<p align="center">
 <img width=200px height=200px src="others/server.jpg" alt="logo"></a>
</p>

<h3 align="center">myHTTP Server</h3>

---

<p align="center">myHTTP server is a HTTP/1.1 compliant web server which handles common web requests.</p>

<!--
## 📝 Table of Contents

- [What is myHTTP?](#what)
- [How to use it?](#how)
- [Built Using](#built_using)
- [Author](#author)
- [References](#references)
 -->

## Introduction
This project implements a simple multithreaded HTTP/1.1 compliant web server designed to handle various HTTP requests (GET, POST, PUT, DELETE, etc.), manage cookies, support multipart form data, and handle basic logging and error management. This server was built to explore the inner workings of the HTTP protocol, server design, and request handling, and is based on the HTTP/1.1 RFC 2616.

---

## Features

1. **HTTP Methods Implementation**  
   - Supports core HTTP methods including `GET`, `POST`, `PUT`, `DELETE`, `HEAD`.

2. **Multipart Form Data Handling**  
   - Ability to process multipart form data for file uploads and form submissions.

3. **Logging**  
   - Implements **access logs** and **error logs** to track request details and server issues.

4. **Customized Configuration File**  
   - Allows server configuration through a user-friendly `.conf` file.

5. **Cookies**  
   - Support for setting and retrieving cookies between the client and server for session management.

6. **Access Logs**  
   - Provides detailed logs of all incoming requests, including IP address, request time, and response status.

7. **Error Logs**  
   - Detailed logging of any errors, including error types and affected resources.

---

## Instructions

### 1. Starting the Server

To start the server, use the following command:

```bash
bash start.sh
```

### 2.Stopping the Server

To stop  the server, use the following command:

```bash
bash stop.sh
```

### 3.Run the testcases

To test the server, you can use the testing.py script, which will do regression testing
```bash
python testing.py
```

## Configuration File 
The config file contains the server’s configuration settings. Below is the format of the configuration file:

```bash
[DOCUMENTROOT]
DocumentRoot = httpfiles/

[POSTROOT]
PostRoot = POST/

[PUTROOT]
PutRoot = PUT/

[PIDFILE]
pidfile = pid.txt

[TIMEOUT]
TimeOut = 300

[KEEP_ALIVE]
KeepAlive = Off

[MAX_KEEP_ALIVE_REQUESTS]
MaxKeepAliveRequests = 5

[KEEP_ALIVE_TIMEOUT]
KeepAliveTimeout = 20

[ACCESSLOG]
AccessLog = logs/access.log

[ERRORLOG]
ErrorLog = logs/error.log

[MAX_SIMULTANEOUS_CONNECTION]
MaxSimultaneousConnection = 5

[PORT_NUMBER]
PortNumber = 12001

```


 ## Logs

### Access Logs

The server maintains an access log for all incoming requests. This log helps monitor server activity and understand client interactions. Below is an example of an access log entry:
 ```bash

 127.0.0.1:50126 - [Sun, 14 Nov 2021 17:23:09 GMT] “GET / HTTP/1.1” 200 3148 python-requests/2.22.0
```
#### Explanation of Access Log Fields:
1. **Client IP Address**: `127.0.0.1` indicates the source of the request.
2. **Port**: `50126` is the port number used by the client.
3. **Timestamp**: `[Sun, 14 Nov 2021 17:23:09 GMT]` records the date and time of the request.
4. **Request Method and URI**: `"GET / HTTP/1.1"` shows the HTTP method (`GET`) and the requested resource (`/`).
5. **Status Code**: `200` indicates the request was successful.
6. **Response Size**: `3148` bytes were sent to the client.
7. **User-Agent**: `python-requests/2.22.0` shows the client application making the request.

---

### Error Logs

The server logs errors encountered while processing client requests. Error logs help identify and debug issues with the server or incoming requests. Below is an example of an error log entry:

```bash
127.0.0.1:50128 - [Sun, 14 Nov 2021 17:23:09 GMT] “GET /index23.html HTTP/1.1” 404 Not Found python-requests/2.22.0 Client-Error:4xx
```
#### Explanation of Error Log Fields:
1. **Client IP Address**: `127.0.0.1` indicates the source of the request.
2. **Port**: `50128` is the port number used by the client.
3. **Timestamp**: `[Sun, 14 Nov 2021 17:23:09 GMT]` records the date and time of the request.
4. **Request Method and URI**: `"GET /index23.html HTTP/1.1"` shows the HTTP method (`GET`) and the requested resource (`/index23.html`).
5. **Status Code and Description**: `404 Not Found` indicates the requested resource could not be found on the server.
6. **User-Agent**: `python-requests/2.22.0` shows the client application making the request.
7. **Error Type**: `Client-Error:4xx` indicates the error type, in this case, a client-side error.

---

### Log File Locations

- **Access Log**: `logs/access.log`
- **Error Log**: `logs/error.log`

These log files are specified in the `config` file and can be customized based on your requirements.


## Acknowledgments

This project would not have been possible without the following resources and contributions:  

- **[MDN Web Docs](https://developer.mozilla.org/)**: For comprehensive documentation on HTTP and web technologies.  
- **[RFC 2616](https://datatracker.ietf.org/doc/html/rfc2616)**: The foundational standard for HTTP/1.1 protocol implementation.  

