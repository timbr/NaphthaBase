import naphthabase as nb
import sql
import datetime

nb.make_database_connection()
tablelist = {'Formula': sql.formula,
             'PurchaseOrder': sql.purchase_order,
             'PurchaseItem': sql.purchase_item,
             'FormulaStock': sql.formula_stock,
             'FormulaStockUsage': sql.formula_stock_usage,
             'SalesOrder': sql.sales_order,
             'SalesOrderItem': sql.sales_order_item,
             'SalesOrderAdditional': sql.sales_order_additional,
             'SalesOrderDespatch': sql.sales_order_despatch,
             'MissingOrderNumber': sql.missing_order_number,
             'AdditionalItems': sql.additional_items,
             'Customer': sql.customer,
             'Depot': sql.depot,
             'Contact': sql.contact,
             'Supplier': sql.supplier}


for table in tablelist.keys():
    print table
    last_updated = nb.naphthabase_query \
                       ("SELECT MAX(LastUpdated) from %s" % table)[0][0]
    if last_updated == None:
        last_updated = datetime.datetime(1982,1,1,0,0)
    #nb.naphthabase_query("DELETE FROM %s" % table) # Clear table
    RandRdata = nb.get_randr_data(tablelist[table], table, last_updated)
    num_fields = len(nb.get_columns(table))
    insert_fields = '(null,' + '?,' * (num_fields - 2) + '?)'
    # creates string "insert into <table> values (?,?,?,?, etc)"
    nb.naphthabase_transfer(RandRdata, 'insert into %s values %s' \
                                       % (table, insert_fields))