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

def get_materialcode(materialid):
    materialcode = [data[1] for data in materialdata if data[0] == materialid]
    if len(materialcode) > 1:
        # There should only be one matching material code
        raise NameError('THERE IS MORE THAN 1 MATCHING MATERIAL')
    elif len(materialcode) == 0:
        return None
    else:
        return materialcode[0]

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