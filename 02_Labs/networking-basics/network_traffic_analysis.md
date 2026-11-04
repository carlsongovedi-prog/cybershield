# CyberShield Network Traffic Analysis

## 1. Lab Information

Lab: Week 2 - TCP and HTTP Traffic Analysis
Environment: Local macOS training environment
Capture interface: lo0 (loopback)
Server address: 127.0.0.1
Server port: 8000
Client port: 59873
Tool: tcpdump

## 2. Objective

Observe and interpret a local TCP connection and HTTP exchange.
Identify the TCP handshake, HTTP request, server response,
and potential security weaknesses.

## 3. Observations

- 12 packets captured.
- 27 packets received by filter.
- 0 packets dropped by kernel.
- Client connected to local server on port 8000.
- HTTP GET request successfully received.
- Server returned HTTP 200 OK.

## 4. TCP Three-Way Handshake

The capture shows:

1. SYN: Client requests a TCP connection.
2. SYN-ACK: Server acknowledges and responds.
3. ACK: Client acknowledges the server.

The connection is established successfully.

## 5. HTTP Communication

The client sent:

GET / HTTP/1.1
Host: 127.0.0.1:8000

The server responded:

HTTP/1.0 200 OK

The response indicates that the requested resource was served
successfully.

## 6. Security Observation

The capture contains:

secret-token=ABC123

This demonstrates that application data can be visible
in an unencrypted HTTP response.

Risk: Sensitive information transmitted over plaintext HTTP
may be exposed to anyone able to observe the traffic.

This is a controlled training example, not evidence of
an external compromise.

## 7. Recommendations

- Use HTTPS with properly configured TLS.
- Never transmit real credentials or tokens over plaintext HTTP.
- Avoid exposing secrets in application responses.
- Store secrets securely and restrict access.
- Review application logs and network traffic for accidental
  disclosure of sensitive information.

## 8. Limitations

- Testing was restricted to the local loopback interface.
- Only one observed HTTP exchange was analyzed.
- No external hosts or third-party systems were tested.
- The sample token is treated as dummy training data.

## 9. Conclusion

The lab demonstrated TCP connection establishment,
HTTP request-response communication, and the visibility
of plaintext application data.

The exercise reinforces the importance of encryption
and secure handling of application secrets.

## 10. Evidence

Capture file: evidence/week2-tcpdump.txt
