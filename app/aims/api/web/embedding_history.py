from datetime import date, datetime
import os
from dotenv import load_dotenv

load_dotenv()

class Embedding_History():

    def __init__(self, file_history, file_log): #Things that get loaded on booting up
        self.history = file_history
        self.log = file_log
        # print("\n\n new embedding history\n")
        # temp_file = os.getenv("TEMP_FOLDER")
        # file_path = temp_file+"/_log/"
        # current_date_time_stamp = datetime.now().strftime("%Y-%m-%d__%H;%M;%S")
        # self.embedding_file = file_path + "Embedding_Histoy" + current_date_time_stamp +".txt"
        # print("File >>>>>> " + self.embedding_file+"\n\n")
        # with open(self.embedding_file, "w") as file:
        #     file.write("Beginning of new Embedding History\n\n")

        

    def add(self, success, file_name):
        timestamp = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

        with open(self.history, "a+", encoding="utf-8") as file:
            file.write(success + ": \n\t" + file_name + "\n")
            
        with open(self.log, "a+", encoding="utf-8") as file:
            file.write("["+timestamp+"] >>> " + success + ": \n\t" + file_name + "\n\n")