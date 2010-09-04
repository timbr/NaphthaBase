from Settings import *
import pyodbc
import os
import sqlite3

NaphthaBase = ''
stock_connection = ''


def MakeDatabaseConnection(RandR_db = RandR_Naphtha_Dbase):
    global NaphthaBase, stock_connection
    NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
    CheckTables() # check that all the necessary tables are present
    
    if os.path.exists(RandR_db):
        stock_connection = \
        pyodbc.connect(DRIVER='{Microsoft Access Driver (*.mdb)}', DBQ=RandR_db)
        print "Made connection with R&R database at %s" %RandR_db
    else:
        print "Unable to make connection with R&R database at %s" % RandR_db

def CheckTables():
    c = NaphthaBase.cursor()
    query = c.execute("select * from sqlite_master where type = 'table'")
    tables = [row[1] for row in query]
    print tables
    if len(tables) == 0:
        # empty database file
        c.execute("create table Material (Code text, Description text, LastUpdated date, RecordNo int)")
        NaphthaBase.commit()
    if 'Material_temp' in tables:
        c.execute("drop table Material_temp")
        NaphthaBase.commit()
        print 'Removed Material_temp table'
        
class materialcodes(object):
    def __init__(self):
        if NaphthaBase == '':
            # No connection has been made to the NaphthaBase
            MakeDatabaseConnection()
        if stock_connection == '':
            # No connection has been made to the R&R stock database
            self.localonly = True
        c = NaphthaBase.cursor()
        self.matdata = [row for row in c.execute("select * from Material")]
        self.createDB()
        
    def createDB(self):
        self.getlatest = {}
        for entry in self.matdata:
            if entry[0] in self.getlatest.keys():
                if entry[2] > self.getlatest[entry[0]][2]:
                    self.getlatest[entry[0]] = entry[1]
            else:
                self.getlatest[entry[0]] = entry[1]
                
        
    def updateNaphthaBase(self):
        RandRcursor = stock_connection.cursor()
        command = """
        SELECT
        Formula.Key AS Code,
        Formula.Description,
        Formula.\"Last Updated\" AS LastUpdated,
        Formula.\"Record Number\" AS RecordNo
        FROM Formula
        WHERE (Formula.\"Customer Key\"='ANY')
        ORDER BY Formula.Key
        """
        RandRdata = RandRcursor.execute(command)
        
        c = NaphthaBase.cursor()
        c.execute("create table Material_temp (Code text, Description text, LastUpdated date, RecordNo int)")
        for entry in RandRdata:
            c.execute('insert into Material_temp values (?,?,?,?)', entry)
        NaphthaBase.commit()
        
        diff = c.execute("SELECT Material_temp.* from Material_temp Left Join Material on (Material_temp.LastUpdated = Material.LastUpdated) where Material.LastUpdated IS Null")
        
        newrows =  [row for row in diff]
        
        for entry in newrows:
            print entry
            c.execute('insert into Material values (?,?,?,?)', entry)
        NaphthaBase.commit()
        self.matdata = [row for row in c.execute("select * from Material")]
        self.createDB()
        NaphthaBase.close()

            
            
        