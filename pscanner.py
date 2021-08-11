import threading, socket, colorama, time, sys
from queue import Queue
from colorama import Fore

colorama.init()
print_lock = threading.Lock()
ip = input("Enter IP: ")
try:
    host = socket.gethostbyname(ip)
except socket.gaierror:
    print(f"{Fore.RED}Enter Valid IP Address!")
    sys.exit()
print(f"{Fore.YELLOW + ip} => {Fore.GREEN + host}")
prange = int(input(f"{Fore.WHITE}Enter port to scan upto: "))
print(f"Scanning host: {Fore.GREEN + host}")

def portscan(port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    con = s.connect((host, port))
    with print_lock:
      print(Fore.WHITE + f"[{port}]", Fore.GREEN + "Open")
    con.close()
  except:
    pass

def threader():
  while True:
    worker = q.get()
    portscan(worker)
    q.task_done()

q = Queue()
start_time = time.time()

for x in range(1000):
  t = threading.Thread(target=threader)
  t.daemon = True
  t.start()

for worker in range(1, prange):
  q.put(worker)

q.join()
time_elapsed = time.time() - start_time
print(f"Finished Scanning in {round(time_elapsed)} seconds!")
