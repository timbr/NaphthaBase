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

from nbsettings import *
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
    tablelist = {'purchaseorder': sql.create_purchaseorder_table,
                 'purchaseitem': sql.create_purchaseitem_table,
                 'material': sql.create_material_table,
                 'stock': sql.create_stock_table,
                 'stockmovement': sql.create_stockmovement_table,
                 'salesorder': sql.create_salesorder_table,
                 'salesitem': sql.create_salesitem_table,
                 'despatch': sql.create_despatch_table,
                 'deletedsales': sql.create_deletedsales_table,
                 'hauliers': sql.create_hauliers_table,
                 'carrier': sql.create_carrier_table,
                 'customer': sql.create_customer_table,
                 'supplier': sql.create_supplier_table,
                 'contact': sql.create_contact_table,
                 'depot': sql.create_depot_table}
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
        entry = [None] + entry # Add null value so that primary key autoincrements
        results = [row for row in c.execute(query, entry)]
    NaphthaBase.commit()
    NaphthaBase.close()


def get_randr_data(query, table = '', last_updated = '',
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
    
    print query
    RandRdata = RandRcursor.execute(query % {'lastupdate': last_updated})
    #try:
    #    RandRdata = RandRcursor.execute(query % {'lastupdate': last_updated})
     #   print 'got R&R stock date'
    #except:
    #    if table == '':
    #        RandRcursor = accounts_connection.cursor()
    #        RandRdata = RandRcursor.execute(query % {'lastupdate': last_updated})
    #        print 'got R&R accounts data'
    
    #RandR_Stringed = stringprocess(RandRdata) # convert decimal types to strings
    #return RandR_Stringed
    return [line for line in RandRdata]
    
    
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

