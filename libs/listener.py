#!/usr/bin/python3
#adding of libraries
import os
import sys
import socket

#creating of server socket
def socket_create(host, port):

    #try of defining global variables
    try:
        global s

        s = socket.socket()

    #When an error occurs, information about it is displayed
    except socket.error as msg:
        print(f"\033[30m[-]\033[0m Error: {str(msg)}")

#The appointment of a socket and listen on port
def socket_bind(host, port):
    try:
        global s

        print(f"\033[34m[*]\033[0m Info: Binding on {host} to port {str(port)}")

        s.bind((host, port))
        s.listen(5)

    #Repeat function on failure
    except socket.error as msg:
        print(f"\033[30m[-]\033[0m Error: {str(msg)}Trying again")
        socket_bind()

#accept of connection
def socket_accept(host, port):

    conn, address = s.accept()
    print(f"\033[32m[+]\033[0m Successful: Socket accepted {host}:{str(port)}")
    print("\033[34m[*]\033[0m Enter quit for exit programm")

    #start function for sending and receive commands
    send_commands(conn)
    conn.close()


#function for sending and receive data
def send_commands(conn):
    #creating cycle for input
    while True:
        cmd = input()

        #Checking for the quit command to exit the program
        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()

        #Sending commands to a remote host
        elif len(str.encode(cmd)) > 0:
            #sending command
            conn.send(str.encode(cmd))
            #getting output
            client_response = str(conn.recv(4096), "utf-8")
            print(client_response, end="")

#Main function that starts the previous functions sequentially
def main(host, port):
    socket_create(host, port)
    socket_bind(host, port)
    socket_accept(host, port)
