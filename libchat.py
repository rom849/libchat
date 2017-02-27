#!/usr/bin/python
# -*- coding: utf-8 -*-

#48BRN3o23IOP

import socket, select
import argparse

#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, xs, message, onlyToSelf = False):
    #Do not send the message to master socket and the client who has send us the message
    for xs in CONNECTION_LIST:

        socket = xs.socket
        if socket != server_socket and ((socket != sock) != onlyToSelf):
            try:
                MSG = message
                messagex = map(ord,MSG)
                values = []
                values.append(len(MSG))
                values.extend(messagex)
                values = bytearray(values)
                #self.request.sendall(values)
                socket.send(values)
            except:
                try:
                    socket.close()
                    CONNECTION_LIST.remove(xs)
                    

                    
                except Exception as e:
                    print ("err12")+str(e)

class Connection(object):
	def __init__(self, sock):
		self.socket = sock

	nick = ""

	def fileno(self):
		return self.socket.fileno()

if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--port', help='Description for foo argument', required=True)
    args = parser.parse_args()


    PORT = int(args.port)
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections



    CONNECTION_LIST.append(Connection(server_socket))
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        try:
            # Get the list sockets which are ready to be read through select
            read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
     
            for xs in read_sockets:
                sock = xs.socket
                #New connection
                if sock == server_socket:
                    # Handle the case in which there is a new connection recieved through server_socket
                    sockfd, addr = server_socket.accept()
                    CONNECTION_LIST.append(Connection(sockfd))
                    print "Client (%s, %s) connected" % addr
                     
                    broadcast_data(sockfd, xs, "[%s:%s] entered room\n" % addr)
                 
                #Some incoming message from a client
                else:
                    # Data recieved from client, process it
                    try:
                        #In Windows, sometimes when a TCP program closes abruptly,
                        # a "Connection reset by peer" exception will be thrown

                        data = sock.recv(RECV_BUFFER)
                        if data:
                            if "count$" in str(data):
                                broadcast_data(sock, xs, "\r" + '' + 'count' + '##' + str(len(CONNECTION_LIST)), True) 

                            if "nick$" in str(data):
                            	xs.nick = data.replace("nick$", "")
                            else:
                                if len(xs.nick) > 1:
    	                            broadcast_data(sock, xs, "\r" + '' + str(xs.nick) + '##' + data) 
                                else:
    	                            broadcast_data(sock, xs, "\r" + '' + str(sock.getpeername()) + '##' + data) 
                            print ("Client (%s, %s) sent " % addr)+ str(xs.nick) + ": "+ str(data) + " -- " + str(len(CONNECTION_LIST))            
                     
                    except Exception as e:

                        broadcast_data(sock, xs, "Client (%s, %s) is offline" % addr)
                        print ("Client (%s, %s) is offline " % addr)+str(e)
                        try:
                            sock.close()
                            CONNECTION_LIST.remove(xs)
                            
                        
                            
                        except Exception as e:
                            print ("err1")+str(e)
                        continue
        except Exception as e:
            print ("err1")+str(e)
            break
     
    server_socket.close()
