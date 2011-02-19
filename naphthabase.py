""" naphthabase.py  -- Interface to the NaphthaBase Database.

Provides routines for taking a snapshot of the official R & R Associates 
database and saving the data in the NaphthaBase Database. All changes since
the last snapshot are added without deleting the older data.

Routines for quick and easy access to data in the NaphthaBase are also
provided.
"""

import pyodbc
import datetime
import os
import nbsettings
import sql
import logging

logger = logging.getLogger("logit")

#////////////////////////////////////////////////////////////////////////////#
class RandRDatabase(object):
    """Creates a connection to the R&R databases.
    
    Connections are made to the stock and accounts
    databases and a method is provided for making queries.
    """
#////////////////////////////////////////////////////////////////////////////#

    def __init__(self):
        self.naphthav6 = nbsettings.RandR_Naphtha_Dbase
        self.naphtha_accounts = nbsettings.RandR_Accounts_Dbase
        self.accounts_db_password = nbsettings.accountsDBpassword
        self.connected = 0
        if self.connect() == True:
            self.list_tables()
        self.disconnect()
        
    def connect(self):
        if os.path.exists(self.naphthav6):
            self.stock_connection = \
               pyodbc.connect(DRIVER = '{Microsoft Access Driver (*.mdb)}',
                          DBQ = self.naphthav6)
            #logger.debug("Made connection with R&R database at %s" % self.naphthav6)
            self.connected = 1
        else:
            logger.warn("Unable to make connection with R&R database at %s" \
                                                              % self.naphthav6)
        if os.path.exists(self.naphtha_accounts):
            self.accounts_connection = \
               pyodbc.connect(DRIVER='{Microsoft Access Driver (*.mdb)}',
                 DBQ = self.naphtha_accounts, PWD = self.accounts_db_password)
            #logger.debug("Made connection with R&R Accounts database at %s" \
            #                                           % self.naphtha_accounts)
            self.connected += 1
        else:
            logger.warn("Unable to make connection with R&R Accounts database at %s" \
                                                       % self.naphtha_accounts)
        if self.connected == 2:
            return True
        else:
            return False

    def disconnect(self):
        if self.connected == 2:
            self.stock_connection.close()
            self.accounts_connection.close()
            self.connected = 0

    def list_tables(self):
        if self.connected == 0:
            self.connect()
        stock_cursor = self.stock_connection.cursor()
        accounts_cursor = self.accounts_connection.cursor()
        self.stock_tables = ['stock_' + row.table_name for row in stock_cursor.tables()]
        self.accounts_tables = ['accounts_' + row.table_name for row in accounts_cursor.tables()]
        self.disconnect()
    
    def query(self, query, table, last_updated = ''):
        if self.connected == 0:
            if self.connect() == False:
                return 'Unable to connect'
        if last_updated == '':
            last_updated = datetime.datetime(1982,1,1,0,0)
        # Connect to the correct R&R database file.
        if table in self.stock_tables:
            RandRcursor = self.stock_connection.cursor()
        elif table in self.accounts_tables:
            RandRcursor = self.accounts_connection.cursor()
        else:
            logger.warn("Table %s not found in R&R Database" % table)
        RandRdata = RandRcursor.execute(query % {'lastupdate': last_updated})
        results = [line for line in RandRdata]
        self.disconnect()
        return results
    
    def simplequery(self, query, variable):
        self.connect()
        RandRcursor = self.stock_connection.cursor()
        RandRdata = RandRcursor.execute(query, variable)
        results = [line for line in RandRdata]
        self.disconnect()
        return results

