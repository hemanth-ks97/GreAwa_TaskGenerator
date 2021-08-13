import os
from DatabaseHandler import DatabaseHandler

#Creating database handler class
dbh = DatabaseHandler()

#Check if the database file exists and create the database
if (os.path.isfile(dbh.DBPath) == False):
    dbh.RetrieveData(0)
    dbh.RetrieveData(1) 

operation = input("Enter 1 to start the essay session: ")
if(operation == "1"):
    issueTask = dbh.PullRandom(0)
    argumentTask = dbh.PullRandom(1)
    print("###########################################################")
    print(issueTask)
    print("###########################################################")
    print(argumentTask)

dbh.CloseDb()