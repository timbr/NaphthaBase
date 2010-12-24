import naphthabase as nb
import datetime

nb.make_database_connection()

def getdata(randr_query, table):
    return nb.get_randr_data(randr_query, table)


def update(data, table):
    print 'Updating NaphthaBase with latest %s Data.' % table
    nb.naphthabase_query("DELETE FROM %s" % table) # Clear table
    num_fields = len(nb.get_columns(table))
    insert_fields = '(' + '?,' * (num_fields - 1) + '?)'
    # creates string "insert into <table> values (?,?,?,?, etc)"
    nb.naphthabase_transfer(data, 'insert into %s values %s' \
                                % (table, insert_fields))



data = getdata(nb.sql.material_codes, 'Material')
update(data, 'material')
materialdata = [row for row in nb.naphthabase_query("select code, id from material")]

data = getdata(nb.sql.get_hauliers, '\"Additional Items\"')
update(data, 'hauliers')

data = getdata(nb.sql.get_carrier, '\"Sales Order Additional\"')
update(data, 'carrier')
carrierdata = [row for row in nb.naphthabase_query("select won, id from carrier")]


data = getdata(nb.sql.get_customer, 'Customer')
newdata = []
for item in data:
    line = []
    line.append(item[0])
    line.append(item[1])
    line.append("%s\n%s\n%s\n%s\n%s" % (item[2], item[3], item[4], item[5], item[6]))
    line[3:] = item[7:]
    newdata.append(line)
update(newdata, 'customer')
customerdata = [row for row in nb.naphthabase_query("select customer_code, id from customer")]

data = getdata(nb.sql.get_supplier, 'Supplier')
newdata = []
for item in data:
    line = []
    line.append(item[0])
    line.append(item[1])
    line.append("%s\n%s\n%s\n%s\n%s" % (item[2], item[3], item[4], item[5], item[6]))
    line[3:] = item[7:]
    newdata.append(line)
update(newdata, 'supplier')
supplierdata =[row for row in nb.naphthabase_query("select supplier_code, id from supplier")]


data = getdata(nb.sql.get_contact, 'Contact')
newdata = []
for item in data:
    line = []
    line[0:5] = item[0:5]
    customercode = [data[1] for data in customerdata if data[0] == item[0]]
    if len(customercode) > 0:
        line.append(customercode[0])
    else:
        line.append(None)
    suppliercode = [data[1] for data in supplierdata if data[0] == item[0]]
    if len(suppliercode) > 0:
        line.append(suppliercode[0])
    else:
        line.append(None)
    line[8:] = item[5:]
    newdata.append(line)
update(newdata, 'contact')

data = getdata(nb.sql.get_purchaseorder, '\"Purchase Order\"')
newdata = []
for item in data:
    line = []
    line[0:2] = item[0:2]
    suppliercode = [data[1] for data in supplierdata if data[0] == item[2]]
    if len(suppliercode) > 0:
        line.append(suppliercode[0])
    else:
        line.append(None)
    line[3:] = item[3:]
    newdata.append(line)
update(newdata, 'purchaseorder')
purchasedata = [row for row in nb.naphthabase_query("select pon, id from purchaseorder")]

data = getdata(nb.sql.get_purchaseitem, '\"Purchase Item\"')
newdata = []
for item in data:
    line = []
    line.append(item[0])
    purchaseorder = [data[1] for data in purchasedata if data[0] == item[0]]
    if len(purchaseorder) > 0:
        line.append(purchaseorder[0])
    else:
        line.append(None)
    materialcode = [data[1] for data in materialdata if data[0] == item[1]]
    if len(materialcode) > 0:
        line.append(materialcode[0])
    else:
        line.append(None)
    line[3:] = item[2:]
    newdata.append(line)
update(newdata, 'purchaseitem')


data = getdata(nb.sql.get_stock, 'Formula Stock')
newdata = []
for item in data:
    line = []
    line.append(item[0])
    materialcode = [data[1] for data in materialdata if data[0] == item[1]]
    if len(materialcode) > 0:
        line.append(materialcode[0])
    else:
        line.append(None)
    line.append(item[2])
    line.append(item[3])
    suppliercode = [data[1] for data in supplierdata if data[0] == item[4]]
    if len(suppliercode) > 0:
        line.append(suppliercode[0])
    else:
        line.append(None)
    purchaseorder = [data[1] for data in purchasedata if data[0] == item[5]]
    if len(purchaseorder) > 0:
        line.append(purchaseorder[0])
    else:
        line.append(None)
    line[6:] = item[6:]
    newdata.append(line)
update(newdata, 'stock')
stockdata = [row for row in nb.naphthabase_query("select batch, id from stock")]


data = getdata(nb.sql.get_salesorder, '\"Sales Order\"')
newdata = []
for item in data:
    line = []
    line.append(item[0])
    line.append(item[1])
    customercode = [data[1] for data in customerdata if data[0] == item[2]]
    if len(customercode) > 0:
        line.append(customercode[0])
    else:
        line.append(None)
    line[3:12] = item[3:12]
    line.append("%s\n%s\n%s\n%s" % (item[12], item[13], item[14], item[15]))
    line.append(item[16])
    line.append("%s\n%s\n%s\n%s\n%s" % (item[17], item[18], item[19], item[20], item[21]))
    line.append("%s\n%s\n%s\n%s\n%s\n%s" % (item[22], item[23], item[24], item[25], item[26], item[27]))
    line.append(item[28])
    line.append(item[29])
    carriercode = [data[1] for data in carrierdata if data[0] == item[0]]
    if len(carriercode) > 0:
        line.append(carriercode[0])
    else:
        line.append(None)
    line.append(item[30])
    line.append(item[31])
    newdata.append(line)
update(newdata, 'salesorder')
salesorderdata = [row for row in nb.naphthabase_query("select won, id from salesorder")]


data = getdata(nb.sql.get_salesitem, '\"Sales Order Item\"')
newdata = []
for item in data:
    line = []
    line.append(item[0])
    salesordercode = [data[1] for data in salesorderdata if data[0] == item[0]]
    if len(salesordercode) > 0:
        line.append(salesordercode[0])
    else:
        line.append(None)
    materialcode = [data[1] for data in materialdata if data[0] == item[1]]
    if len(materialcode) > 0:
        line.append(materialcode[0])
    else:
        line.append(None)
    line[3:] = item[2:]
    newdata.append(line)
update(newdata, 'salesitem')
salesitemdata = [row for row in nb.naphthabase_query("select won, id from salesitem")]


data = getdata(nb.sql.get_despatch, '\"Sales Order Despatch\"')
newdata = []
for item in data:
    line = []
    line.append(item[0])
    line.append(item[1])
    stockcode = [data[1] for data in stockdata if data[0] == item[2]]
    if len(stockcode) > 0:
        line.append(stockcode[0])
    else:
        line.append(None)
    salesitemcode = [data[1] for data in salesitemdata if data[0] == item[0]]
    if len(salesitemcode) > 0:
        line.append(salesitemcode[0])
    else:
        line.append(None)
    line[4:] = item[4:]
    newdata.append(line)
update(newdata, 'despatch')


data = getdata(nb.sql.get_stockusage, '\"Formula Stock Usage\"')
newdata = []
for item in data:
    line = []
    stockcode = [data[1] for data in stockdata if data[0] == item[0]]
    if len(stockcode) > 0:
        line.append(stockcode[0])
    else:
        line.append(None)
    line.append(item[1])
    customercode = [data[1] for data in customerdata if data[0] == item[2]]
    if len(customercode) > 0:
        line.append(customercode[0])
    else:
        line.append(None)
    salesordercode = [data[1] for data in salesorderdata if data[0] == item[3]]
    if len(salesordercode) > 0:
        line.append(salesordercode[0])
    else:
        line.append(None)
    line[4:] = item[4:]
    newdata.append(line)
update(newdata, 'stockmovement')
