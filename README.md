Tools and concepts
    Python 3: socket, threading, queue, sys, datetime
    Networking: TCP/IP protocol, 3-way handshake, DNS resolution, port numbers
    Concurrency: Thread pooling, queue management, race condition prevention
    
Components
    1. Threads: Uses 100 concurrent threads to scan ports parallely, thus reduces time taken to         scan compared to single-threaded approach.
    2. Thread-safe functions: queue.Queue and threading/Lock() to prevent race conditions and           ensure safe data handling across all threads
    3. Service detection: Resolves the open ports to their service name with local device db
    4. Error Handling: Catches the DNS resolution failures and unexpected network errors
    5. Clean output: formatted banner

System process:
    1. Script generates ports 1-1023 and puts them in a queue
    2. The threads act as 100 workers working parallely, all working the same worker_function that      is assigned to them. Each thread (worker) pulls a port from queue, creates a socket, and           attempts TCP conncetion (3-way handshake with the help of connect_ex). 
    3. When thread finds open port, it should get a lock before adding it to the list of                 open_ports. Helps prevent race conditions where multiple threads are trying to modify the          same list at the same time, which would cause data loss. 
    
    
    
