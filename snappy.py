import naphthabase as nb
from update import *
import datetime
import decimal

rrdata = nb.RandRDatabase()
nbdb = loadSession()
Base.metadata.create_all()

def get_customer_id(clientid):
    customer = nbdb.query(Customer).filter(Customer.customer_code == clientid).all()
    if len(customer) == 1:
        customerid = customer[0].id
    else:
        customerid = None
    return customerid

def get_supplier_id(clientid):
    supplier = nbdb.query(Supplier).filter(Supplier.supplier_code == clientid).all()
    if len(supplier) == 1:
        supplierid = supplier[0].id
    else:
        supplierid = None
    return supplierid


material = {'rrtable' : 'stock_Formula',
            'rrsql'   : nb.sql.get_material_codes,
            'nbtable' : 'Material',
            'Map' :
            {
            'code'        :  'Material',
            'description' :  'Description',
            'lastupdated' :  'LastUpdated',
            'rr_recordno' :  'RecordNumber'
            }
            }

hauliers = {'rrtable' : 'stock_Additional Items',
            'rrsql'   : nb.sql.get_hauliers,
            'nbtable' : 'Hauliers',
            'Map' :
            {
            'haulierkey'  :  'HaulierKey',
            'name'        :  'Name',
            'nominalcode' : 'NominalCode',
            'lastupdated' :  'LastUpdated',
            'rr_recordno' :  'RecordNumber'
            }
            }

carrier  = {'rrtable' : 'stock_Sales Order Additional',
            'rrsql'   : nb.sql.get_carrier,
            'nbtable' : 'Carrier',
            'Map' :
            {
            'won'         :  'WO_Num',
            'description' :  'Description',
            'lastupdated' :  'LastUpdated',
            'rr_recordno' :  'RecordNumber'
            }
            }
            
          
customer = {'rrtable' : 'accounts_Customer',
            'rrsql'   : nb.sql.get_customer,
            'nbtable' : 'Customer',
            'Map' :
            {
            'customer_code' :  'CustomerID',
            'name'          :  'Name',
            'address'       :  ['Address1',
                               'Address2',
                               'Address3',
                               'Address4',
                               'Address5'],
            'postcode'      :  'PostCode',
            'phone'         :  'Telephone',
            'fax'           :  'Fax',
            'email'         :  'Email',
            'website'       :  'Website',
            'contactname'   :  'ContactName',
            'vat'           :  'VAT',
            'comment'       :  'Comment',
            'memo'          :  'Memo',
            'creditlimit'   :  'CreditLimit',
            'terms'         :  'Terms',
            'lastupdated'   :  'LastUpdated',
            'rr_recordno'   :  'RecordNumber'
            }
            }

supplier = {'rrtable' : 'accounts_Supplier',
            'rrsql'   : nb.sql.get_supplier,
            'nbtable' : 'Supplier',
            'Map' :
            {
            'supplier_code' :  'SupplierID',
            'name'          :  'Name',
            'address'       :  ['Address1',
                               'Address2',
                               'Address3',
                               'Address4',
                               'Address5'],
            'postcode'      :  'PostCode',
            'phone'         :  'Telephone',
            'fax'           :  'Fax',
            'email'         :  'Email',
            'website'       :  'Website',
            'contactname'   :  'ContactName',
            'vat'           :  'VAT',
            'comment'       :  'Comment',
            'memo'          :  'Memo',
            'lastupdated'   :  'LastUpdated',
            'rr_recordno'   :  'RecordNumber'
            }
            }

contacts = {'rrtable' : 'accounts_Contact',
            'rrsql'   : nb.sql.get_contact,
            'nbtable' : 'Contact',
            'Map' :
            {
            'clientcode'    :  'ClientID',
            'title'         :  'Title',
            'forename'      :  'Forename',
            'surname'       :  'Surname',
            'phone'         :  'Phone',
            'department'    :  'Department',
            'customer_id'   :  {'func':
                              'get_customer_id(record.ClientID)'},
            'supplier_id'   :  {'func':
                              'get_supplier_id(record.ClientID)'},
            'lastupdated'   :  'LastUpdated',
            'rr_recordno'   :  'RecordNumber'
            }
            }

depot    = {'rrtable' : 'accounts_Depot',
            'rrsql'   : nb.sql.get_depot,
            'nbtable' : 'Depot',
            'Map' :
            {
            'clientid'      :  'ClientID',
            'clientname'    :  'Name',
            'address'       :  ['Address1',
                               'Address2',
                               'Address3',
                               'Address4',
                               'Address5'],
            'postcode'      :  'PostCode',
            'phone'         :  'Telephone',
            'fax'           :  'Fax',
            'email'         :  'Email',
            'comment'       :  'Comment',
            'customer_id'   :  {'func':
                              'get_customer_id(record.ClientID)'},
            'supplier_id'   :  {'func':
                              'get_supplier_id(record.ClientID)'},
            'lastupdated'   :  'LastUpdated',
            'rr_recordno'   :  'RecordNumber'
            }
            }
            
po_order = {'rrtable' : 'stock_Purchase Order',
            'rrsql'   : nb.sql.get_purchaseorder,
            'nbtable' : 'PurchaseOrder',
            'Map' :
            {
            'pon'           :  'PO_Num',
            'ordervalue'    :  'OrderValue',
            'supplier_id'   :  {'func':
                              'get_supplier_id(record.Supplier)'},
            'orderref'      :  'OrderReference',
            'orderdate'     :  'OrderDate',
            'placedby'      :  'PlacedBy',
            'printedcomment':  'PrintedComment',
            'deliverycomment': 'DeliveryComment',
            'status'        :  'Status',
            'lastupdated'   :  'LastUpdated',
            'rr_recordno'   :  'RecordNumber'
            }
            }
            
            
            
            

def map_and_update(table_mapping):
    """Maps the R&R database to the NaphthaBase
    
    The table_mapping dictionary describes how the NaphthaBase columns
    are mapped to the R&R database columns.
    This function gets the latest data from the R&R database and updates
    the NaphthaBase.
    """
    
    nbtable = eval(table_mapping['nbtable'])
    # This is the specified NaphthaBase table object, eg Material, Customer, Supplier etc.
    last_nb_record = nbdb.query(nbtable).order_by(desc(nbtable.lastupdated)). \
                                                                        first()
    if last_nb_record is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = last_nb_record.lastupdated
    # Finds the last updated record in the NaphthaBase and sets lastupdated variable to this date, or defaults to 1982.
    lastnb_records = set([i.rr_recordno for i in nbdb.query(nbtable).filter(nbtable.deleted == False)])
    # Creates a set of all Record Numbers in the Naphthabase table
    all_rr_data = rrdata.query(table_mapping['rrsql'], table_mapping['rrtable'])
    all_records = set([i.RecordNumber for i in all_rr_data])
    # Creates a set of all Record Numbers in the R&R database table
    newdata = rrdata.query(table_mapping['rrsql'], table_mapping['rrtable'], lastupdated)
    recentmods = set([i.RecordNumber for i in newdata])
    # Creates a set of all Record Numbers for entries in the R&R database table since the lastupdated date.
    
    new_records = recentmods.difference(lastnb_records)
    # Set of all new records in the R&R database table that aren't in the NaphthaBase table
    updated_records = recentmods.intersection(lastnb_records)
    # Set of records that exist in the NaphthaBase but need updating
    deletedrecords = lastnb_records.difference(all_records)
    # Set of records that have been deleted from the R&R database and need the deleted flag setting in the NaphthaBase
    
    map = table_mapping['Map']
    # This is the specific column mapping information.
    args = ['%s(id = None' % (table_mapping['nbtable'])]
    for column in map.keys():
        rrcolumn = map[column]
        if type(rrcolumn) is list:
            # All records in the list are combined into a single field before writing to the NaphthaBase
            start = '%s = combine(' % column
            middle = []
            for item in rrcolumn:
                middle.append('record.%s' % item)
                rrfield = start + ', '.join(middle) + ')'
            args.append(rrfield)
        elif type(rrcolumn) is dict:
            # The function specified in the dictionary needs to be executed to get the reference id.
            args.append('%s = %s' % (column, rrcolumn['func']))
        else:
            args.append('%s = record.%s' % (column, rrcolumn))
        
    args.append('deleted = False)')
    newinstruction = ', '.join(args)
    print newinstruction + '\n\n'
    
    args = ['%sHistory(id = None' % (table_mapping['nbtable'])]
    for column in map.keys():
        args.append('%s = lastrecord.%s' % (column, column))
    oldinstruction = ', '.join(args) + ')'
    print oldinstruction
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            newmat = eval(newinstruction)
            newmat.lastupdated = record.LastUpdated
            nbdb.add(newmat)
        elif record.RecordNumber in updated_records:
            lastrecord = nbdb.query(nbtable). \
             filter(nbtable.rr_recordno == record.RecordNo).all()[0]
            old = eval(oldinstruction)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = eval(newinstruction)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        recordtodelete = nbdb.query(nbtable). \
          filter(nbtable.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()
    
    


    




    
    
def update_purchaseitem():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(PurchaseItem). \
                            order_by(desc(PurchaseItem.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(PurchaseItem).filter(PurchaseItem.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_purchaseitem,                           'stock_Purchase Item')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_purchaseitem,                           'stock_Purchase Item', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            po = nbdb.query(PurchaseOrder).filter(PurchaseOrder.pon == record.PO_Num).all()
            if len(po) == 1:
                poid = po[0].id
            else:
                poid = None
            mat = nbdb.query(Material).filter(Material.code == record.Material).all()
            if len(mat) == 1:
                matid = mat[0].id
            else:
                matid = None
            newpi = PurchaseItem(id = None,
                        pon = record.PO_Num,
                        itemno = record.Index,
                        purchaseorder_id = poid,
                        material_id = matid,
                        quantity = record.Quantity,
                        price = record.Price,
                        duedate = record.DueDate,
                        delivered_quantity = record.DeliveredQuantity,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newpi.lastupdated = record.LastUpdated
            nbdb.add(newpi)
        elif record.RecordNumber in updated_records:
            po = nbdb.query(PurchaseOrder).filter(PurchaseOrder.pon == record.PO_Num).all()
            if len(po) == 1:
                poid = po[0].id
            else:
                poid = None
            mat = nbdb.query(Material).filter(Material.code == record.Material).all()
            if len(mat) == 1:
                matid = mat[0].id
            else:
                matid = None
                
            lastrecord = nbdb.query(PurchaseItem). \
             filter(PurchaseItem.rr_recordno == record.RecordNumber).all()[0]
            old = PurchaseItemHistory(id = None,
                        pi_id = lastrecord.id,
                        pon = lastrecord.pon,
                        itemno = lastrecord.itemno,
                        purchaseorder_id = lastrecord.purchaseorder_id,
                        material_id = lastrecord.material_id,
                        quantity = lastrecord.quantity,
                        price = lastrecord.price,
                        duedate = lastrecord.duedate,
                        delivered_quantity = lastrecord.delivered_quantity,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = PurchaseItem(id = None,
                        pon = record.PO_Num,
                        itemno = record.Index,
                        purchaseorder_id = poid,
                        material_id = matid,
                        quantity = record.Quantity,
                        price = record.Price,
                        duedate = record.DueDate,
                        delivered_quantity = record.DeliveredQuantity,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        print record
        recordtodelete = nbdb.query(PurchaseItem). \
          filter(PurchaseItem.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()


def update_stock():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(Stock). \
                            order_by(desc(Stock.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(Stock).filter(Stock.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_stock,                           'stock_Formula Stock')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_stock,                           'stock_Formula Stock', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    query = """
    Select Batch, \"Item Order\" AS ItemOrder from \"Formula Stock Usage\"
    where \"Record Type\" = 'P' or \"Record Type\" = ?
    """
    po_items = rrdata.simplequery(query, 'G')
    global po_item_num
    po_item_num = {}
    for item in po_items:
        if item.Batch == '15381':
            itemnum = None
        else:
            itemnum = item.ItemOrder
        po_item_num[item.Batch] = itemnum
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            pi = nbdb.query(PurchaseItem).filter(PurchaseItem.pon == record.PO_Num).filter(PurchaseItem.itemno == po_item_num.get(record.Batch, None)).all()
            if len(pi) == 1:
                piid = pi[0].id
            else:
                piid = None
            mat = nbdb.query(Material).filter(Material.code == record.Material).all()
            if len(mat) == 1:
                matid = mat[0].id
            else:
                matid = None
            supplier = nbdb.query(Supplier).filter(Supplier.supplier_code == record.Supplier).all()
            if len(supplier) == 1:
                supplierid = supplier[0].id
            else:
                supplierid = None
            newstock = Stock(id = None,
                        batch = record.Batch,
                        material_id = matid,
                        stockinfo = record.StockInfo,
                        status = record.BatchStatus,
                        supplier_id = supplierid,
                        purchaseitem_id = piid,
                        costprice = record.PurchaseCost,
                        batchup_quantity = record.OriginalDeliveredQuantity,
                        batchup_date = record.BatchUp_Date,
                        stockquantity = record.QuantityNow,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newstock.lastupdated = record.LastUpdated
            nbdb.add(newstock)
        elif record.RecordNumber in updated_records:
            pi = nbdb.query(PurchaseItem).filter(PurchaseItem.pon == record.PO_Num).filter(PurchaseItem.itemno == po_item_num.get(record.Batch, None)).all()
            if len(pi) == 1:
                piid = pi[0].id
            else:
                piid = None
            mat = nbdb.query(Material).filter(Material.code == record.Material).all()
            if len(mat) == 1:
                matid = mat[0].id
            else:
                matid = None
            supplier = nbdb.query(Supplier).filter(Supplier.supplier_code == record.Supplier).all()
            if len(supplier) == 1:
                supplierid = supplier[0].id
            else:
                supplierid = None
                
            lastrecord = nbdb.query(Stock). \
             filter(Stock.rr_recordno == record.RecordNumber).all()[0]
            old = StockHistory(id = None,
                        stock_id = lastrecord.id,
                        batch = lastrecord.batch,
                        material_id = lastrecord.material_id,
                        stockinfo = lastrecord.stockinfo,
                        status = lastrecord.status,
                        supplier_id = lastrecord.supplier_id,
                        purchaseitem_id = lastrecord.purchaseitem_id,
                        costprice = lastrecord.costprice,
                        batchup_quantity = lastrecord.batchup_quantity,
                        batchup_date = lastrecord.batchup_date,
                        stockquantity = lastrecord.stockquantity,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = Stock(id = None,
                        batch = record.Batch,
                        material_id = matid,
                        stockinfo = record.StockInfo,
                        status = record.BatchStatus,
                        supplier_id = supplierid,
                        purchaseitem_id = piid,
                        costprice = record.PurchaseCost,
                        batchup_quantity = record.OriginalDeliveredQuantity,
                        batchup_date = record.BatchUp_Date,
                        stockquantity = record.QuantityNow,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        print record
        recordtodelete = nbdb.query(Stock). \
          filter(Stock.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()
    
    
    
def update_salesorder():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(SalesOrder). \
                            order_by(desc(SalesOrder.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(SalesOrder).filter(SalesOrder.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_salesorder,                           'stock_Sales Order')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_salesorder,                           'stock_Sales Order', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            customer = nbdb.query(Customer).filter(Customer.customer_code == record.CustomerKey).all()
            if len(customer) == 1:
                customerid = customer[0].id
            else:
                customerid = None
            carrier = nbdb.query(Carrier).filter(Carrier.won == record.WO_Num).all()
            if len(carrier) == 1:
                carrierid = carrier[0].id
            elif len(carrier) > 1:
                print 'ARRGGGHH', carrier
            else:
                carrierid = None
            newso = SalesOrder(id = None,
                        won = record.WO_Num,
                        followon_link = record.Link,
                        customer_id = customerid,
                        customer_orderno = record.CustomerOrderNumber,
                        picklist_comment = record.DespatchNotes,
                        ordervalue = record.OrderValue,
                        status = record.Status,
                        orderdate = record.OrderDate,
                        despatchdate = record.DespatchDate,
                        invoicedate = record.InvoiceDate,
                        operator = record.Operator,
                        delivery_name = record.DespatchCompanyName,
                        delivery_address = combine(record.DespatchAddress1,
                                          record.DespatchAddress2,
                                          record.DespatchAddress3,
                                          record.DespatchAddress4),
                        delivery_postcode = record.DespatchPostCode,
                        printed_comments = combine(record.DeliveryNoteComment1,
                                                   record.DeliveryNoteComment2,
                                                   record.DeliveryNoteComment3,
                                                   record.DeliveryNoteComment4,
                                                   record.DeliveryNoteComment5),
                        invoice_comments = combine(record.InvoiceComment1,
                                                   record.InvoiceComment2,
                                                   record.InvoiceComment3,
                                                   record.InvoiceComment4,
                                                   record.InvoiceComment5,
                                                   record.InvoiceComment6),
                        invoice_terms = record.InvoiceTerms,
                        item_count = record.ItemCount,
                        carrier_id = carrierid,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newso.lastupdated = record.LastUpdated
            nbdb.add(newso)
        elif record.RecordNumber in updated_records:
            customer = nbdb.query(Customer).filter(Customer.customer_code == record.CustomerKey).all()
            if len(customer) == 1:
                customerid = customer[0].id
            else:
                customerid = None
            carrier = nbdb.query(Carrier).filter(Carrier.won == record.WO_Num).all()
            if len(carrier) == 1:
                carrierid = carrier[0].id
            elif len(carrier) > 1:
                print 'ARRGGGHH', carrier
            else:
                carrierid = None
                
            lastrecord = nbdb.query(SalesOrder). \
             filter(SalesOrder.rr_recordno == record.RecordNumber).all()[0]
            old = SalesOrderHistory(id = None,
                        so_id = lastrecord.id,
                        won = lastrecord.won,
                        followon_link = lastrecord.followon_link,
                        customer_id = lastrecord.customer_id,
                        customer_orderno = lastrecord.customer_orderno,
                        picklist_comment = lastrecord.picklist_comment,
                        ordervalue = lastrecord.ordervalue,
                        status = lastrecord.status,
                        orderdate = lastrecord.orderdate,
                        despatchdate = lastrecord.despatchdate,
                        invoicedate = lastrecord.invoicedate,
                        operator = lastrecord.operator,
                        delivery_name = lastrecord.delivery_name,
                        delivery_address = lastrecord.delivery_address,
                        delivery_postcode = lastrecord.delivery_postcode,
                        printed_comments = lastrecord.printed_comments,
                        invoice_comments = lastrecord.invoice_comments,
                        invoice_terms = lastrecord.invoice_terms,
                        item_count = lastrecord.item_count,
                        carrier_id = lastrecord.carrier_id,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = SalesOrder(id = None,
                        won = record.WO_Num,
                        followon_link = record.Link,
                        customer_id = customerid,
                        customer_orderno = record.CustomerOrderNumber,
                        picklist_comment = record.DespatchNotes,
                        ordervalue = record.OrderValue,
                        status = record.Status,
                        orderdate = record.OrderDate,
                        despatchdate = record.DespatchDate,
                        invoicedate = record.InvoiceDate,
                        operator = record.Operator,
                        delivery_name = record.DespatchCompanyName,
                        delivery_address = combine(record.DespatchAddress1,
                                          record.DespatchAddress2,
                                          record.DespatchAddress3,
                                          record.DespatchAddress4),
                        delivery_postcode = record.DespatchPostCode,
                        printed_comments = combine(record.DeliveryNoteComment1,
                                                   record.DeliveryNoteComment2,
                                                   record.DeliveryNoteComment3,
                                                   record.DeliveryNoteComment4,
                                                   record.DeliveryNoteComment5),
                        invoice_comments = combine(record.InvoiceComment1,
                                                   record.InvoiceComment2,
                                                   record.InvoiceComment3,
                                                   record.InvoiceComment4,
                                                   record.InvoiceComment5,
                                                   record.InvoiceComment6),
                        invoice_terms = record.InvoiceTerms,
                        item_count = record.ItemCount,
                        carrier_id = carrierid,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        print record
        recordtodelete = nbdb.query(SalesOrder). \
          filter(SalesOrder.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()
    


def update_salesitem():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(SalesItem). \
                            order_by(desc(SalesItem.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(SalesItem).filter(SalesItem.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_salesitem,                           'stock_Sales Order Item')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_salesitem,                           'stock_Sales Order Item', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    global new_records
    global updated_records
    global deletedrecords
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber== '21781':
            print 'here', record.RecordNumber
        if record.RecordNumber in new_records:
            so = nbdb.query(SalesOrder).filter(SalesOrder.won == record.WO_Num).all()
            if len(so) == 1:
                soid = so[0].id
            else:
                soid = None
            mat = nbdb.query(Material).filter(Material.code == record.Material).all()
            if len(mat) == 1:
                matid = mat[0].id
            else:
                matid = None
            newsi = SalesItem(id = None,
                        won = record.WO_Num,
                        salesorder_id = soid,
                        material_id = matid,
                        quantity = record.OrderQuantity,
                        price = record.Price,
                        required_date = record.RequiredDate,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newsi.lastupdated = record.LastUpdated
            nbdb.add(newsi)
        elif record.WO_Num in updated_records:
            so = nbdb.query(SalesOrder).filter(SalesOrder.won == record.WO_Num).all()
            if len(so) == 1:
                soid = so[0].id
            else:
                soid = None
            mat = nbdb.query(Material).filter(Material.code == record.Material).all()
            if len(mat) == 1:
                matid = mat[0].id
            else:
                matid = None
                
            lastrecord = nbdb.query(SalesItem). \
             filter(SalesItem.rr_recordno == record.RecordNumber).all()[0]
            old = SalesItemHistory(id = None,
                        si_id = lastrecord.id,
                        won = lastrecord.won,
                        salesorder_id = lastrecord.salesorder_id,
                        material_id = lastrecord.material_id,
                        quantity = lastrecord.quantity,
                        price = lastrecord.price,
                        required_date = lastrecord.required_date,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = SalesItem(id = None,
                        won = record.WO_Num,
                        salesorder_id = soid,
                        material_id = matid,
                        quantity = record.OrderQuantity,
                        price = record.Price,
                        required_date = record.RequiredDate,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        print record
        recordtodelete = nbdb.query(SalesItem). \
          filter(SalesItem.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()    
    
    
def update_deletedsales():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(DeletedSales). \
                            order_by(desc(DeletedSales.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(DeletedSales).filter(DeletedSales.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_deleted_sales,                           'stock_Missing Order Number')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_deleted_sales,                           'stock_Missing Order Number', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            so = nbdb.query(SalesOrder).filter(SalesOrder.won == record.WO_Num).all()
            if len(so) == 1:
                soid = so[0].id
            else:
                soid = None
            newds = DeletedSales(id = None,
                        won = record.WO_Num,
                        salesorder_id = soid,
                        operator = record.UserID,
                        reason = record.Reason,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newds.lastupdated = record.LastUpdated
            nbdb.add(newds)
        elif record.RecordNumber in updated_records:
            so = nbdb.query(SaleseOrder).filter(SalesOrder.won == record.WO_Num).all()
            if len(so) == 1:
                soid = so[0].id
            else:
                soid = None
                
            lastrecord = nbdb.query(DeletedSales). \
             filter(DeletedSales.rr_recordno == record.RecordNumber).all()[0]
            old = DeletedSalesHistory(id = None,
                        ds_id = lastrecord.id,
                        won = lastrecord.won,
                        salesorder_id = lastrecord.salesorder_id,
                        operator = lastrecord.operator,
                        reason = lastrecord.reason,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = DeletedSales(id = None,
                        won = record.WO_Num,
                        salesorder_id = soid,
                        operator = record.UserID,
                        reason = record.Reason,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        print record
        recordtodelete = nbdb.query(DeletedSales). \
          filter(DeletedSales.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()  

    
def update_despatch():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(Despatch). \
                            order_by(desc(Despatch.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(Despatch).filter(Despatch.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_despatch,                           'stock_Sales Order Despatch')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_despatch,                           'stock_Sales Order Despatch', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            stock = nbdb.query(Stock).filter(Stock.batch == record.BatchDespatched).all()
            if len(stock) == 1:
                stockid = stock[0].id
            elif len(stock) > 1:
                print "UURRGHHH!!", stock
            else:
                stockid = None
            mat = nbdb.query(Material).filter(Material.code == record.Material).all()
            if len(mat) == 1:          
                salesitem = nbdb.query(SalesItem).filter(SalesItem.won == record.WO_Num).filter(SalesItem.deleted == False).filter(SalesItem.material_id == mat[0].id).all()
                if len(salesitem) == 1:
                    salesitemid = salesitem[0].id
                elif len(salesitem) > 1:
                    print "UURRGHHH!!", salesitem
                else:
                    salesitemid = None
            else:
                salesitemid = None
            newdsptch = Despatch(id = None,
                        won = record.WO_Num,
                        materialcode = record.Material,
                        stock_id = stockid,
                        salesitem_id = salesitemid,
                        batch = record.BatchDespatched,
                        quantity = record.DespatchedQuantity,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newdsptch.lastupdated = record.LastUpdated
            nbdb.add(newdsptch)
        elif record.RecordNumber in updated_records:
            stock = nbdb.query(Stock).filter(Stock.batch == record.BatchDespatched).all()
            if len(stock) == 1:
                stockid = stock[0].id
            elif len(stock) > 1:
                print "UURRGHHH!!", stock
            else:
                stockid = None
            mat = nbdb.query(Material).filter(Material.code == record.Material).all()
            if len(mat) == 1:          
                salesitem = nbdb.query(SalesItem).filter(SalesItem.won == record.WO_Num).filter(SalesItem.deleted == False).filter(SalesItem.material_id == mat[0].id).all()
                if len(salesitem) == 1:
                    salesitemid = salesitem[0].id
                elif len(salesitem) > 1:
                    print "UURRGHHH!!", stock
                else:
                    salesitemid = None
            else:
                salesitemid = None
                
            lastrecord = nbdb.query(Despatch). \
             filter(Despatch.rr_recordno == record.RecordNumber).all()[0]
            old = DespatchHistory(id = None,
                        desp_id = lastrecord.id,
                        won = lastrecord.won,
                        materialcode = lastrecord.materialcode,
                        stock_id = lastrecord.stock_id,
                        salesitem_id = lastrecord.salesitem_id,
                        batch = lastrecord.batch,
                        quantity = lastrecord.quantity,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = Despatch(id = None,
                        won = record.WO_Num,
                        materialcode = record.Material,
                        stock_id = stockid,
                        salesitem_id = salesitemid,
                        batch = record.BatchDespatched,
                        quantity = record.DespatchedQuantity,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        print record
        recordtodelete = nbdb.query(Depatch). \
          filter(Despatch.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()
    
    
def update_stockmovement():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(StockMovement). \
                            order_by(desc(StockMovement.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(StockMovement).filter(StockMovement.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_stockusage,                           'stock_Formula Stock Usage')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_stockusage,                           'stock_Formula Stock Usage', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            stock = nbdb.query(Stock).filter(Stock.batch == record.Batch).all()
            if len(stock) == 1:
                stockid = stock[0].id
            elif len(stock) > 1:
                print "UURRGHHH!!", stock
            else:
                stockid = None
            customer = nbdb.query(Customer).filter(Customer.customer_code == record.Customer).all()
            if len(customer) == 1:
                customerid = customer[0].id
            else:
                customerid = None
            mat = nbdb.query(Material).filter(Material.code == record.Material).all()
            if len(mat) == 1:          
                salesitem = nbdb.query(SalesItem).filter(SalesItem.won == record.WO_Num).filter(SalesItem.deleted == False).filter(SalesItem.material_id == mat[0].id).all()
                if len(salesitem) == 1:
                    salesitemid = salesitem[0].id
                elif len(salesitem) > 1:
                    print "UURRGHHH!!", stock
                else:
                    salesitemid = None
            else:
                salesitemid = None
            newstockusage = StockMovement(id = None,
                        stock_id = stockid,
                        action = record.Action,
                        customer_id = customerid,
                        salesitem_id = salesitemid,
                        salesprice = record.Price,
                        pon = record.PO_Num,
                        movement_description = record.UsageRef,
                        movement_quantity = record.Quantity,
                        item_order = record.ItemOrder,
                        user_id = record.UserID,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newstockusage.lastupdated = record.LastUpdated
            nbdb.add(newstockusage)
        elif record.RecordNumber in updated_records:
            stock = nbdb.query(Stock).filter(Stock.batch == record.Batch).all()
            if len(stock) == 1:
                stockid = stock[0].id
            elif len(stock) > 1:
                print "UURRGHHH!!", stock
            else:
                stockid = None
            customer = nbdb.query(Customer).filter(Customer.customer_code == record.Customer).all()
            if len(customer) == 1:
                customerid = customer[0].id
            else:
                customerid = None
            mat = nbdb.query(Material).filter(Material.code == record.Material).all()
            if len(mat) == 1:          
                salesitem = nbdb.query(SalesItem).filter(SalesItem.won == record.WO_Num).filter(SalesItem.deleted == False).filter(SalesItem.material_id == mat[0].id).all()
                if len(salesitem) == 1:
                    salesitemid = salesitem[0].id
                elif len(salesitem) > 1:
                    print "UURRGHHH!!", stock
                else:
                    salesitemid = None
            else:
                salesitemid = None
                
            lastrecord = nbdb.query(StockMovement). \
             filter(StockMovement.rr_recordno == record.RecordNumber).all()[0]
            old = StockMovementHistory(id = None,
                        sm_id = lastrecord.id,
                        stock_id = lastrecord.stock_id,
                        action = lastrecord.action,
                        customer_id = lastrecord.customer_id,
                        salesitem_id = lastrecord.salesitem_id,
                        salesprice = lastrecord.salesprice,
                        pon = lastrecord.pon,
                        movement_description = lastrecord.movement_description,
                        movement_quantity = lastrecord.movement_quantity,
                        item_order = lastrecord.item_order,
                        user_id = lastrecord.user_id,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = StockMovement(id = None,
                        stock_id = stockid,
                        action = record.Action,
                        customer_id = customerid,
                        salesitem_id = salesitemid,
                        salesprice = record.Price,
                        pon = record.PO_Num,
                        movement_description = record.UsageRef,
                        movement_quantity = record.Quantity,
                        item_order = record.ItemOrder,
                        user_id = record.UserID,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        print record
        recordtodelete = nbdb.query(StockMovement). \
          filter(StockMovement.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()    
    
    

def sanitise(record):
    cont = container()
    columns = [item[0] for item in record.cursor_description]
    for column in columns:
        data = record.__getattribute__(column)
        if type(data) is decimal.Decimal:
            cont.__dict__[column] = str(data)
        elif type(data) is str:
            text = record.__getattribute__(column)
            cont.__dict__[column] = text.replace('\xa3', '&POUND').replace('\xd9', '')
        else:
            cont.__dict__[column] = data
    return cont
    


    

def combine(*args, **kwargs):
    """Combines several dataitems into a single string.
        
    By default, commas are removed from the end of dataitems. The optional
    filter argument can be used to specify other characters to strip.
    By default, a newline character is added to the end of each dataitem
    (apart from the last). The optional separator argument can be used to
    specify other end of line characters.
    """
        
    filter = kwargs.get('filter', ',')
    separator = kwargs.get('separator', '\n')
    output = []
    for line in args:
        output.append(line.strip(filter))
    output = separator.join(output)
    # No new-line character wanted at the end.
    return output

    
class container(object):
    def __repr__(self):
        contents = self.__dict__.values()
        answer = [str(thing) for thing in contents]
        return '<Record: ' + ', '.join(answer) + '>'
        

if __name__ == '__main__':
    update_material()
    update_hauliers()
    update_carrier()
    update_customer()
    update_supplier()
    update_contacts()
    update_depot()
    update_purchaseorder()
    update_purchaseitem()
    update_stock()
    update_salesorder()
    update_salesitem()
    update_deletedsales()
    update_despatch()
    update_stockmovement()