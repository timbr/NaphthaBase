# settings.py

import os

RandR_Naphtha_Dbase = "S:\\NAPHTHAV6\\DATA\\Naphtha.mdb"
RandR_Accounts_Dbase = "S:\\NAPHTHAV6\\DATA\\Naphtha_accounts.mdb"
accountsDBpassword = "bgSoiqOogNMOH"

# NaphthaBase tables that originate from the R&R 'Naphtha.mdb' database
stock_tables = ['Formula', 'PurchaseOrder', 'PurchaseItem', 'FormulaStock', 'FormulaStockUsage', 'SalesOrder', 'SalesOrderItem', 'SalesOrderAdditional', 'SalesOrderDespatch', 'MissingOrderNumber', 'AdditionalItems']
# NaphthaBase tables that originate from the R&R 'Naphtha_accounts.mdb' database
accounts_tables = ['Customer', 'Depot', 'Contact', 'Supplier']

TestDB_New = "C:\\Users\\Tim\\Desktop\\NaphthaBase\\Local Test Databases\\New\\Naphtha.mdb"
TestDB_Old = "C:\\Users\\Tim\\Desktop\\NaphthaBase\\Local Test Databases\\Old\\Naphtha.mdb"
TestDB_Acc_Old = "C:\\Users\\Tim\\Desktop\\NaphthaBase\\Local Test Databases\\Old\\Naphtha_accounts.mdb"

if os.getenv('COMPUTERNAME') == 'ACER5920':
    NaphthaBase_Dbase = "C:\\Users\\Tim\\Desktop\\NaphthaBase\\NaphthaBase.db"
else:
    NaphthaBase_Dbase = "C:\\Users\\Tim\\Documents\\My Dropbox\\NaphthaBase\\NaphthaBase.db"