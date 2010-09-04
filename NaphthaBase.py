from Settings import *
import pyodbc
import os
import sqlite3
import datetime

NaphthaBaseChecked = 0
stock_connection = ''


def MakeDatabaseConnection(RandR_db = RandR_Naphtha_Dbase):
    global stock_connection
    CheckTables() # check that all the necessary tables are present
    
    if os.path.exists(RandR_db):
        stock_connection = \
        pyodbc.connect(DRIVER='{Microsoft Access Driver (*.mdb)}', DBQ=RandR_db)
        print "Made connection with R&R database at %s" % RandR_db
    else:
        print "Unable to make connection with R&R database at %s" % RandR_db

def CheckTables():
    global NaphthaBaseChecked # TODO Find alternative to global variables
    NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
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
    NaphthaBase.close()
    NaphthaBaseChecked = 1
        
class materialcodes(object):
    def __init__(self):
        if NaphthaBaseChecked == 0:
            # No connection has been made to the NaphthaBase
            MakeDatabaseConnection()
        if stock_connection == '':
            # No connection has been made to the R&R stock database
            self.localonly = 1
        else:
            self.localonly = 0
        NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
        c = NaphthaBase.cursor()
        self.matdata = [row for row in c.execute("select * from Material")]
        self.createDB()
    
    def getdesc(self, matcode):
        return self.getlatest.get(matcode.upper().upper(), [''])[0]
        # Return an empty string if no key found
    
    def createDB(self):
        # Constants to make list items clearer
        CODE = 0
        DESC = 1
        LASTUPDATE = 2
        RECORDNUM = 3
        self.getlatest = {}
        for entry in self.matdata:
            if entry[CODE] in self.getlatest.keys():
                if entry[LASTUPDATE] > self.getlatest[entry[CODE]][LASTUPDATE]:
                    self.getlatest[entry[CODE]] = [entry[DESC], entry[RECORDNUM], entry[LASTUPDATE]]
                    # RECORDNUM is added in position 1 so that LASTUPDATE remains in position 2
            else:
                self.getlatest[entry[CODE]] = [entry[DESC], entry[RECORDNUM], entry[LASTUPDATE]]
        
    def updateNaphthaBase(self):
        if self.localonly == 1:
            print 'Unable to update - remote database not found'
            return
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
        
        NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
        c = NaphthaBase.cursor()
        c.execute("create table Material_temp (Code text, Description text, LastUpdated date, RecordNo int)")
        for entry in RandRdata:
            c.execute('insert into Material_temp values (?,?,?,?)', entry)
        NaphthaBase.commit()
        
        diffquery = """
        SELECT Material_temp.*
        from Material_temp
        Left Join Material on (Material_temp.LastUpdated = Material.LastUpdated)
        where Material.LastUpdated IS Null
        """  
        diff = c.execute(diffquery)
        
        newrows =  [row for row in diff]
        
        for entry in newrows:
            c.execute('insert into Material values (?,?,?,?)', entry)
        NaphthaBase.commit()
        self.matdata = [row for row in c.execute("select * from Material")]
        self.createDB()
        NaphthaBase.close()

if __name__ == '__main__':
    # Tests
    if os.path.exists(NaphthaBase_Dbase):
        os.remove(NaphthaBase_Dbase) # delete existing NaphthaBase file
    MakeDatabaseConnection(TestDB_Old)
    MatCodeOld = materialcodes()
    MatCodeOld.updateNaphthaBase()
    original = MatCodeOld.getdesc('pa23')
    no_entry = MatCodeOld.getdesc('ppld26c')
    
    MakeDatabaseConnection(TestDB_New)
    MatCodeNew = materialcodes()
    MatCodeNew.updateNaphthaBase()
    revised = MatCodeNew.getdesc('PA23')
    an_entry = MatCodeNew.getdesc('PPLD26C')
    
    print
    print original, revised
    print no_entry, an_entry