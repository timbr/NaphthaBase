import naphthabase as nb
import datetime
import decimal

#////////////////////////////////////////////////////////////////////////////#
class DataTransferObject(object):
    """Universal data transfer class.
    
    Contains basic routines for transferring data from the
    R&R database to the NaphhaBase. Each table that needs
    to be transferred should subclass DataTransferObject.
    """
#////////////////////////////////////////////////////////////////////////////#
    
    def __init__(self):
        self.rrdata = nb.RandRDatabase()
        self.naphthabase = nb.NaphthaBase()
        self.dc = DataContainer()
        self.getdata(self.r_and_r_sql, self.r_and_r_table)
        
    def getdata(self, randr_query, table):
        print 'Getting %s data' % (table)
        self.data = self.rrdata.query(randr_query, table)
        
    def update(self, data, table):
        print 'Updating NaphthaBase with latest %s Data.' % table
        self.naphthabase.query("DELETE FROM %s" % table) # Clear table
        num_fields = len(self.naphthabase.get_columns(table))
        insert_fields = '(' + '?,' * (num_fields - 1) + '?)'
        # creates string "insert into <table> values (?,?,?,?, etc)"
        self.naphthabase.transfer(data, 'insert into %s values %s' \
                                    % (table, insert_fields))
            

#////////////////////////////////////////////////////////////////////////////#
class DataContainer(object):
    """Container for staging a table before uploading to the NaphthaBase.
    
    A table can be built up row by row in the DataContainer using addentry, or
    transferred in one go using process. Any decimal values are converted to
    strings first. Several lines can be combined into one using combine.
    """
#////////////////////////////////////////////////////////////////////////////#
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


#////////////////////////////////////////////////////////////////////////////#
class QuickReference(object):
    """Storage for an in-memory table for quick look-ups
    """
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self, table = '', fields = ''):
        self.naphthabase = nb.NaphthaBase()
        if table != '' and fields != '':
            self.create_memory_table(table, fields)

    def create_memory_table(self, table, fields = ''):
        if fields == '':
            fields = '*'
            self.columns = self.naphthabase.get_columns(table)
        else:
            self.columns = list(fields)
            fields = ('%s,' * len(fields)).strip(',') % fields
        self.pos = {}
        for f in self.columns:
            self.pos[f] = self.columns.index(f)
        self.memorydata = [row for row in self.naphthabase.query("select %s from %s" % (fields, table))]
    
    def get_id(self, reply = 'id', **kwargs):
        p = self.pos
        columns_of_interest = kwargs.keys()
        if len(columns_of_interest) == 1:
            col = columns_of_interest[0]
            value = kwargs[col]
            self.id = [line[p[reply]] for line in self.memorydata if line[p[col]] == value]
        elif len(columns_of_interest) == 2:
            col0 = columns_of_interest[0]
            value0 = kwargs[col0]
            col1 = columns_of_interest[1]
            value1 = kwargs[col1]
            self.id = [line[p[reply]] for line in self.memorydata if line[p[col0]] == col0 and line[p[col1]] == value1]
        if len(self.id) > 1:
            self.duplicates()
        elif len(self.id) == 0:
            return None
        else:
            return self.id[0]

    def duplicates(self):
        # More than one matching reference has been found
        print 'duplicates:', self.id
        raise NameError('MORE THAN ONE MATCHING REFERENCE FOUND')



#////////////////////////////////////////////////////////////////////////////#
class Material(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self):
        self.r_and_r_sql = nb.sql.get_material_codes
        self.r_and_r_table = 'stock_Formula'
        DataTransferObject.__init__(self)
        self.dc.process(self.data)
        self.update(self.dc.datatable, 'material')
        self.qr = self.QR('material', ('id', 'code'))
        
    class QR(QuickReference):
        def __init__(self, table = '', fields = ''):
            QuickReference.__init__(self, table, fields)


#////////////////////////////////////////////////////////////////////////////#
class Hauliers(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self):
        self.r_and_r_sql = nb.sql.get_hauliers
        self.r_and_r_table = 'stock_Additional Items'
        DataTransferObject.__init__(self)
        self.dc.process(self.data)
        self.update(self.dc.datatable, 'hauliers')        

        
#////////////////////////////////////////////////////////////////////////////#
class Carrier(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self):
        self.r_and_r_sql = nb.sql.get_carrier
        self.r_and_r_table = 'stock_Sales Order Additional'
        DataTransferObject.__init__(self)
        self.dc.process(self.data)
        self.update(self.dc.datatable, 'carrier') 
        self.qr = self.QR('carrier', ('id', 'won', 'description', 'lastupdated'))
        
    class QR(QuickReference):
        def __init__(self, table = '', fields = ''):
            QuickReference.__init__(self, table, fields)


#////////////////////////////////////////////////////////////////////////////#
class Customer(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self):
        self.r_and_r_sql = nb.sql.get_customer
        self.r_and_r_table = 'accounts_Customer'
        DataTransferObject.__init__(self)
        for cstmr in self.data:
            self.dc.addentry(cstmr.CustomerID)
            self.dc.addentry(cstmr.Name)
            address = self.dc.combine(cstmr.Address1,
                                      cstmr.Address2,
                                      cstmr.Address3,
                                      cstmr.Address4,
                                      cstmr.Address5)
            self.dc.addentry(address)
            self.dc.addentry(cstmr.PostCode)
            self.dc.addentry(cstmr.Telephone)
            self.dc.addentry(cstmr.Fax)
            self.dc.addentry(cstmr.Email)
            self.dc.addentry(cstmr.Website)
            self.dc.addentry(cstmr.ContactName)
            self.dc.addentry(cstmr.VAT)
            self.dc.addentry(cstmr.Comment)
            self.dc.addentry(cstmr.Memo)
            self.dc.addentry(cstmr.CreditLimit)
            self.dc.addentry(cstmr.Terms)
            self.dc.addentry(cstmr.LastUpdated)
            self.dc.addentry(cstmr.RecordNumber)
            self.dc.addline()
        self.update(self.dc.datatable, 'customer') 
        self.qr = self.QR('customer', ('id', 'customer_code'))
        
    class QR(QuickReference):
        def __init__(self, table = '', fields = ''):
            QuickReference.__init__(self, table, fields)


#////////////////////////////////////////////////////////////////////////////#
class Supplier(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self):
        self.r_and_r_sql = nb.sql.get_supplier
        self.r_and_r_table = 'accounts_Supplier'
        DataTransferObject.__init__(self)
        for spplr in self.data:
            self.dc.addentry(spplr.SupplierID)
            self.dc.addentry(spplr.Name)
            address = self.dc.combine(spplr.Address1,
                                      spplr.Address2,
                                      spplr.Address3,
                                      spplr.Address4,
                                      spplr.Address5)
            self.dc.addentry(address)
            self.dc.addentry(spplr.PostCode)
            self.dc.addentry(spplr.Telephone)
            self.dc.addentry(spplr.Fax)
            self.dc.addentry(spplr.Email)
            self.dc.addentry(spplr.Website)
            self.dc.addentry(spplr.ContactName)
            self.dc.addentry(spplr.VAT)
            self.dc.addentry(spplr.Comment)
            self.dc.addentry(spplr.Memo)
            self.dc.addentry(spplr.LastUpdated)
            self.dc.addentry(spplr.RecordNumber)
            self.dc.addline()
        self.update(self.dc.datatable, 'supplier') 
        self.qr = self.QR('supplier', ('id', 'supplier_code'))
        
    class QR(QuickReference):
        def __init__(self, table = '', fields = ''):
            QuickReference.__init__(self, table, fields)


#////////////////////////////////////////////////////////////////////////////#
class Contact(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self, customer, supplier):
        self.r_and_r_sql = nb.sql.get_contact
        self.r_and_r_table = 'accounts_Contact'
        DataTransferObject.__init__(self)
        for cntct in self.data:
            self.dc.addentry(cntct.ClientID)
            self.dc.addentry(cntct.Title)
            self.dc.addentry(cntct.Forename)
            self.dc.addentry(cntct.Surname)
            self.dc.addentry(cntct.Phone)
            self.dc.addentry(cntct.Department)
            self.dc.addentry(customer.qr.get_id(customer_code = cntct.ClientID))
            self.dc.addentry(supplier.qr.get_id(supplier_code = cntct.ClientID))
            self.dc.addentry(cntct.LastUpdated)
            self.dc.addentry(cntct.RecordNumber)
            self.dc.addline()
        self.update(self.dc.datatable, 'contact')






def carrier():
    data = getdata(nb.sql.get_carrier, '\"Sales Order Additional\"')
    dc = DataContainer()
    dc.process(data)
    update(dc.datatable, 'carrier')
    global carrierdata
    carrierdata = [row for row in nb.naphthabase_query("select won, id, description, lastupdated from carrier")]

def get_carriercode(won):
    carriercode = [data[1] for data in carrierdata if data[0] == won]
    if len(carriercode) > 1:
        # There should only be one matching carriercode
        print won, carriercode
        duplicates = checkduplication([data for data in carrierdata if data[0] == won])
        if not duplicates:
            raise NameError('THERE IS MORE THAN 1 MATCHING CARRIER')
    elif len(carriercode) == 0:
        return None
    else:
        return carriercode[0]

def checkduplication(itemlist):
    print itemlist
    dataset = set()
    for item in itemlist:
        for index, field in enumerate(item):
            if index != 1:
                # we want to ignore the id as we know this will be different!
                dataset.add(field)
    print 'dataset:', dataset
    if len(dataset) != len(item)-1:
        return False
    else:
        return True
            
            


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
    
def get_pocode(pon):
    purchaseorder = [data[1] for data in purchasedata if data[0] == pon]
    if len(purchaseorder) > 1:
        # There should only be one matching PO code
        raise NameError('THERE IS MORE THAN 1 MATCHING PO')
    elif len(purchaseorder) == 0:
        return None
    else:
        return purchaseorder[0]

def purchaseitem():
    data = getdata(nb.sql.get_purchaseitem, '\"Purchase Item\"')
    dc = DataContainer()
    for itm in data:
        dc.addentry(itm.PO_Num)
        dc.addentry(get_pocode(itm.PO_Num))
        dc.addentry(get_materialcode(itm.Material))
        dc.addentry(itm.Quantity)
        dc.addentry(itm.Price)
        dc.addentry(itm.DueDate)
        dc.addentry(itm.DeliveredQuantity)
        dc.addentry(itm.LastUpdated)
        dc.addentry(itm.RecordNumber)
        dc.addline()
    update(dc.datatable, 'purchaseitem')
    global purchaseitemdata
    purchaseitemdata = [row for row in nb.naphthabase_query("select pon, material_id, id from purchaseitem")]

def get_purchaseitemcode(pon, material):
    purchaseitem = [data[2] for data in purchaseitemdata if data[0] == pon and data[1] == material]
    if len(purchaseitem) > 1:
        # There should only be one matching Purchase Item code
        raise NameError('THERE IS MORE THAN 1 MATCHING Purchase Item')
    elif len(purchaseitem) == 0:
        return None
    else:
        return purchaseitem[0]

def formulastock():
    data = getdata(nb.sql.get_stock, 'Formula Stock')
    dc = DataContainer()
    for stck in data:
        dc.addentry(stck.Batch)
        dc.addentry(get_materialcode(stck.Material))
        dc.addentry(stck.StockInfo)
        dc.addentry(stck.BatchStatus)
        dc.addentry(get_suppliercode(stck.Supplier))
        dc.addentry(get_purchaseitemcode(stck.PO_Num, stck.Material))
        dc.addentry(stck.PurchaseCost)
        dc.addentry(stck.OriginalDeliveredQuantity)
        dc.addentry(stck.BatchUp_Date)
        dc.addentry(stck.QuantityNow)
        dc.addentry(stck.LastUpdated)
        dc.addentry(stck.RecordNumber)
        dc.addline()
    update(dc.datatable, 'stock')
    global stockdata
    stockdata = [row for row in nb.naphthabase_query("select batch, id from stock")]

def get_stockcode(batch):
    stockcode = [data[1] for data in stockdata if data[0] == batch]
    if len(stockcode) > 1:
        # There should only be one matching stockcode
        if batch not in ['15381']:
            raise NameError('THERE IS MORE THAN 1 MATCHING BATCH NUMBER')
    elif len(stockcode) == 0:
        return None
    else:
        return stockcode[0]

def sales():
    data = getdata(nb.sql.get_salesorder, '\"Sales Order\"')
    dc = DataContainer()
    for sls in data:
        dc.addentry(sls.WO_Num)
        dc.addentry(sls.Link)
        dc.addentry(get_customercode(sls.CustomerKey))
        dc.addentry(sls.CustomerOrderNumber)
        dc.addentry(sls.DespatchNotes)
        dc.addentry(sls.OrderValue)
        dc.addentry(sls.Status)
        dc.addentry(sls.OrderDate)
        dc.addentry(sls.DespatchDate)
        dc.addentry(sls.InvoiceDate)
        dc.addentry(sls.Operator)
        dc.addentry(sls.DespatchCompanyName)
        address = dc.combine(sls.DespatchAddress1,
                             sls.DespatchAddress2,
                             sls.DespatchAddress3,
                             sls.DespatchAddress4)
        dc.addentry(address)
        dc.addentry(sls.DespatchPostCode)
        delnotecomment = dc.combine(sls.DeliveryNoteComment1,
                                    sls.DeliveryNoteComment2,
                                    sls.DeliveryNoteComment3,
                                    sls.DeliveryNoteComment4,
                                    sls.DeliveryNoteComment5,
                                    filter = '')
        dc.addentry(delnotecomment)
        invoicecomment = dc.combine(sls.InvoiceComment1,
                                    sls.InvoiceComment2,
                                    sls.InvoiceComment3,
                                    sls.InvoiceComment4,
                                    sls.InvoiceComment5,
                                    sls.InvoiceComment6,
                                    filter = '')
        dc.addentry(invoicecomment)
        dc.addentry(sls.InvoiceTerms)
        dc.addentry(sls.ItemCount)
        dc.addentry(get_carriercode(sls.WO_Num))
        dc.addentry(sls.LastUpdated)
        dc.addentry(sls.RecordNumber)
        dc.addline()
    update(dc.datatable, 'salesorder')
    global salesorderdata
    salesorderdata = [row for row in nb.naphthabase_query("select won, id from salesorder")]

def get_salesordercode(won):
    salesorder = [data[1] for data in salesorderdata if data[0] == won]
    if len(salesorder) > 1:
        # There should only be one matching Sales Order code
        raise NameError('THERE IS MORE THAN 1 MATCHING SALES ORDER')
    elif len(salesorder) == 0:
        return None
    else:
        return salesorder[0]

def salesitem():
    data = getdata(nb.sql.get_salesitem, '\"Sales Order Item\"')
    dc = DataContainer()
    for itm in data:
        dc.addentry(itm.WO_Num)
        dc.addentry(get_salesordercode(itm.WO_Num))
        dc.addentry(get_materialcode(itm.Material))
        dc.addentry(itm.OrderQuantity)
        dc.addentry(itm.Price)
        dc.addentry(itm.RequiredDate)
        dc.addentry(itm.LastUpdated)
        dc.addentry(itm.RecordNumber)
        dc.addline()
    update(dc.datatable, 'salesitem')
    global salesitemdata
    salesitemdata = [row for row in nb.naphthabase_query("select won, material_id, id from salesitem")]

def get_salesitemcode(won, material):
    salesitem = [data[2] for data in salesitemdata if data[0] == won and data[1] == material]
    if len(salesitem) > 1:
        # There should only be one matching Sales Itemcode
        raise NameError('THERE IS MORE THAN 1 MATCHING SALES Item')
    elif len(salesitem) == 0:
        return None
    else:
        return salesitem[0]

def deletedsales():
    data = getdata(nb.sql.get_deleted_sales, '\"Missing Order Number\"')
    dc = DataContainer()
    for dltdsls in data:
        dc.addentry(dltdsls.WO_Num)
        dc.addentry(get_salesordercode(dltdsls.WO_Num))
        dc.addentry(dltdsls.UserID)
        dc.addentry(dltdsls.Reason)
        dc.addentry(dltdsls.LastUpdated)
        dc.addentry(dltdsls.RecordNumber)
        dc.addline()
    update(dc.datatable, 'deletedsales')

def despatch():
    data = getdata(nb.sql.get_despatch, '\"Sales Order Despatch\"')
    dc = DataContainer()
    for dsptch in data:
        dc.addentry(dsptch.WO_Num)
        dc.addentry(dsptch.Material)
        dc.addentry(get_materialcode(dsptch.Material))
        dc.addentry(get_salesitemcode(dsptch.WO_Num, dsptch.Material))
        dc.addentry(dsptch.BatchDespatched)
        dc.addentry(dsptch.DespatchedQuantity)
        dc.addentry(dsptch.LastUpdated)
        dc.addentry(dsptch.RecordNumber)
        dc.addline()
    update(dc.datatable, 'despatch')

def stockusage():
    data = getdata(nb.sql.get_stockusage, '\"Formula Stock Usage\"')
    dc = DataContainer()
    for stckusg in data:
        dc.addentry(get_stockcode(stckusg.Batch))
        dc.addentry(stckusg.Action)
        dc.addentry(get_customercode(stckusg.Customer))
        materialcode = get_materialcode(stckusg.Material)
        dc.addentry(get_salesitemcode(stckusg.WO_Num, materialcode))
        dc.addentry(stckusg.Price)
        dc.addentry(stckusg.UsageRef)
        dc.addentry(stckusg.Quantity)
        dc.addentry(stckusg.ItemOrder)
        dc.addentry(stckusg.UserID)
        dc.addentry(stckusg.LastUpdated)
        dc.addentry(stckusg.RecordNumber)
        dc.addline()
    update(dc.datatable, 'stockmovement')

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
    formulastock()
    sales()
    salesitem()
    deletedsales()
    despatch()
    stockusage()