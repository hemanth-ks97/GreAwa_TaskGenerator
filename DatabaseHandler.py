import requests
from bs4 import BeautifulSoup
import sqlite3

class DatabaseHandler:

    def __init__(self):
        self.IssuePool = 'https://www.ets.org/gre/revised_general/prepare/analytical_writing/issue/pool'
        self.ArgumentPool = 'https://www.ets.org/gre/revised_general/prepare/analytical_writing/argument/pool'
        self.DBPath = 'database.db'
        self.connection = self.CreateDB(self.DBPath)

    # retrieve data ---------------------
    def RetrieveData(self,type):
        if type == 0:
            source = requests.get(self.IssuePool).text
        else:
            source = requests.get(self.ArgumentPool).text
        soup = BeautifulSoup(source, 'lxml')
        div = soup.find('div', class_='contents left')
        paras = div.find_all('p')
        self.CleanandPopulate(paras, type)
    # -----------------------------------

    # Clean and Populate DB -------------
    def CleanandPopulate(self, paras, type):
        paras.pop(0)
        paras.pop(0)
        questionFrame = ""
        for obj in paras:
            frame = str(obj.text)
            frame.replace("<p>", "")
            frame.replace("</p>", "")
            if frame.find("Write a response in which you") != -1:
                questionFrame += "\n" + frame
                #store it in database
                if type == 0:
                    self.connection.execute("insert into issues (text) values(?)",(questionFrame,))
                else:
                    self.connection.execute("insert into arguments (text) values(?)",(questionFrame,))
                #questionDb.append(questionFrame)   # SHOULD BE CHANGED TO DATABASE.EXECUTE()
                #reset the questionFrame variable
                questionFrame = ""
            else:
                if len(questionFrame) == 0:
                    questionFrame = frame
                else:
                    questionFrame += "\n" + frame
        self.connection.commit()
    # -----------------------------------

    def PullRandom(self,type):
        cursor = self.connection.cursor()
        if type == 0:
            cursor.execute("SELECT * FROM issues ORDER BY RANDOM() LIMIT 1")
            return cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM arguments ORDER BY RANDOM() LIMIT 1")
            return cursor.fetchall()            

    # Create DB and tables---------------
    def CreateDB(self, path):
        connection = None
        
        try:
            connection = sqlite3.connect(path)
            print("Connection successful")
        except self.Error as e:
            print(f"The error '{e}' has occurred")
        
        create_issue_table = '''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        );
        '''

        create_argument_table = '''
        CREATE TABLE IF NOT EXISTS arguments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        );
        '''

        connection.execute(create_issue_table)
        connection.execute(create_argument_table)

        return connection
    # ------------------------------------

    def CloseDb(self):
        self.connection.close()
    