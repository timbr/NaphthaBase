import naphthabase as nb
import datetime
import decimal


def getdata(randr_query, table):
    print 'Getting %s data' % (table)
    data = nb.get_randr_data(randr_query, table)
    return data


def update(data, table):
    print 'Updating NaphthaBase with latest %s Data.' % table
    nb.naphthabase_query("DELETE FROM %s" % table) # Clear table
    num_fields = len(nb.get_columns(table))
    insert_fields = '(' + '?,' * (num_fields - 1) + '?)'
    # creates string "insert into <table> values (?,?,?,?, etc)"
    nb.naphthabase_transfer(data, 'insert into %s values %s' \
                                % (table, insert_fields))

class DataContainer(object):
    def __init__(self):
        self.datatable = []
        self._dataline = []
    
    def addentry(self, data):
        """Add the given data item to the dataline list.
        
        Any decimal values are converted to strings first.
        """
        
        if type(data) is decimal.Decimal:
            data = str(data)
        self._dataline.append(data)
        
    def combine(*args, **kwargs):
        """Combines several dataitems into a single string.
        
        By default, commas are removed from the end of dataitems. The optional
        filter argument can be used to specify other characters to strip.
        By default, a newline character is added to the end of each dataitem (apart from the last). The optional separator argument can be used to specify other end of line characters.
        """
        
        filter = kwargs.get('filter', ',')
        separator = kwargs.get('separator', '\n')
        output = ''
        for line in args[1:]:
            # first arg says <__main__.DataContainer object at 0x031E9830>
            output = output + line.strip(filter) + separator
        output = output.strip(separator)
        # No new-line character wanted at the end.
        return output
    
    def addline(self):
        self.datatable.append(self._dataline)
        self._dataline = []
    
    def process(self, datablock):
        for line in datablock:
            for entry in line:
                self.addentry(entry)
            self.addline()


def material():
    data = getdata(nb.sql.get_material_codes, 'Material')
    dc = DataContainer()
    dc.process(data)
    update(dc.datatable, 'material')
    global materialdata
    materialdata = [row for row in nb.naphthabase_query("select code, id from material")]

def hauliers():
    data = getdata(nb.sql.get_hauliers, '\"Additional Items\"')
    dc = DataContainer()
    dc.process(data)
    update(dc.datatable, 'hauliers')

def carrier():
    data = getdata(nb.sql.get_carrier, '\"Sales Order Additional\"')
    dc = DataContainer()
    dc.process(data)
    update(dc.datatable, 'carrier')
    global carrierdata
    carrierdata = [row for row in nb.naphthabase_query("select won, id from carrier")]

def customer():
    data = getdata(nb.sql.get_customer, 'Customer')
    dc = DataContainer()
    for cstmr in data:
        dc.addentry(cstmr.CustomerID)
        dc.addentry(cstmr.Name)
        address = dc.combine(cstmr.Address1,
                             cstmr.Address2,
                             cstmr.Address3,
                             cstmr.Address4,
                             cstmr.Address5)
        dc.addentry(address)
        dc.addentry(cstmr.PostCode)
        dc.addentry(cstmr.Telephone)
        dc.addentry(cstmr.Fax)
        dc.addentry(cstmr.Email)
        dc.addentry(cstmr.Website)
        dc.addentry(cstmr.ContactName)
        dc.addentry(cstmr.VAT)
        dc.addentry(cstmr.Comment)
        dc.addentry(cstmr.Memo)
        dc.addentry(cstmr.CreditLimit)
        dc.addentry(cstmr.Terms)
        dc.addentry(cstmr.LastUpdated)
        dc.addentry(cstmr.RecordNumber)
        dc.addline()
    update(dc.datatable, 'customer')
    global customerdata
    customerdata = [row for row in nb.naphthabase_query("select customer_code, id from customer")]
    
def get_customercode(customerid):
    cstmr_pk = [data[1] for data in customerdata if data[0] == customerid]
    if len(cstmr_pk) > 1:
        # There should only be one matching customer code
        raise NameError('THERE IS MORE THAN 1 MATCHING CUSTOMER')
    elif len(cstmr_pk) == 0:
        return None
    else:
        return cstmr_pk[0]

def supplier():
    data = getdata(nb.sql.get_supplier, 'Supplier')
    dc = DataContainer()
    for spplr in data:
        dc.addentry(spplr.SupplierID)
        dc.addentry(spplr.Name)
        address = dc.combine(spplr.Address1,
                             spplr.Address2,
                             spplr.Address3,
                             spplr.Address4,
                             spplr.Address5)
        dc.addentry(address)
        dc.addentry(spplr.PostCode)
        dc.addentry(spplr.Telephone)
        dc.addentry(spplr.Fax)
        dc.addentry(spplr.Email)
        dc.addentry(spplr.Website)
        dc.addentry(spplr.ContactName)
        dc.addentry(spplr.VAT)
        dc.addentry(spplr.Comment)
        dc.addentry(spplr.Memo)
        dc.addentry(spplr.LastUpdated)
        dc.addentry(spplr.RecordNumber)
        dc.addline()
    update(dc.datatable, 'supplier')
    global supplierdata
    supplierdata =[row for row in nb.naphthabase_query("select supplier_code, id from supplier")]

def get_suppliercode(supplierid):
    spplr_pk = [data[1] for data in supplierdata if data[0] == supplierid]
    if len(spplr_pk) > 1:
        # There should only be one matching supplier code
        raise NameError('THERE IS MORE THAN 1 MATCHING SUPPLIER')
    elif len(spplr_pk) == 0:
        return None
    else:
        return spplr_pk[0]

def contact():
    data = getdata(nb.sql.get_contact, 'Contact')
    dc = DataContainer()
    for cntct in data:
        dc.addentry(cntct.ClientID)
        dc.addentry(cntct.Title)
        dc.addentry(cntct.Forename)
        dc.addentry(cntct.Surname)
        dc.addentry(cntct.Phone)
        dc.addentry(cntct.Department)
        dc.addentry(get_customercode(cntct.ClientID))
        dc.addentry(get_suppliercode(cntct.ClientID))
        dc.addentry(cntct.LastUpdated)
        dc.addentry(cntct.RecordNumber)
        dc.addline()
    update(dc.datatable, 'contact')

def depot():
    data = getdata(nb.sql.get_depot, 'Depot')
    dc = DataContainer()
    for dpt in data:
        dc.addentry(dpt.ClientID)
        dc.addentry(dpt.Name)
        address = dc.combine(dpt.Address1,
                             dpt.Address2,
                             dpt.Address3,
                             dpt.Address4,
                             dpt.Address5)
        dc.addentry(address)
        dc.addentry(dpt.PostCode)
        dc.addentry(dpt.Telephone)
        dc.addentry(dpt.Fax)
        dc.addentry(dpt.Email)
        dc.addentry(dpt.Comment)
        dc.addentry(get_customercode(dpt.ClientID))
        dc.addentry(get_suppliercode(dpt.ClientID))
        dc.addentry(dpt.LastUpdated)
        dc.addentry(dpt.RecordNumber)
        dc.addline()
    update(dc.datatable, 'depot')

def purchase():
    data = getdata(nb.sql.get_purchaseorder, '\"Purchase Order\"')
    dc = DataContainer()
    for prchse in data:
        dc.addentry(prchse.PO_Num)
        dc.addentry(prchse.OrderValue)
        dc.addentry(get_suppliercode(prchse.Supplier))
        dc.addentry(prchse.OrderReference)
        dc.addentry(prchse.OrderDate)
        dc.addentry(prchse.PlacedBy)
        dc.addentry(prchse.PrintedComment)
        dc.addentry(prchse.DeliveryComment)
        dc.addentry(prchse.Status)
        dc.addentry(prchse.LastUpdated)
        dc.addentry(prchse.RecordNumber)
        dc.addline()
    update(dc.datatable, 'purchaseorder')
    global purchasedata
    purchasedata = [row for row in nb.naphthabase_query("select pon, id from purchaseorder")]

def purchaseitem():
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
    global purchaseitemdata
    purchaseitemdata = [row for row in nb.naphthabase_query("select pon, material_id, id from purchaseitem")]

def formula():
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
        purchaseitem = [data[2] for data in purchaseitemdata if data[0] == item[5] and data[1] == line[1]]
        if len(purchaseitem) > 0:
            line.append(purchaseitem[0])
        else:
            line.append(None)
        line[6:] = item[6:]
        newdata.append(line)
    update(newdata, 'stock')
    global stockdata
    stockdata = [row for row in nb.naphthabase_query("select batch, id from stock")]

def sales():
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
    global salesorderdata
    salesorderdata = [row for row in nb.naphthabase_query("select won, id from salesorder")]

def salesitem():
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
    global salesitemdata
    salesitemdata = [row for row in nb.naphthabase_query("select won, material_id, id from salesitem")]

def deletedsales():
    data = getdata(nb.sql.get_deleted_sales, '\"Missing Order Number\"')
    newdata = []
    for item in data:
        line = []
        line.append(item[0])
        salesordercode = [data[1] for data in salesorderdata if data[0] == item[0]]
        if len(salesordercode) > 0:
            line.append(salesordercode[0])
        else:
            line.append(None)
        line[2:] = item[1:]
        newdata.append(line)
    update(newdata, 'deletedsales')

def despatch():
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
        salesitemcode = [data[2] for data in salesitemdata if data[0] == item[0]]
        if len(salesitemcode) > 0:
            line.append(salesitemcode[0])
        else:
            line.append(None)
        line[4:] = item[4:]
        newdata.append(line)
    update(newdata, 'despatch')

def stockusage():
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
        materialcode = [data[1] for data in materialdata if data[0] == item[4]]
        if len(materialcode) != 1:
            materialcode = None
        else:
            materialcode = materialcode[0]
        salesitemcode = [data[2] for data in salesitemdata if data[0] == item[3] and data[1] == materialcode]
        if len(salesitemcode) > 0:
            line.append(salesitemcode[0])
        else:
            line.append(None)
        line[4:] = item[5:]
        newdata.append(line)
    update(newdata, 'stockmovement')

if __name__ == '__main__':
    nb.make_database_connection()
    material()
    hauliers()
    carrier()
    customer()
    supplier()
    contact()
    depot()
    purchase()
    purchaseitem()
    formula()
    sales()
    salesitem()
    deletedsales()
    despatch()
    stockusage()