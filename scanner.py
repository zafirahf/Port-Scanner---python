import socket
import sys
from datetime import datetime
from queue import Queue
import threading


#cmd argument handling
if len(sys.argv)==2: #ensures user provides 2 arguments, including a target
    target=socket.gethostbyname(sys.argv[1])  #converts ip/hostname to ip addr 
else: 
    print ("Usage: py scanner.py <target_ip_or_hostname>")
    sys.exit(1) 

#banner display
print("-" * 50)
print(f"Scanning target: {target}")
print(f"Time started: {datetime.now()}")
print("-" * 50)


#threading
port_queue = Queue() #creating a queue to store the ports that are yet to be scanned
open_ports = [] #to store all the open ports 
lock = threading.Lock() #using the same lock(key) for all the threads to overcome race conditions

#debug code
print(f"Adding ports to queue...")
for port in range(1, 101):
    port_queue.put(port)
print(f"Queue size: {port_queue.qsize()} ports added")

def worker_function(target): 
    while not port_queue.empty(): 
        port = port_queue.get() #take a port from the port queue
        print(f"Scanning port: {port}") 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #instructs socket to use IPv4 and TCP
        socket.setdefaulttimeout(2) #sets timeout to 2 seconds
        result = sock.connect_ex ((target, port)) #connect_ex returns error code, else 0 which indicates open port
        if result == 0:
            print(f"FOUND OPEN PORT: {port}")   
            with lock: #to prevent race conditions 
                open_ports.append(port) #add it to the list of open ports once scanned and verified
        sock.close()
        port_queue.task_done() #to indicate that the "task is done" and to remove it from the queue

try: 
    threads = [] #to store all the threads created
    for i in range(100): 
        thread = threading.Thread(target=worker_function, args=(target,)) #create a thread to run the worker_function with the target as an argument
        thread.start()
        threads.append(thread) #to keep track of all the threads created

    for thread in threads:
        thread.join() #to wait for all the threads to complete before proceeding further


#error handling
except KeyboardInterrupt: 
    print("Error: Scan interrupted by the user!")
    sys.exit(0)

except socket.gaierror: #invalid hostname
    print("Error: Hostname could not be resolved; exiting")
    sys.exit(1)

except Exception as e: 
    print(f"Unexpectedw error: {type(e).__name__}")
    sys.exit(1)


#port service name
def identify_service(port): 
    try: 
        service = socket.getservbyport(port, 'tcp') #gives name of port service (from local dir)
        return service

    except OSError: #unknown port service name
        return "Unknown service"


#results displayed:
print("-" * 50)
print(f"Scan completed at: {datetime.now()}")
print("-" * 50)

if open_ports:
    open_ports.sort()
    print(f"Found {len(open_ports)} open ports:")
    print("-" * 30)
    for port in open_ports:
        service = identify_service(port)  # ← USING YOUR FUNCTION!
        print(f"Port {port}: OPEN - {service}")
else:
    print("No open ports found in range 1-1023")

print("-" * 50)
print("Scan complete!")


# #scanning loop
# try: 
#     for port in range(1,1024):
#         sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #instructs socket to use IPv4 and TCP
#         socket.setdefaulttimeout(1) #sets timeout to 1 second 
#         result = sock.connect_ex((target, port)) #connect_ex returns error code, else 0 which indicates open port
#         if result == 0: 
#             print(f"Port {port}: OPEN")
#             sock.close()