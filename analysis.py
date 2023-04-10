import requests
from uuid import uuid4
import datetime
 
sample_data_object = {
    "id": uuid4(),
    "timestamp": datetime.datetime.now()
}

def analyse_direct_passing_method(server1_address, server2_address):
    SERVER1_CONN_URI = server1_address
    SERVER2_CONN_URI = server2_address
    data = sample_data_object
    data["PEER_SERVER_CONN_URI"] = SERVER2_CONN_URI
    response = requests.post(SERVER1_CONN_URI, sample_data_object)
    duration = float(str(response.content, 'UTF-8'))
    return duration
    
def analyse_remote_passing_method(server1_address, server2_address):
    SERVER1_CONN_URI = server1_address
    SERVER2_CONN_URI = server2_address
    data = sample_data_object
    res1 = requests.put(SERVER1_CONN_URI, data)
    duration = res1.elapsed.total_seconds()
    res2 = requests.get(SERVER2_CONN_URI)
    duration = duration + res2.elapsed.total_seconds()
    return duration

duration1 = analyse_direct_passing_method("http://127.0.0.1:8000", "http://127.0.0.1:8100")
duration2 = analyse_remote_passing_method("http://127.0.0.1:8000", "http://127.0.0.1:8100")
print("Direct Passing Method:", duration1)
print("Remote Passing Method:", duration2)
