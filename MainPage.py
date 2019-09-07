from tkinter import *
from tkinter import ttk
import sys
from tkinter import filedialog
import subprocess
import socket
import os
import json
import _thread

class MainPage:
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fileName = None
        self.setupUI()
        self.c = None
        self.imageFileTypes = ("Image Files", ('*.jpg', '*.png', '*.gif', '*.bmp'))
        self.videoFileTypes = ("Video Files", ('*.flv', '*.avi', '*.mp4', '*.mov', '*.mkv', '*.3gp'))
        self.musicFileTypes = ("Music Files", ('*.mp3', '*.wav'))
    
    def setupUI(self):
        self.root = Tk()
        self.root.title("PyShare")
        self.root.resizable(width = False, height = False)
        
        self.mainFrame = Frame(self.root, width = 300, height = 450, background = '#2d2d2d')
        self.mainFrame.pack(fill = None, expand = False)
	
        self.label = Label(self.mainFrame, text = 'PyShare', fg = "white", bg = "#2d2d2d", font = ("Arial", 25))
        self.label.place(x = 10, y = 50, width = 280, height = 30)

        connectPCButton = Button(self.mainFrame, text = 'Connect PC', bg = '#2d2d2d', fg = 'white', bd = 0, font = ("Arial", 14, 'bold'), command = self.waitPage)
        connectPCButton.place(x = 85, y = 150, width = 120, height = 40)
        
        searchPCButton = Button(self.mainFrame, text = 'Search PC', font = ("Arial", 14, 'bold'), bd = 0, bg = '#2d2d2d', fg = 'white', command = self.connectPage)
        searchPCButton.place(x = 85, y = 210, width = 120, height = 40)
        
        #self.label = Label(self.mainFrame, fg = "red", bg = "white", font = "bold")
        #self.label.place(x = 10, y = 420, width = 280, height = 20)
        
        lineStyle = ttk.Style()
        lineStyle.configure("Line.TSeparator", background="#00ffff")

        seperator = ttk.Separator(self.mainFrame, orient=HORIZONTAL, style="Line.TSeparator")
        seperator.place(x = 10, y = 100, width = 280, height = 2)
        
        '''
        self.details = Label(self.mainFrame, bg = "white")
        self.details.place(x = 10, y = 240, width = 280, height = 100)
        '''
        
        #thread.start_new_thread(self.createHotspot, ())
    
    def connectedPage(self):
        self.connectedFrame = Frame(self.root, width = 300, height = 450, background = '#2d2d2d')
        self.connectedFrame.pack(fill = None, expand = False)
    
        self.nameLabel = Label(self.connectedFrame, text='Connected',bg = '#2d2d2d', fg = 'white' )
        self.nameLabel.place(x = 10, y = 5, width = 280, height = 30)
		
        lineStyle = ttk.Style()
        lineStyle.configure("Line.TSeparator", background="#1f0077")

        seperator = ttk.Separator(self.connectedFrame, orient=HORIZONTAL, style="Line.TSeparator")
        seperator.place(x = 10, y = 45, width = 280, height = 3)
        
        self.sendFileButton = Button(self.connectedFrame, text = 'Send Files', font = "bold", bg = '#2d2d2d', fg = 'white', command = lambda: self.sendFiles(self.c, self.sock))
        self.sendFileButton.place(x = 85, y = 410, width = 100, height = 30)
        
        self.recvLabel = Label(self.connectedFrame, anchor = 'nw', bg = '#5d5d5d', fg = 'white')
        self.recvLabel.place(x = 10, y = 60, width = 280, height = 320)
        
        try:
            _thread.start_new_thread(self.recvFiles, (self.sock, self.c, ))
        except Exception as e:
            print(e)

    def waitPage(self):
        self.mainFrame.destroy()
        self.waitFrame = Frame(self.root, width = 300, height = 450, background = '#2d2d2d')
        self.waitFrame.pack(fill = None, expand = False)

        ipLabel = Label(self.waitFrame, text = "IP ADDRESS:\n" + self.getIP(), font=("Courier", 20, 'bold'), fg = 'white', bg = '#2d2d2d')
        ipLabel.place(x = 10, y = 100, width = 280, height = 50)

        lineStyle = ttk.Style()
        lineStyle.configure("Line.TSeparator", background="#ff5400")

        seperator = ttk.Separator(self.waitFrame, orient=HORIZONTAL, style="Line.TSeparator")
        seperator.place(x = 10, y = 170, width = 280, height = 2)		

        instrLabel = Label(self.waitFrame, text = "1. Open PyShare on another PC\n2. Click the search PC and\nenter this IP to connect", font=("Arial", 11), fg = 'white', bg = '#2d2d2d')
        instrLabel.place(x = 10, y = 190, width = 280, height = 80)

        requirementLabel = Label(self.waitFrame, text = "Requirement : \nBoth PC's should be in the same LAN", font=("Arial", 10), fg = 'white', bg = '#2d2d2d')
        requirementLabel.place(x = 10, y = 280, width = 280, height = 50)
		
        self.connectPcThread()
		
    def connectPage(self):
        self.mainFrame.destroy()

        self.connectFrame = Frame(self.root, width = 300, height = 450, background = '#2d2d2d')
        self.connectFrame.pack(fill = None, expand = False)

        label = Label(self.connectFrame, text = 'Enter IP', font = ("Courier", 18, 'bold'), bg = '#2d2d2d', fg = 'white')
        label.place(x = 85, y = 150, width = 120, height = 40)

        self.enterIP = Entry(self.connectFrame, bg = '#4d4d4d', fg = 'white', font = ("Courier", 10))
        self.enterIP.place(x = 85, y = 200, width = 120, height = 20)

        connectButton = Button(self.connectFrame, text = 'Connect', font = "bold",bg = '#2d2d2d', fg = 'white', command = self.searchPC)
        connectButton.place(x = 85, y = 240, width = 120, height = 40)

        self.errorLabel = Label(self.connectFrame, bg = '#2d2d2d', fg = 'red', font = ("Courier", 12))
        self.errorLabel.place(x = 10, y = 300, width = 290, height = 40)

    def getIP(self):
    	try:
    		ip = socket.gethostbyname_ex(socket.gethostname())
    		return ip[2][0]
    	except:
    		return '127.0.0.1'
       
    def getSSID(self):
        try:
            ssid = subprocess.check_output("netsh wlan show interfaces | findstr /i SSID", shell = True)
        except:
            return
        ssid = ssid.split("\r\n")
        
        if len(ssid) == 0:
            return
        
        ssid1 = ssid[0].split(":")
        return ssid1[1]
        
    def createHotspot(self):
        try:
            output = subprocess.check_output("netsh wlan show drivers", shell=True)
            if "Hosted network supported  : Yes" not in output:
                self.label['text'] = "Device Not Supported"
                return
            output = subprocess.check_output("whoami /groups", shell=True)
            if 'S-1-16-12288' not in output:
                self.details['text'] = "Waiting for client...\nHotspot Name : " + "\nPassword : " + "\nInitialization Failed"
                self.label['text'] = "Run as Administrator"
                _thread.exit()
                return
                
            ssid = "FileShare"
            password = "abcd12345"

        
            cmd = "netsh wlan set hostednetwork mode=allow ssid=" + ssid + " key=" + password
            output1 = subprocess.check_output(cmd, shell = True, stderr = subprocess.STDOUT)
            if "successfully changed" in output1:
                output = subprocess.check_output("netsh wlan start hostednetwork", shell = True)
                if "started" in output:
                    self.details['text'] = "Waiting for client...\nHotspot Name : " + ssid + "\nPassword : " + password
                else:
                    self.details['text'] = "Initialization Failed\n Both PCs should be in the same LAN"
        except Exception as e:
                print(e)


    def createServer(self):
        print(self.getIP())
        host = self.getIP()                         
        port = 12345
        self.sock.bind((host, port))
        
    def connectPC(self):
        self.createServer()
        self.sock.listen(1)

        self.c, addr = self.sock.accept()
        
        self.waitFrame.destroy()
        self.connectedPage()
            
    def connectPcThread(self):
        _thread.start_new_thread(self.connectPC, ())
    
    def searchPC(self): 
        host = self.enterIP.get()#"127.0.0.1"#"192.168.0.107"
        port = 12345
        
        try:
            self.sock.connect((host, port))
        except:
            self.errorLabel["text"] = 'Please enter valid IP'
            return
        
        self.connectFrame.destroy()
        self.connectedPage()
                
    def sendFiles(self, *s):
        text = ''
        file1 = filedialog.askopenfilenames(title='Choose a file', filetypes = (('All Files', '*.*'), self.imageFileTypes, self.videoFileTypes, self.musicFileTypes))
        filelist = self.root.tk.splitlist(file1)
        if not filelist:
            return
        
        for i in range(len(s)):
            try:
                sock = s[i]
                for file in filelist:
                    size = int(os.path.getsize(file))
                    filename = file.split("/")
                    data = {'size' : size, 'filename' : filename[-1]}
                    data = json.dumps(data)
                    text += "Sent : " + filename[-1] + "\n\n"
                    sock.send(data.encode())
                    f = open(file,'rb')
                    totalsend = 0
                    while totalsend!=size: 
                        l = f.read(1024)
                        totalsend += len(l)
                        sock.send(l)
                    f.close()
                    self.recvLabel['text'] = text
            except:
                pass

    def sendFilesThread(self):
        _thread.start_new_thread(self.sendFiles, ())

    def makedir(self, ext):
        ext = '*' + ext
        if ext in self.imageFileTypes[1]:
            if not os.path.isdir("./FileShare/Images"):
                os.mkdir("./FileShare/Images")
            return "./FileShare/Images/"
        elif ext in self.videoFileTypes[1]:
            if not os.path.isdir("./FileShare/Videos"):
                os.mkdir("./FileShare/Videos")
            return "./FileShare/Videos/"
        elif ext in self.musicFileTypes[1]:
            if not os.path.isdir("./FileShare/Music"):
                os.mkdir("./FileShare/Music")
            return "./FileShare/Music/"
        else:
            if not os.path.isdir("./FileShare/Other"):
                os.mkdir("./FileShare/Other")
            return "./FileShare/Other/"
			
    def recvFiles(self, *s):
        text = ''
        if not os.path.isdir("./FileShare/"):
            os.mkdir("./FileShare/")
        for i in range(len(s)):
            try:
                sock = s[i]
                while True:
                    data = sock.recv(1024)
                    print(data)
                    data = json.loads(data.decode())
                    filename = data['filename']
                    size = int(data['size'])
                    text += "Received : " + filename + "\n\n"
                    name, ext = os.path.splitext(filename)
                    filename = self.makedir(ext) + filename
                    f = open(filename,'wb')
                    totalrecv = 0
                    while totalrecv!=size:
                        l=sock.recv(1024)
                        totalrecv += len(l)
                        f.write(l)
                    f.close()
                    self.recvLabel['text'] = text
            except:
                pass

if __name__ == '__main__':
    m = MainPage()
    mainloop()
    m.sock.close()