from xmlrpc.server import SimpleXMLRPCDispatcher, SimpleXMLRPCServer
import mysql.connector
import docx
import os 

connection = mysql.connector.connect(host = "localhost",
                                    port = 3306 , 
                                    user = 'root' ,
                                    password = 'xiang8912300965233705',
                                    database = 'File_Address' )

cursor = connection.cursor()





PORT = 8888

# insert File to DB
def Insert_DB(Recieve_IP , File_Address , Sender_IP):
    print("entry")
    sql = "INSERT INTO Address (Sender_IP, File_Address , Reciever_IP) VALUES (%s,%s,%s)"
    value = (Sender_IP,File_Address,Recieve_IP)
    print("Insert DB")
    cursor.execute(sql , value)
    connection.commit()

# delete DB_File     
def Delete_DB(File_Address):
    print("Delete File")
    sql = "DELETE FROM address WHERE File_Address = %s "
    value = (File_Address ,)
    cursor.execute(sql , value)
    connection.commit()

# get the Information from DB
def Get_the_Information_From_DB(Receive_IP):
    sql = "SELECT Sender_IP , File_Address FROM address WHERE Reciever_IP = %s "
    val = (Receive_IP ,)
    cursor.execute(sql , val)

    information = cursor.fetchall()
    
    for i in information:
        print(i)
    #print(information)

def user_register_To_DB(Local_IP , password):
    sql = "INSERT INTO user (Local_IP , password) VALUES (%s,%s)"
    value = (Local_IP , password)

    cursor.execute(sql , value)
    connection .commit()

def Login_check(Local_IP):
    sql = "SELECT password FROM user WHERE Local_IP = %s "
    val = (Local_IP , )
    cursor.execute(sql , val)
    #print(cursor.fetchone())
    infor = cursor.fetchone()
    print("check "+str(infor[0]))
    return infor[0]

    

# Store File to Database
def Store_File_To_Database(Recieve_IP , Name , Sender_IP):
    Insert_DB(Recieve_IP , Name , Sender_IP)

# Send File to Reciever
def Send_File_To_Reciever(File_Address):
    Delete_DB(File_Address)
    print("Get2")

# Store File to local Server
def save_data(File_Name , data):
    handle = open(File_Name, "w")
    handle.write(data)
    handle.close()

# Store Binary File to local Server
def save_binary_data(File_Name , binary_data):
    handle = open(File_Name , "wb")
    handle.write(binary_data.data)
    handle.close()

def Send_File_To_Receiver(Receive_IP , File_Address):
    format = File_Address[File_Address.index("."):]

    if(format == ".txt"):
        f = open(File_Address, "r")
        data = f.read()
        print("Send Finish")
        return data 
    else:
        f = open(File_Address ,"rb")
        data = f.read()
        print("Send Finish")
        return data


class File_Access : 

    def Send_File(self , Recieve_IP , File_Name , data ,Sender_IP,File_Format):
        print(Sender_IP)
        Store_File_To_Database(Recieve_IP=Recieve_IP , Name=File_Name , Sender_IP = Sender_IP )

        if(File_Format == ".txt"):
            save_data(File_Name , data)
        else:
            save_binary_data(File_Name , data)
        print("Send")

    def Get_File(self , File_Address,Receive_IP):
        #Send_File_To_Reciever(File_Adress = File_Address)
        #Delete_DB(File_Address)    
        #Get_the_Information_From_DB(Receive_IP=Receive_IP)
        print("Get") 
        return Send_File_To_Receiver(Receive_IP , File_Address)

    def register(self , Local_IP , password):

        user_register_To_DB(Local_IP  , password)
        path = Local_IP
        print(path)
        if not os.path.isdir(path):
            os.mkdir(path)
        
    def login(self , Local_IP , password ):
        check_password = Login_check(Local_IP = Local_IP)
        print(check_password)
        if(check_password == password):
            return True 
        else :
            return False


def main():
    obj = File_Access()
    server = SimpleXMLRPCServer(("localhost" , PORT),allow_none=True)
    print("Listening on port %d..." % PORT)
    server.register_instance(obj)
    server.serve_forever()


if __name__ == '__main__':
    main()