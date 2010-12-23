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

tim = nb.naphthabase_query("select id from customer where customer_code='%(code)s'" % {'code': 'VERIFY'})
data = getdata(nb.sql.get_contact, 'Contact')
newdata = []
for item in data:
    line = []
    line[0:5] = item[0:5]
    customercode = nb.naphthabase_query("select id from customer where customer_code='%(code)s'" % {'code': item[0]})
    if len(customercode) > 0:
        line.append(customercode[0][0])
    else:
        line.append(None)
    suppliercode = nb.naphthabase_query("select id from supplier where supplier_code='%(code)s'" % {'code': item[0]})
    if len(suppliercode) > 0:
        line.append(suppliercode[0][0])
    else:
        line.append(None)
    line[8:] = item[5:]
    newdata.append(line)
    print line
update(newdata, 'contact')
    