import json
import socket
from ExtCommands.TextCommands import *
from ExtCommands.JSONCommands import *


HOST = '127.0.0.1'
PORT = 65432


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    endTCPServer = False

    while True:
        
        if endTCPServer:
            break

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            
            while conn:
                
                data = conn.recv(131072)
                
                if not data:
                    break            
                
                try:
                    JasonData = json.loads(data.decode())
                    CommandResult = JSONCommands.processCommand(JasonData)
                    conn.sendall(CommandResult)
                except ValueError as e:
                    CommandResult = TextCommands.ProcessCommand(data)
                    if CommandResult == "TCP SERVER KILLED".encode():
                        conn.sendall(CommandResult)
                        endTCPServer = True
                        break
                    else:
                        conn.sendall(CommandResult)

                    
