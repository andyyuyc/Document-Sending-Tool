import sys 
import xmlrpc.client 
import socket

PORT = 8888
password = ''
# Reciever Address 
addr = "127.0.0.1"
# Store File 
def save_data(File_Name , data):
    handle = open(File_Name, "w")
    handle.write(data)
    handle.close()

# Store Binary File
def save_binary_data(File_Name , binary_data):
    handle = open(File_Name , "wb")
    handle.write(binary_data.data)
    handle.close()

def main():
    global password

    #get the host_name 
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(local_ip)
    # connect to server
    server = xmlrpc.client.ServerProxy('http://'+ addr +':'+str(PORT))

    num = int(input("please enter a number 1. Send , 2. Get , 3.Store"))
    

    # here is put the File Address and get the file format 
    File_Address = "C://Users//Administrator//Desktop//test.txt"
    File_Format =  File_Address[File_Address.index("."):]
    print(File_Format)

    #File is txt
    #add txt 
    
    if(num == 1): 
        #pass 

        File_Name = File_Address+File_Format
    
    #with open("C://Users//Administrator//Desktop//test.txt", "rb") as handle:
    #binary_data = xmlrpc.client.Binary(handle.read())
    #text file

        if(File_Format == ".txt"):
            f = open("C://Users//Administrator//Desktop//test.txt", "r")
    #doc = docx.Document("C://Users//Administrator//Desktop//text.docx")
        else:
            f = open("C://Users//Administrator//Desktop//課表.pdf" , "rb")
    
        data = f.read()
    
        File_Name = input("please enter your File name : ")
        Receive_IP = input("please enter recieve ip : ")

        server.Send_File(Receive_IP , File_Name , data , local_ip , File_Format)
    elif(num == 2):
        File_Name = input("please enter which File name you want : ")
        #Receive_IP = input("please enter recieve ip : ")

        new_data = server.Get_File(File_Name , local_ip)
        new_address = "C://Users//Administrator//Desktop//school//網路程式設計//Demo//Server_2_Client//"+File_Name
        save_data(new_address , new_data)
    elif(num ==3 ):
        password = input("please enter your password : ")
        server.register(local_ip , password)
    elif(num ==4 ):
        password = input("please enter your password : ")
        check = server.login(local_ip , password)
        print(check)
if __name__ == "__main__":
    main()