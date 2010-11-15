import naphthabase as nb
import sql

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
    nb.naphthabase_query("DELETE FROM %s" % table) # Clear table
    RandRdata = nb.get_randr_data(tablelist[table], table)
    num_fields = len(nb.get_columns(table))
    insert_fields = '(' + '?,' * (num_fields - 1) + '?)'
    # creates string "insert into <table> values (?,?,?,?, etc)"
    nb.naphthabase_transfer(RandRdata, 'insert into %s values %s' \
                                       % (table, insert_fields))