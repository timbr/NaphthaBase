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
