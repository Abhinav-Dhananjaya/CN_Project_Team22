Project Title: Custom Port Scanner with Service Detection (Team 22)

Problem Statement: A secure, multi-threaded tool to identify open TCP ports and grab service banners.

Architecture : 
   This project implements a Distributed Secure Port Scanning system using a Client-server model. The architecture is designed to handle high-concurrency network 
probes while maintaining data integrity through encryption.
  The system consists of two primary modules :
     * The multi - threaded scanner(client) : Responsible for probing target IP addresses and performing service detection
     * The secure log server : A centralized repository that listens for and records scan results reported by client over an encrypted channel
  The Communication overflow  :
      The interaction follows a specific sequence to ensure both performance and security :
        * TCP three - way handshake : The scanner uses low-level socket.connect_ex() to initiate a TCP handshake with the target port
        * Service detection(Banner grabbing) : If the port is open, the scanner sends a probe and waits for a response to identify the service version(eg: SSH,HTTP)
        * SSL/TLS handshake: Once a service is identified , the scanner initiates a mandatory SSL/TLS handshake with the Log Server using ssl.SSLContext
        * Secure Data transfer : The encrypted scan results are sent to the server , ensuring that data is protected from network sniffing
  Logic flow diagram : 
   The scanner operates by dividing the port range into chunks, which are processed in parallel by the thread pool.Each thread independently manages its own socket 
lifecycle .  Creation --> Connection --> Detection --> Reporting --> Closure to maximise throughput.

Performance evaluation  :
When the system was scanned under high request rates , it scanned 1024 ports in 0.40 seconds when I run it first. We have used a concurrency model which uses a 
multi-threaded approach with 100 worker threads to manage simultaneous TCP connections . By parallelizing the socket connect_ex calls , the scanner achieves a 
significantly higher throughput compared to sequential scanning.

This project avoids high level libraries ( like Nmap) and uses the Python socket module directly for fine-grained control over the TCP handshake.
Using Banner Grabbing, it implements a post-connection probe to capture service banners , identifying the software running on open ports.
Each socket connection has a settimeout(1.0) to ensure the scanner remains responsive even when encountering filtered ports or network latency

Security Features :
  There is an SSL/TLS encryption where all data exchanges between the scanner and the log server are encrypted using the TLS 1.3 protocol
  It uses X.509 certificates(cert.pem) and private keys(key.pem) to establish a secure identity for the Log server

To generate certificate  :
     openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
To start the Secure Server :
     python3 secure_server.py
To run the threaded scanner : 
     python3 scanner_threaded.py

Design : Established the secure communication protocol between scanner and server
Development : Implemented low-level TCP socket logic and SSL wrapping
Testing : Performed performance evaluation and optimised thread counts to achieve the 0.40s scan time
