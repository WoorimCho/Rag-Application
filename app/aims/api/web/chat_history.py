from datetime import date, datetime
import os
from dotenv import load_dotenv

load_dotenv()

class Chat_History():

    def __init__(self): #Things that get loaded on booting up
        temp_file = os.getenv("TEMP_FOLDER")
        file_path = temp_file+"/_log/"
        current_date_time_stamp = datetime.now().strftime("%Y-%m-%d")
        self.chat_file = file_path + "Chat_Histoy" + current_date_time_stamp +".txt"
        self.chat_log = file_path + "Chat_Log" + current_date_time_stamp +".txt"
        
        try:
            if os.path.getsize(self.chat_file) != 0:
                with open(self.chat_file, "a+") as file:
                    file.write("_"* 50 + "\n")
        except FileNotFoundError:
            with open(self.chat_file, "a+") as file:
                    file.write("Please enter prompt or Select a file to Upload\n\n")
        finally:
            with open(self.chat_log, "a+") as log:
                log.write("*"*50)
                log.write("Opening the chat")
                log.write("*"*50+"\n\n")
        

    def add(self, user, message):
        timestamp = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

        with open(self.chat_log, "a+", encoding="utf-8") as file:
            file.write("["+timestamp+"] >>> " + user + ": \n\t" + message + "\n\n")
            
        if "Chat" in user:
            user = "Chat"
        with open(self.chat_file, "a+", encoding="utf-8") as file:
            file.write(user + ": \n\t" + message + "\n\n")
        

    def getAll(self):
        with open(self.chat_file, "r", encoding="utf-8") as file:
            return file.read()

    def deleteFile(self):       #Will need to work on this...
        if os.path.exists(os.path(self.chat_file)):
            os.remove(self.chat_file)
            print(f"{self.chat_file} has been deleted.")
        else:
            print("File does not exist.")
    
    def getHistoryFile(self):
        return self.chat_file

    def getLogFile(self):
        return self.chat_log