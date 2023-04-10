def get_server_uri(server):
    return "http://" + server.server_address[0] + ":" + str(server.server_address[1])