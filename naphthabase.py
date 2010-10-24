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

from settings import *
import sql


NaphthaBaseChecked = 0
stock_connection = ''


def make_database_connection(RandR_db = RandR_Naphtha_Dbase, \
                             RandR_Acc_db = RandR_Accounts_Dbase):
    """Make a connection to the Official R&R database or any other db given"""
    
    global stock_connection, accounts_connection
    check_tables() # check that all the necessary tables are present
    
    if os.path.exists(RandR_db):
        stock_connection = \
           pyodbc.connect(DRIVER = '{Microsoft Access Driver (*.mdb)}',
                          DBQ = RandR_db)
        print "Made connection with R&R database at %s" % RandR_db
    else:
        print "Unable to make connection with R&R database at %s" % RandR_db
    
    if os.path.exists(RandR_Acc_db):
        accounts_connection = \
           pyodbc.connect(DRIVER='{Microsoft Access Driver (*.mdb)}',
                          DBQ = RandR_Acc_db, PWD = accountsDBpassword)
        print "Made connection with R&R Accounts database at %s" % RandR_Acc_db
    else:
        print "Unable to make connection with R&R Accounts database at %s" \
                                                                 % RandR_Acc_db

        
def check_tables():
    """Checks that the NaphthaBase has all the tables it needs and no more."""
    
    global NaphthaBaseChecked # TODO Find alternative to global variables
    # Dictionary of table names and the sql query strings needed to create them
    tablelist = {'Material': sql.create_material_table,
                 'Purchases': sql.create_purchases_table,
                 'Stock': sql.create_stock_table,
                 'Sales': sql.create_sales_table,
                 'DeletedSales': sql.create_deleted_sales_table,
                 'Hauliers': sql.create_hauliers_table,
                 'Customer': sql.create_customer_table}
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

def get_column_positions(table):
    """Creates a dictionary relating column names and their positions.
    
    So given the Materials table it would return:
    
        {'Code': 0, 'Description': 1, 'LastUpdated': 2, 'RecordNo': 3}
    """
    
    column_names = get_columns(table)
    column_dict = {}
    for index, value in enumerate(column_names):
        column_dict[value] = index
    return column_dict

    
def get_columns(table):
    """Creates an ordered list of column names for a given table.
    """
    
    column_data = naphthabase_query("pragma table_info(%s)" % table)
    column_names = [col[1] for col in column_data]
    return column_names


class NaphthaBaseObject(object):
    """Universal data object class that can be subclassed.
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
        self._data = \
          [row for row in naphthabase_query("select * from %s" % self._table)]
        # create a dictionary relating column postions against their names.
        # ie 'Code': 0, 'Description': 1, etc
        self._clmn = get_column_positions(self._table)
        self._create_db()
    
    def getdesc(self, code):
        self._update_naphtha_base()
        return self._getlatest.get(code.upper().upper(), [''])[0]
        # Return an empty string if no key found    
    
    def _create_db(self):
        """Creates a python dictionary of codes and descriptions.
        """

        self._getlatest = {}
        for entry in self._data:
            code = entry[self._clmn['Code']]
            lastupdate = entry[self._clmn['LastUpdated']]
            desc = entry[self._clmn['Description']]
            recordnum = entry[self._clmn['RecordNo']]
            if code in self._getlatest.keys():
                if lastupdate > code[self._clmn['LastUpdated']]:
                    self._getlatest[code] = [desc, recordnum, lastupdate]
                    # recordnum is added in position 1 so that lastupdate remains in position 2
            else:
                self._getlatest[code] = [desc, recordnum, lastupdate]

    def _update_naphtha_base(self):
        if self._localonly == 1:
            print 'Unable to update - remote database not found'
            return
        # Don't refresh again if last_refreshed is more recent than 30 minutes
        if self._last_refreshed > \
                   datetime.datetime.now() - datetime.timedelta(minutes = 30):
            return
        print 'Updating NaphthaBase with latest %s Data.' % self._table
        RandRcursor = stock_connection.cursor()   
        RandRdata = RandRcursor.execute(self._randr_query)
        naphthabase_query(self._cleardb)
        num_fields = len(get_columns(self._table))
        insert_fields = '(' + '?,' * (num_fields - 1) + '?)'
        # creates string "insert into <table> values (?,?,?,?, etc)"
        naphthabase_transfer(RandRdata, 'insert into %s values %s' \
                                         % (self._table, insert_fields))
        self._data = \
          [row for row in naphthabase_query("select * from %s" % self._table)]
        # create a dictionary relating column postions against their names.
        # ie 'Code': 0, 'Description': 1, etc
        self._clmn = get_column_positions(self._table)
        self._create_db()
        self._last_refreshed = datetime.datetime.now()

class MatCodes(NaphthaBaseObject):
    """Updates and provides access to Material Codes and their descriptions.
    
    If the R&R database can be connected to, the material codes are read,
    written to the NaphthaBase and stored in memory as a Python Dictionary.
    If the R&R database can't be found then only NaphthaBase data is used.
    """
    
    def __init__(self):
        self._table = 'Material'
        self._randr_query = sql.material_codes
        self._cleardb = sql.clear_material_table
        NaphthaBaseObject.__init__(self)
    
    def get_mat(self, mat_code):
        return NaphthaBaseObject.getdesc(self, mat_code)

    
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
        # create a dictionary relating column postions against their names.
        # ie 'Code': 0, 'Description': 1, etc
        self._clmn = get_column_positions('Material')
        self._create_db()
    
    def getdesc(self, matcode):
        self._update_naphtha_base()
        return self._getlatest.get(matcode.upper().upper(), [''])[0]
        # Return an empty string if no key found    
    
    def _create_db(self):
        """Creates a python dictionary of material codes and descriptions.
        """

        self._getlatest = {}
        for entry in self._matdata:
            code = entry[self._clmn['Code']]
            lastupdate = entry[self._clmn['LastUpdated']]
            desc = entry[self._clmn['Description']]
            recordnum = entry[self._clmn['RecordNo']]
            if code in self._getlatest.keys():
                if lastupdate > code[self._clmn['LastUpdated']]:
                    self._getlatest[code] = [desc, recordnum, lastupdate]
                    # recordnum is added in position 1 so that lastupdate remains in position 2
            else:
                self._getlatest[code] = [desc, recordnum, lastupdate]

    def _update_naphtha_base(self):
        if self._localonly == 1:
            print 'Unable to update - remote database not found'
            return
        # Don't refresh again if last_refreshed is more recent than 30 minutes
        if self._last_refreshed > \
                   datetime.datetime.now() - datetime.timedelta(minutes = 30):
            return
        print 'Updating NaphthaBase with latest Material Codes.'
        RandRcursor = stock_connection.cursor()   
        RandRdata = RandRcursor.execute(sql.material_codes)
        naphthabase_query(sql.clear_material_table)
        naphthabase_transfer(RandRdata, 'insert into Material values \
          (?,?,?,?)')
        self._matdata = \
          [row for row in naphthabase_query("select * from Material")]
        # create a dictionary relating column postions against their names.
        # ie 'Code': 0, 'Description': 1, etc
        self._clmn = get_column_positions('Material')
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
        # create a dictionary relating column postions against their names.
        # ie 'PO_Num': 0, 'Code': 1, etc
        self._clmn = get_column_positions('Purchases')
    
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
        # create a dictionary relating column postions against their names.
        # ie 'PO_Num': 0, 'Code': 1, etc
        self._clmn = get_column_positions('Purchases')
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
        # create a dictionary relating column postions against their names.
        # ie 'Batch': 0, 'Code': 1, etc
        self._clmn = get_column_positions('Stock')
    
    def get_batch(self, Batch_Num):
        self._update_naphtha_base()
        results = \
          naphthabase_query(sql.get_batch % {'batch_num': str(Batch_Num)})
        return [line for line in results]

    def getdict(self, Batch_Num):
        """Returns a list of dictionaries with stock data.
        
        Each stock entry is returned as a dictionary, with column names as
        the dictionary keys.
        """
        
        data = self.get_batch(Batch_Num)
        columns = get_columns('Stock')
        datalist = []
        for record in data:
            datadict = {}
            for index, field in enumerate(record):
                datadict[columns[index]] = field
            datalist.append(datadict)
        return datalist

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
        # create a dictionary relating column postions against their names.
        # ie 'Batch': 0, 'Code': 1, etc
        self._clmn = get_column_positions('Stock')
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
        self._deletedsalesdata = \
          [row for row in naphthabase_query("select * from DeletedSales")]
        # create a dictionary relating column postions against their names.
        # ie 'WO_Num': 0, 'Link': 1, etc
        self._clmn = get_column_positions('Sales')
    
    def get_wo(self, WO_Num):
        self._update_naphtha_base()
        results = \
          naphthabase_query(sql.sales_orders % {'wo_num': str(WO_Num)})
        if results == []:
            # if the WO number can't be found check the list of deleted orders
            results = naphthabase_query \
                          (sql.deleted_sales_orders % {'wo_num': str(WO_Num)})
        return [line for line in results]
    
    def getdict(self, WO_Num):
        """Returns a list of dictionaries with sales data.
        
        Each entry is returned as a dictionary, with column names as
        the dictionary keys.
        """
        
        data = self.get_wo(WO_Num)
        if len(data[0]) == 4:
            # Works Order number is on the Deleted list
            return data
        columns = get_columns('Sales')
        datalist = []
        for record in data:
            datadict = {}
            for index, field in enumerate(record):
                if field != '':
                    # don't include blank columns
                    datadict[columns[index]] = field
            datalist.append(datadict)
        return datalist

    def _update_naphtha_base(self):
        if self._localonly == 1:
            print 'Unable to update - remote database not found'
            return
         # Don't refresh again if last_refreshed is more recent than 30 minutes
        if self._last_refreshed > \
                   datetime.datetime.now() - datetime.timedelta(minutes = 30):
            return
        print 'Updating NaphthaBase with latest Sales and Despatch Information.'
        RandRcursor = stock_connection.cursor()
        RandRdata = RandRcursor.execute(sql.get_sales)
        naphthabase_query(sql.clear_sales_table)
        RandR_Stringed = stringprocess(RandRdata) # convert decimal types to strings
        naphthabase_transfer(RandR_Stringed, 'insert into Sales values \
                            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, \
                             ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
        self._salesdata = \
          [row for row in naphthabase_query("select * from Sales")]
        # create a dictionary relating column postions against their names.
        # ie 'WO_Num': 0, 'Link': 1, etc
        self._clmn = get_column_positions('Sales')
        
        RandRdata = RandRcursor.execute(sql.get_deleted_sales)
        naphthabase_query(sql.clear_deleted_sales_table)
        naphthabase_transfer(RandRdata, 'insert into DeletedSales values \
                            (?,?,?,?)')
        self._deletedsalesdata = \
          [row for row in naphthabase_query("select * from DeletedSales")]
        
        self._last_refreshed = datetime.datetime.now()

        
class Hauliers(object):
    """Updates and provides access to Haulier names.
    
    If the R&R database can be connected to, the haulier names are read,
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
        self._haulierdata = \
          [row for row in naphthabase_query("select * from Hauliers")]
        # create a dictionary relating column postions against their names.
        # ie 'HaulierKey': 0, 'Name': 1, etc
        self._clmn = get_column_positions('Hauliers')
        self._create_db()
    
    def getdesc(self, haulier_key):
        self._update_naphtha_base()
        return self._hauliers_dict.get(haulier_key.upper().upper(), [''])[0]
        # Return an empty string if no key found
    
    def _create_db(self):
        """Creates a python dictionary of haulier codes and descriptions.
        """

        self._hauliers_dict = {}
        for entry in self._haulierdata:
            haulier_key = entry[self._clmn['HaulierKey']]
            name = entry[self._clmn['Name']]
            nominal = entry[self._clmn['NominalCode']]
            self._hauliers_dict[haulier_key] = [name, nominal]

    def _update_naphtha_base(self):
        if self._localonly == 1:
            print 'Unable to update - remote database not found'
            return
        # Don't refresh again if last_refreshed is more recent than 30 minutes
        if self._last_refreshed > \
                   datetime.datetime.now() - datetime.timedelta(minutes = 30):
            return
        print 'Updating NaphthaBase with latest Hauliers.'
        RandRcursor = stock_connection.cursor()   
        RandRdata = RandRcursor.execute(sql.get_hauliers)
        naphthabase_query(sql.clear_hauliers_table)
        naphthabase_transfer(RandRdata, 'insert into Hauliers values \
          (?,?,?)')
        self._haulierdata = \
          [row for row in naphthabase_query("select * from Hauliers")]
        # create a dictionary relating column postions against their names.
        # ie 'HaulierKey': 0, 'Name': 1, etc
        self._clmn = get_column_positions('Hauliers')
        self._create_db()
        self._last_refreshed = datetime.datetime.now()

        
class Customer(object):
    """Updates and provides access to Customer details."""
    
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
        self._customerdata = \
          [row for row in naphthabase_query("select * from Customer")]
        # create a dictionary relating column postions against their names.
        # ie 'ID': 0, 'Name': 1, etc
        self._clmn = get_column_positions('Customer')
    
    def get_customer(self, CustomerID):
        self._update_naphtha_base()
        results = \
          naphthabase_query(sql.customer % {'customer_id': str(CustomerID)})
        return [line for line in results]

    def getdict(self, CustomerID):
        """Returns a list of dictionaries with customer data.
        
        Each entry is returned as a dictionary, with column names as
        the dictionary keys.
        """
        
        data = self.get_customer(CustomerID)
        columns = get_columns('Customer')
        datalist = []
        for record in data:
            datadict = {}
            for index, field in enumerate(record):
                datadict[columns[index]] = field
            datalist.append(datadict)
        return datalist

    def _update_naphtha_base(self):
        if self._localonly == 1:
            print 'Unable to update - remote database not found'
            return
         # Don't refresh again if last_refreshed is more recent than 30 minutes
        if self._last_refreshed > \
                   datetime.datetime.now() - datetime.timedelta(minutes = 30):
            return
        print 'Updating NaphthaBase with latest Customer Details.'
        RandRcursor = accounts_connection.cursor()
        RandRdata = RandRcursor.execute(sql.get_customer)
        naphthabase_query(sql.clear_customer_table)
        RandR_Stringed = stringprocess(RandRdata) # convert decimal types to strings
        naphthabase_transfer(RandR_Stringed, 'insert into Customer values \
                            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
        self._customerdata = \
          [row for row in naphthabase_query("select * from Customer")]
        # create a dictionary relating column postions against their names.
        # ie 'ID': 0, 'Name': 1, etc
        self._clmn = get_column_positions('Customer')
        self._last_refreshed = datetime.datetime.now()


if __name__ == '__main__':
    # Tests
    if os.getenv('COMPUTERNAME') == 'ACER5920':
        # Use dummy R&R database and run some tests
        print '\nACER5920\n========\n'
        if os.path.exists(NaphthaBase_Dbase):
            os.remove(NaphthaBase_Dbase) # delete existing NaphthaBase file
        make_database_connection(TestDB_Old, TestDB_Acc_Old)
    else:
        make_database_connection()
        
    matcode = MaterialCodes()
    po = Purchases()
    stock = Stock()
    so = Sales()
    haulier = Hauliers()
    customer = Customer()
       