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
                 'DeletedSales': sql.create_deletedsales_table,
                 'Hauliers': sql.create_hauliers_table,
                 'Customer': sql.create_customer_table,
                 'Depot': sql.create_depot_table,
                 'Contact': sql.create_contact_table,
                 'Supplier': sql.create_supplier_table}
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


def get_randR_data(query, table = '', last_updated = '',
                      convert_decimal_to_strings = True):
    """Run an SQL query on the RandR database.
    
    The correct database file is selected according to which table is being
    queried. Any Decimal type fields are converted to strings by default to
    avoid errors converting to floats.
    """
    
    if last_updated == '':
        last_updated = datetime.datetime(1982,1,1,0,0)
    # Connect to the correct R&R database file.
    # stock_tables and accounts_tables lists are in settings.py
    if table in stock_tables:
        RandRcursor = stock_connection.cursor()
    elif table in accounts_tables:
        RandRcursor = accounts_connection.cursor()
    else:
        print "no table specified, I'll try both"
        RandRcursor = stock_connection.cursor()
    
    try:
        RandRdata = RandRcursor.execute(query, {'lastupdate': last_updated})
    except:
        if table == '':
            RandRcursor = accounts_connection.cursor()
            RandRdata = RandRcursor.execute(query, {'lastupdate': last_updated})

    RandR_Stringed = stringprocess(RandRdata) # convert decimal types to strings
    return RandR_Stringed
    
    
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


#////////////////////////////////////////////////////////////////////////////#
class NaphthaBaseObject(object):
    """Universal data object class that can be subclassed.
    """
#////////////////////////////////////////////////////////////////////////////#
    
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
        self._data = self._getdata() # Get a list containing all the data
        # create a dictionary relating column postions against their names.
        # ie 'Code': 0, 'Description': 1, etc
        self._clmn = get_column_positions(self._table)
        
    def _getdata(self, table = ''):
        """Get all the data and store it as a list in self._data
        """
        
        if table == '':
            # If the table isn't specified, use the default table
            table = self._table
        data = [row for row in naphthabase_query
                              ("select * from %s where priority = 1" % table)]
        return data
    
    def _getfromdict(self, code):
        self._update_naphtha_base()
        return self._datadict.get(code.upper().upper(), [''])[0]
        # Return an empty string if no key found    
        
    def _sqlquery(self, query, revis = 1, sql = ''):
        """Returns a list of tuples containing results of sql query
        """
        
        if sql == '':
            # If the sql to use isn't specified then use the default sql
            sql = self._nbquery
        self._update_naphtha_base()
        results = \
          naphthabase_query(sql % {'query': str(query), 'priority': revis})
        return [line for line in results]

    def _return_as_dict(self, data, revis = 1, no_blank_columns = True):
        """Returns a list of dictionaries for the given list of tuples.
        
        The dictionary keys are the column names. Only columns that contain
        data are returned unless otherwise requested.
        """
        
        columns = get_columns(self._table)
        datalist = []
        for record in data:
            datadict = {}
            for index, field in enumerate(record):
                if field != '' or no_blank_columns is False:
                    # don't include blank columns unless told to
                    datadict[columns[index]] = field
            datalist.append(datadict)
        return datalist
    
    def _sqlquery_as_dict(self, query, revis = 1, no_blank_columns = True):
        """Returns a list of dictionaries containing results of sql query.
        
        The dictionary keys are the column names. Only columns that contain
        data are returned unless otherwise requested.
        """
        
        data = self._sqlquery(query)
        return self._return_as_dict(data, no_blank_columns)

    def _update_naphtha_base(self):
        if self._localonly == 1:
            print 'Unable to update - remote database not found'
            return
        # Don't refresh again if last_refreshed is more recent than 30 minutes
        if self._last_refreshed > \
                   datetime.datetime.now() - datetime.timedelta(minutes = 30):
            return
        table_size = naphthabase_query("SELECT COUNT(*) FROM %s" %self._table)
        if table_size[0][0] == 0:
            # It's an empty table so fill it, all records priority 1
            print 'Populating NaphthaBase with %s Data.' % self._table
            RandRdata = get_randR_data(self._randr_query, self._table)
            # Assign priority 1 to each record:
            tim = ()
            for record in RandRdata:
                record.append(1)
                tim = tuple(tim + (record,))
            RandRdata = tim
        else:
            last_updated = naphthabase_query \
                             ("SELECT MAX(LastUpdated) from %s" % self._table)
            new_records = get_randr_data \
                                (self._randr_query, self._table, last_updated)
            print [row for row in new_records]
        #naphthabase_query("DELETE FROM %s" % self._table) # Clear table
        num_fields = len(get_columns(self._table))
        insert_fields = '(' + '?,' * (num_fields - 1) + '?)'
        # creates string "insert into <table> values (?,?,?,?, etc)"
        naphthabase_transfer(RandRdata, 'insert into %s values %s' \
                                       % (self._table, insert_fields))
        self._data = self._getdata() # Get a list containing all the data
        # create a dictionary relating column postions against their names.
        # ie 'Code': 0, 'Description': 1, etc
        self._clmn = get_column_positions(self._table)
        self._last_refreshed = datetime.datetime.now()


#////////////////////////////////////////////////////////////////////////////#
class MaterialCodes(NaphthaBaseObject):
    """Updates and provides access to Material Codes and their descriptions.
    
    If the R&R database can be connected to, the material codes are read,
    written to the NaphthaBase and stored in memory as a Python Dictionary.
    If the R&R database can't be found then only NaphthaBase data is used.
    """
#////////////////////////////////////////////////////////////////////////////#
    
    def __init__(self):
        self._table = 'Material'
        self._randr_query = sql.material_codes
        NaphthaBaseObject.__init__(self)
        self._create_db()
    
    def get_mat(self, mat_code):
        # This method is probably not needed
        return NaphthaBaseObject._getfromdict(self, mat_code)
    
    def _create_db(self):
        """Creates a python dictionary of Material codes and descriptions.
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
        self._datadict = self._getlatest
    
    def _update_naphtha_base(self):
        NaphthaBaseObject._update_naphtha_base(self)
        self._create_db()


#////////////////////////////////////////////////////////////////////////////#
class Purchases(NaphthaBaseObject):
    """Updates and provides access to Purchase Order information."""
#////////////////////////////////////////////////////////////////////////////#

    def __init__(self):
        self._table = 'Purchases'
        self._randr_query = sql.po_data
        self._nbquery = sql.purchase_orders
        NaphthaBaseObject.__init__(self)
    
    def get_po(self, PO_Num):
        return NaphthaBaseObject._sqlquery(self, PO_Num)

    def getdict(self, PO_Num):
        """Returns a list of dictionaries with purchase data.
        
        Each entry is returned as a dictionary, with column names as
        the dictionary keys.
        """

        results = NaphthaBaseObject._sqlquery_as_dict(self, PO_Num)
        return [line for line in results]
    
    def purchase_orders(self, no_blank_columns = True):
        """Returns purchase orders that haven't been delivered"""
        
        purchase_orders = []
        for entry in self._data:
            qty_batched = entry[self._clmn['DeliveredQuantity']]
            status = entry[self._clmn['Status']]
            if qty_batched == '0.0000' or qty_batched == '1.0000':
                if status == 4:
                    purchase_orders.append(entry)
        return self._return_as_dict(purchase_orders, no_blank_columns)

    def supplier_history(self, SupplierID, all=False, no_blank_columns=True):
        """Returns history of orders from suppliers.
        
        Orders that haven't been delivered are excluded, unless 'all' is set
        to True.
        """
        
        supplier_history = []
        active_POs = [entry['PO_Num'] for entry in self.purchase_orders()]
        for entry in self._data:
            if entry[self._clmn['Supplier']] == SupplierID.upper():
                if all is False:
                    if entry[self._clmn['PO_Num']] not in active_POs:
                        supplier_history.append(entry)
                else:
                    supplier_history.append(entry)
        return self._return_as_dict(supplier_history, no_blank_columns)


#////////////////////////////////////////////////////////////////////////////#
class Stock(NaphthaBaseObject):
    """Updates and provides access to Stock information."""
#////////////////////////////////////////////////////////////////////////////#

    def __init__(self):
        self._table = 'Stock'
        self._randr_query = sql.get_stock
        self._nbquery = sql.get_batch
        NaphthaBaseObject.__init__(self)

    def get_batch(self, Batch_Num):
        return NaphthaBaseObject._sqlquery(self, Batch_Num)

    def get_dict(self, Batch_Num):
        return NaphthaBaseObject._sqlquery_as_dict(self, Batch_Num)


#////////////////////////////////////////////////////////////////////////////#
class Sales(NaphthaBaseObject):
    """Updates and provides access to Sales and Despatch information."""
#////////////////////////////////////////////////////////////////////////////#

    def __init__(self):
        self._table = 'Sales'
        self._randr_query = sql.get_sales
        self._nbquery = sql.sales_orders
        NaphthaBaseObject.__init__(self)
        # Create a list of WO numbers that have been deleted
        self._deleted = self._getdata('DeletedSales')
    
    def get_wo(self, WO_Num):
        results = NaphthaBaseObject._sqlquery(self, WO_Num)
        if results == []:
            # if the WO number can't be found check the list of deleted orders
            results = NaphthaBaseObject._sqlquery(self, WO_Num, \
                                                  sql.deleted_sales_orders)
        return [line for line in results]
    
    def getdict(self, WO_Num):
        """Returns a list of dictionaries with sales data.
        
        Each entry is returned as a dictionary, with column names as
        the dictionary keys.
        """

        results = NaphthaBaseObject._sqlquery_as_dict(self, WO_Num)
        if results == []:
            results = NaphthaBaseObject._sqlquery(self, WO_Num, \
                                                  sql.deleted_sales_orders)
        return [line for line in results]

    def not_despatched(self):
        """Returns orders that haven't been despatched"""
        
        not_despatched = []
        for entry in self._data:
            if entry[self._clmn['Status']] == 0:
                not_despatched.append(entry)
        return not_despatched

    def customer_orders(self, CustomerID, no_blank_columns = True):
        """Returns a customer's orders that haven't been despatched"""
        
        customer_orders = []
        for entry in self.not_despatched():
            if entry[self._clmn['CustomerKey']] == CustomerID.upper():
                customer_orders.append(entry)
        return self._return_as_dict(customer_orders, no_blank_columns)

    def customer_history(self, CustomerID, all=False, no_blank_columns=True):
        """Returns history of customer orders.
        
        Orders that haven't been despatched are excluded, unless 'all' is set
        to True.
        """
        
        customer_history = []
        for entry in self._data:
            if entry[self._clmn['CustomerKey']] == CustomerID.upper():
                if all is False:
                    if entry[self._clmn['Status']] != 0:
                        customer_history.append(entry)
                else:
                    customer_history.append(entry)
        return self._return_as_dict(customer_history, no_blank_columns)

    def _update_naphtha_base(self):
        NaphthaBaseObject._update_naphtha_base(self)
        # Create a list of WO numbers that have been deleted
        self._deleted = self._getdata('DeletedSales')
        

#////////////////////////////////////////////////////////////////////////////#
class Hauliers(NaphthaBaseObject):
    """Updates and provides access to Haulier names.
    
    If the R&R database can be connected to, the haulier names are read,
    written to the NaphthaBase and stored in memory as a Python Dictionary.
    If the R&R database can't be found then only NaphthaBase data is used.
    """
#////////////////////////////////////////////////////////////////////////////#

    def __init__(self):
        self._table = 'Hauliers'
        self._randr_query = sql.get_hauliers
        NaphthaBaseObject.__init__(self)
        self._create_db()
    
    def get_name(self, haulier_key):
        return NaphthaBaseObject._getfromdict(self, haulier_key)
    
    def _create_db(self):
        """Creates a python dictionary of haulier codes and descriptions.
        """

        self._hauliers_dict = {}
        for entry in self._data:
            haulier_key = entry[self._clmn['HaulierKey']]
            name = entry[self._clmn['Name']]
            nominal = entry[self._clmn['NominalCode']]
            self._hauliers_dict[haulier_key] = [name, nominal]
        self._datadict = self._hauliers_dict
    
    def _update_naphtha_base(self):
        NaphthaBaseObject._update_naphtha_base(self)
        self._create_db()


#////////////////////////////////////////////////////////////////////////////#
class Customer(NaphthaBaseObject):
    """Updates and provides access to Customer details."""
#////////////////////////////////////////////////////////////////////////////#

    def __init__(self):
        self._table = 'Customer'
        self._randr_query = sql.get_customer
        self._nbquery = sql.customer
        NaphthaBaseObject.__init__(self)

    def get_customer(self, CustomerID):
        return NaphthaBaseObject._sqlquery(self, CustomerID)

    def get_dict(self, CustomerID):
        return NaphthaBaseObject._sqlquery_as_dict(self, CustomerID)


#////////////////////////////////////////////////////////////////////////////#
class Depot(NaphthaBaseObject):
    """Updates and provides access to Warehouse Address details."""
#////////////////////////////////////////////////////////////////////////////#

    def __init__(self):
        self._table = 'Depot'
        self._randr_query = sql.get_depot
        self._nbquery = sql.depot
        NaphthaBaseObject.__init__(self)

    def get_depot(self, ClientID):
        return NaphthaBaseObject._sqlquery(self, ClientID)

    def get_dict(self, ClientID):
        return NaphthaBaseObject._sqlquery_as_dict(self, ClientID)


#////////////////////////////////////////////////////////////////////////////#
class Contact(NaphthaBaseObject):
    """Updates and provides access to Contact details."""
#////////////////////////////////////////////////////////////////////////////#

    def __init__(self):
        self._table = 'Contact'
        self._randr_query = sql.get_contact
        self._nbquery = sql.contact
        NaphthaBaseObject.__init__(self)

    def get_contact(self, ClientID):
        return NaphthaBaseObject._sqlquery(self, ClientID)

    def get_dict(self, ClientID):
        return NaphthaBaseObject._sqlquery_as_dict(self, ClientID)


#////////////////////////////////////////////////////////////////////////////#
class Supplier(NaphthaBaseObject):
    """Updates and provides access to Supplier details."""
#////////////////////////////////////////////////////////////////////////////#

    def __init__(self):
        self._table = 'Supplier'
        self._randr_query = sql.get_supplier
        self._nbquery = sql.supplier
        NaphthaBaseObject.__init__(self)

    def get_supplier(self, SupplierID):
        return NaphthaBaseObject._sqlquery(self, SupplierID)

    def get_dict(self, SupplierID):
        return NaphthaBaseObject._sqlquery_as_dict(self, SupplierID)


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
    depot = Depot()
    contact = Contact()
    supplier = Supplier()