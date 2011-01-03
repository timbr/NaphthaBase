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

    class qrcontainer(object):
        pass

    def create_memory_table(self, table, fields = ''):
        if fields == '':
            fields = '*'
            self.columns = self.naphthabase.get_columns(table)
        else:
            self.columns = list(fields)
            #fields = ('%s,' * len(fields)).strip(',') % fields
            fields = ','.join(fields)
        self.pos = {}
        for f in self.columns:
            self.pos[f] = self.columns.index(f)
        alldata = self.naphthabase.query("select %s from %s" % (fields, table))
        self.memorydata = []
        for row in alldata:
            line = self.qrcontainer()
            for col in self.columns:
               line.__dict__[col] = row[self.pos[col]]
            self.memorydata.append(line)
    
    def get_id(self, reply = 'id', **kwargs):
        clmns = kwargs.keys()
        col_a = clmns[0]
        value_a = kwargs[col_a]
        if len(clmns) == 2:
            col_b = clmns[1]
            value_b = kwargs[col_b]
        else:
            col_b = 'dummy'
            value_b = ''
        results = []
        for line in self.memorydata:
            linedata = line.__dict__
            if col_b == 'dummy':
                linedata[col_b] = ''
            if linedata[col_a] == value_a and linedata[col_b] == value_b:
                results.append(line.__dict__)
                # use line.__dict__ rather than linedata to avoid having 'dummy' and '' included
        if len(results) > 1:
            if not self.duplicates(results):
                raise NameError('MORE THAN ONE MATCHING REFERENCE FOUND')
        elif len(results) == 0:
            return None
        else:
            return results[0][reply]

    def duplicates(self, results):
        # More than one matching reference has been found
        dataset = set()
        for result in results:
            print 'duplicates:', result
            for field in result.keys():
               if field != 'id':
                   # we want to ignore the id field as we know this will be different
                   dataset.add(result[field])
        print 'dataset: ', dataset
        if len(dataset) != len(result.keys()) - 1:
            if self.excluded(results):
                return True # we're going to ignore this one....
            else:
                return False # the entries are different
        else:
            return True # they are exact copies

    def excluded(self, results):
        return False


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


#////////////////////////////////////////////////////////////////////////////#
class Depot(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self, customer, supplier):
        self.r_and_r_sql = nb.sql.get_depot
        self.r_and_r_table = 'accounts_Depot'
        DataTransferObject.__init__(self)
        for dpt in self.data:
            self.dc.addentry(dpt.ClientID)
            self.dc.addentry(dpt.Name)
            address = self.dc.combine(dpt.Address1,
                                      dpt.Address2,
                                      dpt.Address3,
                                      dpt.Address4,
                                      dpt.Address5)
            self.dc.addentry(address)
            self.dc.addentry(dpt.PostCode)
            self.dc.addentry(dpt.Telephone)
            self.dc.addentry(dpt.Fax)
            self.dc.addentry(dpt.Email)
            self.dc.addentry(dpt.Comment)
            self.dc.addentry(customer.qr.get_id(customer_code = dpt.ClientID))
            self.dc.addentry(supplier.qr.get_id(supplier_code = dpt.ClientID))
            self.dc.addentry(dpt.LastUpdated)
            self.dc.addentry(dpt.RecordNumber)
            self.dc.addline()
        self.update(self.dc.datatable, 'depot') 


#////////////////////////////////////////////////////////////////////////////#
class PurchaseOrder(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self, supplier):
        self.r_and_r_sql = nb.sql.get_purchaseorder
        self.r_and_r_table = 'stock_Purchase Order'
        DataTransferObject.__init__(self)
        for prchse in self.data:
            self.dc.addentry(prchse.PO_Num)
            self.dc.addentry(prchse.OrderValue)
            self.dc.addentry(supplier.qr.get_id(supplier_code = prchse.Supplier))
            self.dc.addentry(prchse.OrderReference)
            self.dc.addentry(prchse.OrderDate)
            self.dc.addentry(prchse.PlacedBy)
            self.dc.addentry(prchse.PrintedComment)
            self.dc.addentry(prchse.DeliveryComment)
            self.dc.addentry(prchse.Status)
            self.dc.addentry(prchse.LastUpdated)
            self.dc.addentry(prchse.RecordNumber)
            self.dc.addline()
        self.update(self.dc.datatable, 'purchaseorder') 
        self.qr = self.QR('purchaseorder', ('id', 'pon'))
        
    class QR(QuickReference):
        def __init__(self, table = '', fields = ''):
            QuickReference.__init__(self, table, fields)


#////////////////////////////////////////////////////////////////////////////#
class PurchaseItem(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self, purchaseorder, material):
        self.r_and_r_sql = nb.sql.get_purchaseitem
        self.r_and_r_table = 'stock_Purchase Item'
        DataTransferObject.__init__(self)
        for itm in self.data:
            self.dc.addentry(itm.PO_Num)
            self.dc.addentry(purchaseorder.qr.get_id(pon = itm.PO_Num))
            self.dc.addentry(material.qr.get_id(code = itm.Material))
            self.dc.addentry(itm.Quantity)
            self.dc.addentry(itm.Price)
            self.dc.addentry(itm.DueDate)
            self.dc.addentry(itm.DeliveredQuantity)
            self.dc.addentry(itm.LastUpdated)
            self.dc.addentry(itm.RecordNumber)
            self.dc.addline()
        self.update(self.dc.datatable, 'purchaseitem') 
        self.qr = self.QR('purchaseitem', ('id', 'pon', 'material_id'))
        
    class QR(QuickReference):
        def __init__(self, table = '', fields = ''):
            QuickReference.__init__(self, table, fields)


#////////////////////////////////////////////////////////////////////////////#
class Stock(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self, material, supplier, purchaseitem):
        self.r_and_r_sql = nb.sql.get_stock
        self.r_and_r_table = 'stock_Formula Stock'
        DataTransferObject.__init__(self)
        for stck in self.data:
            self.dc.addentry(stck.Batch)
            self.dc.addentry(material.qr.get_id(code = stck.Material))
            self.dc.addentry(stck.StockInfo)
            self.dc.addentry(stck.BatchStatus)
            self.dc.addentry(supplier.qr.get_id(supplier_code = stck.Supplier))
            self.dc.addentry(purchaseitem.qr.get_id(pon = stck.PO_Num, \
                                                    material_id = stck.Material))
            self.dc.addentry(stck.PurchaseCost)
            self.dc.addentry(stck.OriginalDeliveredQuantity)
            self.dc.addentry(stck.BatchUp_Date)
            self.dc.addentry(stck.QuantityNow)
            self.dc.addentry(stck.LastUpdated)
            self.dc.addentry(stck.RecordNumber)
            self.dc.addline()
        self.update(self.dc.datatable, 'stock') 
        self.qr = self.QR('stock', ('id', 'batch', 'status', 'lastupdated'))
        
    class QR(QuickReference):
        def __init__(self, table = '', fields = ''):
            QuickReference.__init__(self, table, fields)

        def excluded(self, results):
        # There are two entries for batch 15381 that are not duplicates.
        # This method will allow this to pass. Only one entry is used.
            if results[0]['batch'] in ['15381']:
                print 'Excluding batch 15381'
                return True
            else:
                return False
            


#////////////////////////////////////////////////////////////////////////////#
class SalesOrder(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self, customer, carrier):
        self.r_and_r_sql = nb.sql.get_salesorder
        self.r_and_r_table = 'stock_Sales Order'
        DataTransferObject.__init__(self)
        for sls in self.data:
            self.dc.addentry(sls.WO_Num)
            self.dc.addentry(sls.Link)
            self.dc.addentry(customer.qr.get_id(customer_code = sls.CustomerKey))
            self.dc.addentry(sls.CustomerOrderNumber)
            self.dc.addentry(sls.DespatchNotes)
            self.dc.addentry(sls.OrderValue)
            self.dc.addentry(sls.Status)
            self.dc.addentry(sls.OrderDate)
            self.dc.addentry(sls.DespatchDate)
            self.dc.addentry(sls.InvoiceDate)
            self.dc.addentry(sls.Operator)
            self.dc.addentry(sls.DespatchCompanyName)
            address = self.dc.combine(sls.DespatchAddress1,
                                      sls.DespatchAddress2,
                                      sls.DespatchAddress3,
                                      sls.DespatchAddress4)
            self.dc.addentry(address)
            self.dc.addentry(sls.DespatchPostCode)
            delnotecomment = self.dc.combine(sls.DeliveryNoteComment1,
                                             sls.DeliveryNoteComment2,
                                             sls.DeliveryNoteComment3,
                                             sls.DeliveryNoteComment4,
                                             sls.DeliveryNoteComment5,
                                             filter = '')
            self.dc.addentry(delnotecomment)
            invoicecomment = self.dc.combine(sls.InvoiceComment1,
                                             sls.InvoiceComment2,
                                             sls.InvoiceComment3,
                                             sls.InvoiceComment4,
                                             sls.InvoiceComment5,
                                             sls.InvoiceComment6,
                                             filter = '')
            self.dc.addentry(invoicecomment)
            self.dc.addentry(sls.InvoiceTerms)
            self.dc.addentry(sls.ItemCount)
            self.dc.addentry(carrier.qr.get_id(won = sls.WO_Num))
            self.dc.addentry(sls.LastUpdated)
            self.dc.addentry(sls.RecordNumber)
            self.dc.addline()
        self.update(self.dc.datatable, 'salesorder') 
        self.qr = self.QR('salesorder', ('id', 'won'))
        
    class QR(QuickReference):
        def __init__(self, table = '', fields = ''):
            QuickReference.__init__(self, table, fields)


#////////////////////////////////////////////////////////////////////////////#
class SalesItem(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self, purchaseorder, material):
        self.r_and_r_sql = nb.sql.get_salesitem
        self.r_and_r_table = 'stock_Sales Order Item'
        DataTransferObject.__init__(self)
        for itm in self.data:
            self.dc.addentry(itm.WO_Num)
            self.dc.addentry(salesorder.qr.get_id(won = itm.WO_Num))
            self.dc.addentry(material.qr.get_id(code = itm.Material))
            self.dc.addentry(itm.OrderQuantity)
            self.dc.addentry(itm.Price)
            self.dc.addentry(itm.RequiredDate)
            self.dc.addentry(itm.LastUpdated)
            self.dc.addentry(itm.RecordNumber)
            self.dc.addline()
        self.update(self.dc.datatable, 'salesitem') 
        self.qr = self.QR('salesitem', ('id', 'won', 'material_id'))
        
    class QR(QuickReference):
        def __init__(self, table = '', fields = ''):
            QuickReference.__init__(self, table, fields)


#////////////////////////////////////////////////////////////////////////////#
class DeletedSales(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self, salesorder):
        self.r_and_r_sql = nb.sql.get_deleted_sales
        self.r_and_r_table = 'stock_Missing Order Number'
        DataTransferObject.__init__(self)
        for dltdsls in self.data:
            self.dc.addentry(dltdsls.WO_Num)
            self.dc.addentry(salesorder.qr.get_id(won = dltdsls.WO_Num))
            self.dc.addentry(dltdsls.UserID)
            self.dc.addentry(dltdsls.Reason)
            self.dc.addentry(dltdsls.LastUpdated)
            self.dc.addentry(dltdsls.RecordNumber)
            self.dc.addline()
        self.update(self.dc.datatable, 'deletedsales')


#////////////////////////////////////////////////////////////////////////////#
class Despatch(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self, material, salesitem):
        self.r_and_r_sql = nb.sql.get_despatch
        self.r_and_r_table = 'stock_Sales Order Despatch'
        DataTransferObject.__init__(self)
        for dsptch in self.data:
            self.dc.addentry(dsptch.WO_Num)
            self.dc.addentry(dsptch.Material)
            self.dc.addentry(material.qr.get_id(code = dsptch.Material))
            self.dc.addentry(salesitem.qr.get_id(won = dsptch.WO_Num, material_id = dsptch.Material))
            self.dc.addentry(dsptch.BatchDespatched)
            self.dc.addentry(dsptch.DespatchedQuantity)
            self.dc.addentry(dsptch.LastUpdated)
            self.dc.addentry(dsptch.RecordNumber)
            self.dc.addline()
        self.update(self.dc.datatable, 'despatch')


#////////////////////////////////////////////////////////////////////////////#
class StockUsage(DataTransferObject):
#////////////////////////////////////////////////////////////////////////////#
    def __init__(self, stock, customer, material, saleitem):
        self.r_and_r_sql = nb.sql.get_stockusage
        self.r_and_r_table = 'stock_Formula Stock Usage'
        DataTransferObject.__init__(self)
        for stckusg in self.data:
            self.dc.addentry(stock.qr.get_id(batch = stckusg.Batch))
            self.dc.addentry(stckusg.Action)
            self.dc.addentry(customer.qr.get_id(customer_code = stckusg.Customer))
            materialcode = material.qr.get_id(code = stckusg.Material)
            self.dc.addentry(salesitem.qr.get_id(won = stckusg.WO_Num, material_id = materialcode))
            self.dc.addentry(stckusg.Price)
            self.dc.addentry(stckusg.UsageRef)
            self.dc.addentry(stckusg.Quantity)
            self.dc.addentry(stckusg.ItemOrder)
            self.dc.addentry(stckusg.UserID)
            self.dc.addentry(stckusg.LastUpdated)
            self.dc.addentry(stckusg.RecordNumber)
            self.dc.addline()
        self.update(self.dc.datatable, 'stockmovement')



if __name__ == '__main__':
    material = Material()
    hauliers = Hauliers()
    carrier = Carrier()
    customer = Customer()
    supplier = Supplier()
    contact = Contact(customer, supplier)
    depot = Depot(customer, supplier)
    purchaseorder = PurchaseOrder(supplier)
    purchaseitem = PurchaseItem(purchaseorder, material)
    stock = Stock(material, supplier, purchaseitem)
    salesorder = SalesOrder(customer, carrier)
    salesitem = SalesItem(salesorder, material)
    deletedsales = DeletedSales(salesorder)
    despatch = Despatch(material, salesitem)
    stockusage = StockUsage(stock, customer, material, salesitem)