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
import decimal

from Settings import *
import sql


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
    # Dictionary of table names and the sql query strings needed to create them
    tablelist = {'Material': sql.create_material_table,
                 'Purchases': sql.create_purchases_table,
                 'Stock': sql.create_stock_table,
                 'Sales': sql.create_sales_table}
    query = \
      naphthabase_query("select * from sqlite_master where type = 'table'")
    # What tables are in the NaphthaBase?
    dbtables = [row[1] for row in query]
    print dbtables
    # Excecute sql to create any missing tables
    for table in tablelist.keys():
        if table not in dbtables:
            naphthabase_query(tablelist[table])
    NaphthaBaseChecked = 1
    
    
def naphthabase_query(query, params = None):
    """Returns results of a given NaphthaBase Query.
    
    Opens NaphthaBase, runs sql query and closes NaphthaBase.
    """
    
    NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
    NaphthaBase.text_factory = str # solves problem with Pound signs....!
    c = NaphthaBase.cursor()
    if params == None:
        results = [row for row in c.execute(query)]
    else:
        results = [row for row in c.execute(query, params)]
    NaphthaBase.commit()
    NaphthaBase.close()
    return results
    
 
def naphthabase_transfer(data, query):
    """Loads data into NaphthaBase and closes database at the end.
    
    Faster than writing each line individually using naphthabase_query()
    as it keeps the NaphthaBase connection open until all lines have been
    written.
    """
    
    NaphthaBase = sqlite3.connect(NaphthaBase_Dbase)
    NaphthaBase.text_factory = str # solves problem with Pound signs....!
    c = NaphthaBase.cursor()
    for entry in data:
            results = [row for row in c.execute(query, entry)]
    NaphthaBase.commit()
    NaphthaBase.close()

    
def stringprocess(datastore):
    """Converts Decimal fields to strings in an sqlite datastore.
    
    Returns a tuple with all decimal values converted to strings.
    """
    
    output_list = []
    for line in datastore:
        output_line = []
        for field in line:
            if type(field) is decimal.Decimal:
                field = str(field)
            output_line.append(field)
        output_list.append(output_line)
    return tuple(output_list)
    
        
class MaterialCodes(object):
    """Updates and provides access to Material Codes and their descriptions.
    
    If the R&R database can be connected to, the material codes are read,
    written to the NaphthaBase and stored in memory as a Python Dictionary.
    If the R&R database can't be found then only NaphthaBase data is used.
    """
    
    def __init__(self):
        if NaphthaBaseChecked == 0:
            # No connection has been made to the NaphthaBase
            make_database_connection()
        if stock_connection == '':
            # No connection has been made to the R&R stock database
            self._localonly = 1
        else:
            self._localonly = 0
            # If connection has been made to the R&R stock database then
            # update the NaphthaBase with the latest codes.
            self._last_refreshed = \
                datetime.datetime.now() - datetime.timedelta(minutes=31)
                # pretend naphthabase hasn't been refreshed for 31 mins)
            self._update_naphtha_base()
        self._matdata = \
          [row for row in naphthabase_query("select * from Material")]
        self._create_db()
    
    def getdesc(self, matcode):
        self._update_naphtha_base()
        return self._getlatest.get(matcode.upper().upper(), [''])[0]
        # Return an empty string if no key found
    
    def _create_db(self):
        """Creates a python dictionary of material codes and descriptions.
        """
        # Constants to make list items clearer
        CODE = 0
        DESC = 1
        LASTUPDATE = 2
        RECORDNUM = 3
        self._getlatest = {}
        for entry in self._matdata:
            if entry[CODE] in self._getlatest.keys():
                if entry[LASTUPDATE] > self.getlatest[entry[CODE]][LASTUPDATE]:
                    self._getlatest[entry[CODE]] = [entry[DESC], \
                       entry[RECORDNUM], entry[LASTUPDATE]]
                    # RECORDNUM is added in position 1 so that LASTUPDATE remains in position 2
            else:
                self._getlatest[entry[CODE]] = [entry[DESC], entry[RECORDNUM],\
                   entry[LASTUPDATE]]

    def _update_naphtha_base(self):
        if self._localonly == 1:
            print 'Unable to update - remote database not found'
            return
        # Don't refresh again if last_refreshed is more recent than 30 minutes
        if self._last_refreshed > \
                   datetime.datetime.now() - datetime.timedelta(minutes = 30):
            return
        print 'Updating NatphthaBase with latest Material Codes.'
        RandRcursor = stock_connection.cursor()   
        RandRdata = RandRcursor.execute(sql.material_codes)
            
        naphthabase_query(sql.clear_material_table)

        naphthabase_transfer(RandRdata, 'insert into Material values \
          (?,?,?,?)')
        self._matdata = \
          [row for row in naphthabase_query("select * from Material")]
        self._create_db()
        self._last_refreshed = datetime.datetime.now()

        
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
            # If connection has been made to the R&R stock database then
            # update the NaphthaBase with the latest purchase orders.
            self._localonly = 0
            self._last_refreshed = \
                datetime.datetime.now() - datetime.timedelta(minutes=31)
                # pretend naphthabase hasn't been refreshed for 31 mins)
            self._update_naphtha_base()

        self._po_data = \
          [row for row in naphthabase_query("select * from Purchases")]
    
    def get_po(self, PO_Num):
        self._update_naphtha_base()
        results = \
          naphthabase_query(sql.purchase_orders % {'po_num': str(PO_Num)})
        return [line for line in results]
        
    def _update_naphtha_base(self):
        if self._localonly == 1:
            print 'Unable to update - remote database not found'
            return
        # Don't refresh again if last_refreshed is more recent than 30 minutes
        if self._last_refreshed > \
                   datetime.datetime.now() - datetime.timedelta(minutes = 30):
            return
        print 'Updating NaphthaBase with latest Purchase Orders.'
        RandRcursor = stock_connection.cursor()
        RandRdata = RandRcursor.execute(sql.po_data)

        naphthabase_query(sql.clear_po_table)
        
        RandR_Stringed = stringprocess(RandRdata) # convert decimal types to strings

        naphthabase_transfer(RandR_Stringed, 'insert into Purchases values \
                             (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')

        self._po_data = \
          [row for row in naphthabase_query("select * from Purchases")]
        self._last_refreshed = datetime.datetime.now()
        
        
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
            # If connection has been made to the R&R stock database then
            # update the NaphthaBase with the latest stock.
            self._localonly = 0
            self._last_refreshed = \
                datetime.datetime.now() - datetime.timedelta(minutes=31)
                # pretend naphthabase hasn't been refreshed for 31 mins)
            self._update_naphtha_base()
        self._stockdata = \
          [row for row in naphthabase_query("select * from Stock")]
    
    def get_batch(self, Batch_Num):
        self._update_naphtha_base()
        results = \
          naphthabase_query(sql.get_batch % {'batch_num': str(Batch_Num)})
        return [line for line in results]

    def _update_naphtha_base(self):
        if self._localonly == 1:
            print 'Unable to update - remote database not found'
            return
         # Don't refresh again if last_refreshed is more recent than 30 minutes
        if self._last_refreshed > \
                   datetime.datetime.now() - datetime.timedelta(minutes = 30):
            return
        print 'Updating NaphthaBase with latest Stock.'
        RandRcursor = stock_connection.cursor()
        RandRdata = RandRcursor.execute(sql.get_stock)
        
        naphthabase_query(sql.clear_stock_table)
        RandR_Stringed = stringprocess(RandRdata) # convert decimal types to strings
        naphthabase_transfer(RandR_Stringed, 'insert into Stock values \
                            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
        self._stockdata = \
          [row for row in naphthabase_query("select * from Stock")]
        self._last_refreshed = datetime.datetime.now()


class Sales(object):
    """Updates and provides access to Sales and Despatch information."""
    
    def __init__(self):
        if NaphthaBaseChecked == 0:
            # No connection has been made to the NaphthaBase
            MakeDatabaseConnection()
        if stock_connection == '':
            # No connection has been made to the R&R stock database
            self._localonly = 1
        else:
            # If connection has been made to the R&R stock database then
            # update the NaphthaBase with the latest sales and despatches.
            self._localonly = 0
            self._last_refreshed = \
                datetime.datetime.now() - datetime.timedelta(minutes=31)
                # pretend naphthabase hasn't been refreshed for 31 mins)
            self._update_naphtha_base()
        self._salesdata = \
          [row for row in naphthabase_query("select * from Sales")]
    
    def get_wo(self, WO_Num):
        self._update_naphtha_base()
        results = \
          naphthabase_query(sql.sales_orders % {'wo_num': str(WO_Num)})
        return [line for line in results]

    def _update_naphtha_base(self):
        if self._localonly == 1:
            print 'Unable to update - remote database not found'
            return
         # Don't refresh again if last_refreshed is more recent than 30 minutes
        if self._last_refreshed > \
                   datetime.datetime.now() - datetime.timedelta(minutes = 30):
            return
        print 'Updating NaphthaBase with latest Sales and Despatches.'
        RandRcursor = stock_connection.cursor()
        RandRdata = RandRcursor.execute(sql.get_sales)
        
        naphthabase_query(sql.clear_sales_table)
        RandR_Stringed = stringprocess(RandRdata) # convert decimal types to strings
        naphthabase_transfer(RandR_Stringed, 'insert into Sales values \
                            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, \
                             ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
        self._salesdata = \
          [row for row in naphthabase_query("select * from Sales")]
        self._last_refreshed = datetime.datetime.now()
        

if __name__ == '__main__':
    # Tests
    if os.path.exists(NaphthaBase_Dbase):
        os.remove(NaphthaBase_Dbase) # delete existing NaphthaBase file
    make_database_connection(TestDB_Old)
    MatCodeOld = MaterialCodes()
    #MatCodeOld.update_naphtha_base()
    original = MatCodeOld.getdesc('pa23')
    no_entry = MatCodeOld.getdesc('ppld26c')
    
    po = Purchases()
    po.update_naphtha_base()
    podata_original = po.get_po(7562)
    
    
    po = Purchases()
    po.update_naphtha_base()
    podata_revised = po.get_po(7562)
    
    print
    print original
    print no_entry
    print
    print podata_original
    print
    print podata_revised
    
    
    
    