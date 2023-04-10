from server_instance import return_server_instance
from vm_passing_memory import SharedMemoryManager
import requests
from utils import get_server_uri
import multiprocessing

SERVER_ADDRESS = "127.0.0.1"

server_details = [
    (SERVER_ADDRESS, 8000),
    (SERVER_ADDRESS, 8100)
]

if __name__ == '__main__':
    servers = []
    for s in server_details: 
        p = multiprocessing.Process(
            target=return_server_instance, 
            args=(s[0], s[1])
        )
        servers.append(p)  

    for server in servers:
        server.start()

    for server in servers:
        server.join()


