""" naphthabase.py  -- Interface to the NaphthaBase Database.

Provides routines for taking a snapshot of the official R & R Associates 
database and saving the data in the NaphthaBase Database. All changes since
the last snapshot are added without deleting the older data.

Routines for quick and easy access to data in the NaphthaBase are also
provided.
"""

import pyodbc
import os
import sqlite3
import datetime

from Settings import *


NaphthaBaseChecked = 0
stock_connection = ''


def make_database_connection(RandR_db = RandR_Naphtha_Dbase):
    """Make a connection to the Official R&R database or any other db given"""
    
    global stock_connection
    check_tables() # check that all the necessary tables are present
    
    if os.path.exists(RandR_db):
        stock_connection = \
           pyodbc.connect(DRIVER='{Microsoft Access Driver (*.mdb)}',
                       DBQ=RandR_db)
        print "Made connection with R&R database at %s" % RandR_db
    else:
        print "Unable to make connection with R&R database at %s" % RandR_db

        
def check_tables():
    """Checks that the NaphthaBase has all the tables it needs and no more."""
    
    global NaphthaBaseChecked # TODO Find alternative to global variables
    NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
    c = NaphthaBase.cursor()
    query = c.execute("select * from sqlite_master where type = 'table'")
    tables = [row[1] for row in query]
    print tables
    if len(tables) == 0:
        # empty database file
        c.execute("create table Material (Code text, Description text, \
                  LastUpdated date, RecordNo int)")
        c.execute("create table Purchases (PO_Num text, Code text, \
                  Batch text, Quantity text, Price text, OrderValue text, \
                  Supplier text, OrderReference text, OrderDate date, \
                  DueDate date, PlacedBy text, DeliveredQuantity text, \
                  PrintedComment text, DeliveryComment text, Status int, \
                  LastUpdated date)")
        c.execute("create table Stock (Batch text, Code text, Revision text, \
                  BatchStatus text, QuantityNow text, \
                  OriginalDeliveredQuantity text, StockInfo text, \
                  Supplier text, PONumber text, PurchaseCost text, \
                  Customer text, WONumber text, Price text, \
                  UsageReference text, StockAction text, ItemOrder text, \
                  QuantityMovement text, UserID text, LastUpdated date, \
                  InvoiceDate date, BatchUp_Date date)")
        NaphthaBase.commit()
    if 'Material_temp' in tables:
        c.execute("drop table Material_temp")
        NaphthaBase.commit()
        print 'Removed Material_temp table'
    if 'Purchases_temp' in tables:
        c.execute("drop table Purchases_temp")
        NaphthaBase.commit()
        print 'Removed Purchases_temp table'
    if 'Stock_temp' in tables:
        c.execute("drop table Stock_temp")
        NaphthaBase.commit()
        print 'Removed Stock_temp table'
    NaphthaBase.close()
    NaphthaBaseChecked = 1
        
        
class MaterialCodes(object):
    """Updates and provides access to Material Codes and their descriptions"""
    
    def __init__(self):
        if NaphthaBaseChecked == 0:
            # No connection has been made to the NaphthaBase
            MakeDatabaseConnection()
        if stock_connection == '':
            # No connection has been made to the R&R stock database
            self._localonly = 1
        else:
            self._localonly = 0
        NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
        c = NaphthaBase.cursor()
        self._matdata = [row for row in c.execute("select * from Material")]
        self._create_db()
    
    def getdesc(self, matcode):
        return self.getlatest.get(matcode.upper().upper(), [''])[0]
        # Return an empty string if no key found
    
    def _create_db(self):
        # Constants to make list items clearer
        CODE = 0
        DESC = 1
        LASTUPDATE = 2
        RECORDNUM = 3
        self.getlatest = {}
        for entry in self._matdata:
            if entry[CODE] in self.getlatest.keys():
                if entry[LASTUPDATE] > self.getlatest[entry[CODE]][LASTUPDATE]:
                    self.getlatest[entry[CODE]] = [entry[DESC], \
                       entry[RECORDNUM], entry[LASTUPDATE]]
                    # RECORDNUM is added in position 1 so that LASTUPDATE remains in position 2
            else:
                self.getlatest[entry[CODE]] = [entry[DESC], entry[RECORDNUM],\
                   entry[LASTUPDATE]]
        
    def update_naphtha_base(self):
        if self._localonly == 1:
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
        
        query = c.execute("select * from sqlite_master where type = 'table'")
        tables = [row[1] for row in query]
        if 'Material_temp' in tables:
            c.execute("drop table Material_temp")
            NaphthaBase.commit()
        
        c.execute("create table Material_temp (Code text, Description text, \
                  LastUpdated date, RecordNo int)")
        for entry in RandRdata:
            c.execute('insert into Material_temp values (?,?,?,?)', entry)
        NaphthaBase.commit()
        
        diffquery = """
        SELECT Material_temp.*
        from Material_temp
        Left Join Material on
        (Material_temp.LastUpdated = Material.LastUpdated)
        where Material.LastUpdated IS Null
        """
        
        diff = c.execute(diffquery)
        newrows =  [row for row in diff]
        for entry in newrows:
            c.execute('insert into Material values (?,?,?,?)', entry)
        NaphthaBase.commit()
        self._matdata = [row for row in c.execute("select * from Material")]
        self._create_db()
        NaphthaBase.close()

        
class Purchases(object):
    """Updates and provides access to Purchase Order information."""
    
    def __init__(self):
        if NaphthaBaseChecked == 0:
            # No connection has been made to the NaphthaBase
            MakeDatabaseConnection()
        if stock_connection == '':
            # No connection has been made to the R&R stock database
            self._localonly = 1
        else:
            self._localonly = 0
        NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
        NaphthaBase.text_factory = str # solves problem with Pound signs....!
        c = NaphthaBase.cursor()
        self._POdata = [row for row in c.execute("select * from Purchases")]
        #self._create_db()
    
    def get_po(self, PO_Num):
        NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
        NaphthaBase.text_factory = str # solves problem with Pound signs....!
        c = NaphthaBase.cursor()
        command = """
        SELECT PO_Num, Code, Batch, Quantity, Price, OrderValue, Supplier,
        OrderReference, OrderDate, DueDate, PlacedBy, DeliveredQuantity,
        PrintedComment, DeliveryComment, Status, LastUpdated
        FROM Purchases,
        (SELECT MAX(LastUpdated) AS latest from Purchases WHERE
        PO_Num = %(po_num)s)
        WHERE PO_Num = %(po_num)s and LastUpdated = latest
        ORDER BY Code
        """ % {'po_num': str(PO_Num)}
        results = c.execute(command)
        return [line for line in results]
    
    def _create_db(self):
        PO_conn = sqlite3.connect(':memory:')
        PO_c = PO_conn.cursor()
        PO_c.execute("create table Purchases (PO_Num text, Code text, \
                     Batch text, Quantity text, Price text, OrderValue text, \
                     Supplier text, OrderReference text, OrderDate date, \
                     DueDate date, PlacedBy text, DeliveredQuantity text, \
                     PrintedComment text, DeliveryComment text, Status int, \
                     LastUpdated date)")
        PO_c.commit()
        
        NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
        NaphthaBase.text_factory = str # solves problem with Pound signs....!
        PO_c_disk = NaphthaBase.cursor()

        
        # Constants to make list items clearer
        CODE = 0
        DESC = 1
        LASTUPDATE = 2
        RECORDNUM = 3
        self.getlatest = {}
        for entry in self.POdata:
            if entry[CODE] in self.getlatest.keys():
                if entry[LASTUPDATE] > self.getlatest[entry[CODE]][LASTUPDATE]:
                    self.getlatest[entry[CODE]] = [entry[DESC], \
                       entry[RECORDNUM], entry[LASTUPDATE]]
                    # RECORDNUM is added in position 1 so that LASTUPDATE remains in position 2
            else:
                self.getlatest[entry[CODE]] = [entry[DESC], entry[RECORDNUM],\
                   entry[LASTUPDATE]]
        
    def update_naphtha_base(self):
        if self._localonly == 1:
            print 'Unable to update - remote database not found'
            return
        RandRcursor = stock_connection.cursor()
        command = """
        SELECT
        \"Purchase Order\".\"Order Number\" AS PO_Num,
        \"Purchase Item\".\"Component Code\" AS Code,
        \"Formula Stock\".Batch,
        \"Purchase Item\".Quantity,
        \"Purchase Item\".Price,
        \"Purchase Order\".\"Order Value\" AS OrderValue,
        \"Purchase Order\".Supplier,
        \"Purchase Order\".\"Order Reference\" AS OrderReference,
        \"Purchase Order\".\"Order Date\" AS OrderDate,
        \"Purchase Item\".\"Due Date\" AS DueDate,
        \"Purchase Order\".\"Placed By\" AS PlacedBy,
        \"Purchase Item\".\"Delivered Quantity\" AS DeliveredQuantity,
        \"Purchase Order\".\"Printed Comment\" AS PrintedComment,
        \"Purchase Order\".\"Delivery Comment\" As DeliveryComment,
        \"Purchase Order\".Status,
        \"Purchase Item\".\"Last Updated\" AS LastUpdated       
        FROM (\"Purchase Order\" INNER JOIN \"Purchase Item\" ON
        \"Purchase Order\".\"Order Number\" = 
        \"Purchase Item\".\"Order Number\") LEFT JOIN \"Formula Stock\" ON
        (\"Purchase Item\".\"Component Code\" = \"Formula Stock\".Key) AND 
        (\"Purchase Item\".\"Order Number\" = \"Formula Stock\".PON)       
        ORDER BY \"Purchase Order\".\"Order Number\"
        """
        RandRdata = RandRcursor.execute(command)
        
        NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
        NaphthaBase.text_factory = str # solves problem with Pound signs....!
        c = NaphthaBase.cursor()
        
        query = c.execute("select * from sqlite_master where type = 'table'")
        tables = [row[1] for row in query]
        if 'Purchases_temp' in tables:
            c.execute("drop table Purchases_temp")
            NaphthaBase.commit()
        
        c.execute("create table Purchases_temp (PO_Num text, Code text, \
                  Batch text, Quantity text, Price text, OrderValue text, \
                  Supplier text, OrderReference text, OrderDate date, \
                  DueDate date, PlacedBy text, DeliveredQuantity text, \
                  PrintedComment text, DeliveryComment text, Status int, \
                  LastUpdated date)")
        for entry in RandRdata:
            entry_temp = [thing for thing in entry] #prices and quantities are
            entry_temp[3] = str(entry_temp[3]) #stored as a decimal type in the
            entry_temp[4] = str(entry_temp[4]) #RandR database. Convert them to text
            entry_temp[5] = str(entry_temp[5]) #fields for storing in the NaphthaBase
            entry_temp[11] = str(entry_temp[11])
            c.execute('insert into Purchases_temp values (?,?,?,?,?,?,?,?,?, \
                      ?,?,?,?,?,?,?)', entry_temp)
        NaphthaBase.commit()
        
        diffquery = """
        SELECT Purchases_temp.*
        from Purchases_temp
        Left Join Purchases on (Purchases_temp.LastUpdated =
        Purchases.LastUpdated)
        where Purchases.LastUpdated IS Null
        """
        
        diff = c.execute(diffquery)
        newrows =  [row for row in diff]
        for entry in newrows: 
            c.execute('insert into Purchases values (?,?,?,?,?,?,?,?,?,?,?, \
                      ?,?,?,?,?)', entry)
        NaphthaBase.commit()
        
        self.POdata = [row for row in c.execute("select * from Purchases")]
        #self._create_db()
        NaphthaBase.close()
        
        
class Stock(object):
    """Updates and provides access to Stock information."""
    
    def __init__(self):
        if NaphthaBaseChecked == 0:
            # No connection has been made to the NaphthaBase
            MakeDatabaseConnection()
        if stock_connection == '':
            # No connection has been made to the R&R stock database
            self._localonly = 1
        else:
            self._localonly = 0
        NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
        NaphthaBase.text_factory = str # solves problem with Pound signs....!
        c = NaphthaBase.cursor()
        self._Stockdata = [row for row in c.execute("select * from Stock")]
        #self._create_db()
    
    def get_batch(self, Batch_Num):
        NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
        NaphthaBase.text_factory = str # solves problem with Pound signs....!
        c = NaphthaBase.cursor()
        command = """
        SELECT Batch, Code, Revision, BatchStatus, QuantityNow, \
        OriginalDeliveredQuantity, StockInfo, Supplier, PONumber, \
        PurchaseCost, Customer, WONumber, Price, UsageReference, \
        StockAction, ItemOrder, QuantityMovement, UserID, LastUpdated, \
        InvoiceDate, BatchUp_Date
        FROM Stock,
        (SELECT MAX(LastUpdated) AS latest from Stock WHERE
        Batch = %(batch_num)s)
        WHERE Batch = %(batch_num)s and LastUpdated = latest
        """ % {'batch_num': str(Batch_Num)}
        results = c.execute(command)
        return [line for line in results]
    
    def _create_db(self):
        Stock_conn = sqlite3.connect(':memory:')
        Stock_c = PO_conn.cursor()
        Stock_c.execute("create table Purchases (PO_Num text, Code text, \
                     Batch text, Quantity text, Price text, OrderValue text, \
                     Supplier text, OrderReference text, OrderDate date, \
                     DueDate date, PlacedBy text, DeliveredQuantity text, \
                     PrintedComment text, DeliveryComment text, Status int, \
                     LastUpdated date)")
        Stock_c.commit()
        
        NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
        NaphthaBase.text_factory = str # solves problem with Pound signs....!
        Stock_c_disk = NaphthaBase.cursor()

        
        # Constants to make list items clearer
        CODE = 0
        DESC = 1
        LASTUPDATE = 2
        RECORDNUM = 3
        self.getlatest = {}
        for entry in self.POdata:
            if entry[CODE] in self.getlatest.keys():
                if entry[LASTUPDATE] > self.getlatest[entry[CODE]][LASTUPDATE]:
                    self.getlatest[entry[CODE]] = [entry[DESC], \
                       entry[RECORDNUM], entry[LASTUPDATE]]
                    # RECORDNUM is added in position 1 so that LASTUPDATE remains in position 2
            else:
                self.getlatest[entry[CODE]] = [entry[DESC], entry[RECORDNUM],\
                   entry[LASTUPDATE]]
        
    def update_naphtha_base(self):
        if self._localonly == 1:
            print 'Unable to update - remote database not found'
            return
        RandRcursor = stock_connection.cursor()
        command = """
        SELECT \"Formula Stock\".Batch,
        \"Formula Stock Usage\".Formula AS Code,
        \"Formula Stock Usage\".Revision,
        \"Formula Stock\".Type AS BatchStatus,
        \"Formula Stock\".Quantity AS QuantityNow,
        \"Formula Stock\".\"Original Quantity\" AS OriginalDeliveredQuantity,
        \"Formula Stock\".Location AS StockInfo,
        \"Formula Stock\".Supplier,
        \"Formula Stock\".PON AS PONumber,
        \"Formula Stock\".Cost AS PurchaseCost,
        \"Formula Stock Usage\".Customer,
        \"Formula Stock Usage\".\"Works order Number\" AS WONumber,
        \"Formula Stock Usage\".Price,
        \"Formula Stock Usage\".\"Usage Reference\" AS UsageReference,
        \"Formula Stock Usage\".\"Record Type\" AS StockAction,
        \"Formula Stock Usage\".\"Item Order\" AS ItemOrder,
        \"Formula Stock Usage\".Quantity AS QuantityMovement,
        \"Formula Stock Usage\".\"User ID\" AS UserID,
        \"Formula Stock Usage\".\"Last Updated\" AS LastUpdated,
        \"Formula Stock\".\"Last Updated\" AS InvoiceDate,
        \"Formula Stock\".\"Production Date\" AS BatchUp_Date
        FROM \"Formula Stock\", \"Formula Stock Usage\"
        WHERE \"Formula Stock\".Batch = \"Formula Stock Usage\".Batch
        ORDER BY \"Formula Stock\".Batch,
        \"Formula Stock Usage\".\"Last Updated\"
        """
        RandRdata = RandRcursor.execute(command)
        
        NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
        NaphthaBase.text_factory = str # solves problem with Pound signs....!
        c = NaphthaBase.cursor()
        
        query = c.execute("select * from sqlite_master where type = 'table'")
        tables = [row[1] for row in query]
        if 'Stock_temp' in tables:
            c.execute("drop table Stock_temp")
            NaphthaBase.commit()
        
        c.execute("create table Stock_temp (Batch text, Code text, \
                  Revision text, BatchStatus text, QuantityNow text, \
                  OriginalDeliveredQuantity text, StockInfo text, \
                  Supplier text, PONumber text, PurchaseCost text, \
                  Customer text, WONumber text, Price text, \
                  UsageReference text, StockAction text, ItemOrder text, \
                  QuantityMovement text, UserID text, LastUpdated date, \
                  InvoiceDate date, BatchUp_Date date)")

        for entry in RandRdata:
            entry_temp = [thing for thing in entry] #prices and quantities are
            entry_temp[9] = str(entry_temp[9]) #stored as a decimal type in the
            entry_temp[12] = str(entry_temp[12]) #RandR database. Convert them to text
            #fields for storing in the NaphthaBase
            c.execute('insert into Stock_temp values (?,?,?,?,?,?,?,?,?, \
                      ?,?,?,?,?,?,?,?,?,?,?,?)', entry_temp)
        NaphthaBase.commit()
        
        diffquery = """
        SELECT Stock_temp.*
        from Stock_temp
        Left Join Stock on (Stock_temp.LastUpdated =
        Stock.LastUpdated)
        where Stock.LastUpdated IS Null
        """
        
        diff = c.execute(diffquery)
        newrows =  [row for row in diff]
        for entry in newrows: 
            c.execute('insert into Stock values (?,?,?,?,?,?,?,?,?,?,?, \
                      ?,?,?,?,?,?,?,?,?,?)', entry)
        NaphthaBase.commit()
        
        self.Stockdata = [row for row in c.execute("select * from Stock")]
        #self._create_db()
        NaphthaBase.close()
        

if __name__ == '__main__':
    # Tests
    if os.path.exists(NaphthaBase_Dbase):
        os.remove(NaphthaBase_Dbase) # delete existing NaphthaBase file
    make_database_connection(TestDB_Old)
    MatCodeOld = MaterialCodes()
    MatCodeOld.update_naphtha_base()
    original = MatCodeOld.getdesc('pa23')
    no_entry = MatCodeOld.getdesc('ppld26c')
    
    po = Purchases()
    po.update_naphtha_base()
    podata_original = po.get_po(7562)
    
    make_database_connection(TestDB_New)
    MatCodeNew = MaterialCodes()
    MatCodeNew.update_naphtha_base()
    revised = MatCodeNew.getdesc('PA23')
    an_entry = MatCodeNew.getdesc('PPLD26C')
    
    po = Purchases()
    po.update_naphtha_base()
    podata_revised = po.get_po(7562)
    
    print
    print original, revised
    print no_entry, an_entry
    print
    print podata_original
    print
    print podata_revised
    
    
    
    