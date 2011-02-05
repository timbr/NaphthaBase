import naphthabase as nb
from update import *
import datetime
import decimal

rrdata = nb.RandRDatabase()
nbdb = loadSession()
Base.metadata.create_all()

def update_material():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(Material). \
                            order_by(desc(Material.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(Material).filter(Material.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_material_codes,                           'stock_Formula')
    all_records = set([i.RecordNo for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_material_codes,                           'stock_Formula', lastupdated)
    
    recentmods = set([i.RecordNo for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNo in new_records:
            newmat = Material(id = None,
                        code = record.Material,
                        description = record.Description,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNo,
                        deleted = False)
            newmat.lastupdated = record.LastUpdated
            nbdb.add(newmat)
        elif record.RecordNo in updated_records:
            lastrecord = nbdb.query(Material). \
             filter(Material.rr_recordno == record.RecordNo).all()[0]
            old = MaterialHistory(id = None,
                        material_id = lastrecord.id,
                        code = lastrecord.code,
                        description = lastrecord.description,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = Material(id = None,
                        code = record.Material,
                        description = record.Description,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNo,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        recordtodelete = nbdb.query(Material). \
          filter(Material.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()

    

def update_hauliers():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(Hauliers). \
                            order_by(desc(Hauliers.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(Hauliers).filter(Hauliers.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_hauliers,                           'stock_Additional Items')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_hauliers,                           'stock_Additional Items', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            newhaul = Hauliers(id = None,
                        haulierkey = record.HaulierKey,
                        name = record.Name,
                        nominalcode = record.NominalCode,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newhaul.lastupdated = record.LastUpdated
            nbdb.add(newhaul)
        elif record.RecordNumber in updated_records:
            lastrecord = nbdb.query(Hauliers). \
             filter(Hauliers.rr_recordno == record.RecordNumber).all()[0]
            old = HauliersHistory(id = None,
                        hauliers_id = lastrecord.id,
                        haulierkey = lastrecord.haulierkey,
                        name = lastrecord.name,
                        nominalcode = lastrecord.nominalcode,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = Haulier(id = None,
                        haulierkey = record.HaulierKey,
                        name = record.Name,
                        nominalcode = record.NominalCode,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNo,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        recordtodelete = nbdb.query(Hauliers). \
          filter(Hauliers.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()
    
    
    
def update_carrier():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(Carrier). \
                            order_by(desc(Carrier.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(Carrier).filter(Carrier.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_carrier,                           'stock_Sales Order Additional')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_carrier,                           'stock_Sales Order Additional', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            newcarrier = Carrier(id = None,
                        won = record.WO_Num,
                        description = record.Description,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newcarrier.lastupdated = record.LastUpdated
            nbdb.add(newcarrier)
        elif record.RecordNumber in updated_records:
            lastrecord = nbdb.query(Carrier). \
             filter(Carrier.rr_recordno == record.RecordNumber).all()[0]
            old = CarrierHistory(id = None,
                        carrier_id = lastrecord.id,
                        won = lastrecord.won,
                        description = lastrecord.description,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = Carrier(id = None,
                        won = record.WO_Num,
                        description = record.Description,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNo,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        recordtodelete = nbdb.query(Carrier). \
          filter(Carrier.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()
    
    

def update_customer():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(Customer). \
                            order_by(desc(Customer.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(Customer).filter(Customer.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_customer,                           'accounts_Customer')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_customer,                           'accounts_Customer', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            newcustomer = Customer(id = None,
                        customer_code = record.CustomerID,
                        name = record.Name,
                        address = combine(record.Address1,
                                          record.Address2,
                                          record.Address3,
                                          record.Address4,
                                          record.Address5),
                        postcode = record.PostCode,
                        phone = record.Telephone,
                        fax = record.Fax,
                        email = record.Email,
                        website = record.Website,
                        contactname = record.ContactName,
                        vat = record.VAT,
                        comment = record.Comment,
                        memo = record.Memo,
                        creditlimit = record.CreditLimit,
                        terms = record.Terms,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newcustomer.lastupdated = record.LastUpdated
            nbdb.add(newcustomer)
        elif record.RecordNumber in updated_records:
            lastrecord = nbdb.query(Customer). \
             filter(Customer.rr_recordno == record.RecordNumber).all()[0]
            old = CustomerHistory(id = None,
                        customer_id = lastrecord.id,
                        customer_code = lastrecord.customer_code,
                        name = lastrecord.name,
                        address = lastrecord.address,
                        postcode = lastrecord.postcode,
                        phone = lastrecord.phone,
                        fax = lastrecord.fax,
                        email = lastrecord.email,
                        website = lastrecord.website,
                        contactname = lastrecord.contactname,
                        vat = lastrecord.vat,
                        comment = lastrecord.comment,
                        memo = lastrecord.memo,
                        creditlimit = lastrecord.creditlimit,
                        terms = lastrecord.terms,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = Customer(id = None,
                        customer_code = record.CustomerID,
                        name = record.Name,
                        address = combine(record.Address1,
                                          record.Address2,
                                          record.Address3,
                                          record.Address4,
                                          record.Address5),
                        postcode = record.PostCode,
                        phone = record.Telephone,
                        fax = record.Fax,
                        email = record.Email,
                        website = record.Website,
                        contactname = record.ContactName,
                        vat = record.VAT,
                        comment = record.Comment,
                        memo = record.Memo,
                        creditlimit = record.CreditLimit,
                        terms = record.Terms,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        print record
        recordtodelete = nbdb.query(Customer). \
          filter(Customer.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()
    
    
    
def update_supplier():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(Supplier). \
                            order_by(desc(Supplier.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(Supplier).filter(Supplier.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_supplier,                           'accounts_Supplier')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_supplier,                           'accounts_Supplier', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            newsupplier = Supplier(id = None,
                        supplier_code = record.SupplierID,
                        name = record.Name,
                        address = combine(record.Address1,
                                          record.Address2,
                                          record.Address3,
                                          record.Address4,
                                          record.Address5),
                        postcode = record.PostCode,
                        phone = record.Telephone,
                        fax = record.Fax,
                        email = record.Email,
                        website = record.Website,
                        contactname = record.ContactName,
                        vat = record.VAT,
                        comment = record.Comment,
                        memo = record.Memo,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newsupplier.lastupdated = record.LastUpdated
            nbdb.add(newsupplier)
        elif record.RecordNumber in updated_records:
            lastrecord = nbdb.query(Supplier). \
             filter(Supplier.rr_recordno == record.RecordNumber).all()[0]
            old = SupplierHistory(id = None,
                        supplier_id = lastrecord.id,
                        supplier_code = lastrecord.supplier_code,
                        name = lastrecord.name,
                        address = lastrecord.address,
                        postcode = lastrecord.postcode,
                        phone = lastrecord.phone,
                        fax = lastrecord.fax,
                        email = lastrecord.email,
                        website = lastrecord.website,
                        contactname = lastrecord.contactname,
                        vat = lastrecord.vat,
                        comment = lastrecord.comment,
                        memo = lastrecord.memo,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = Supplier(id = None,
                        supplier_code = record.SupplierID,
                        name = record.Name,
                        address = combine(record.Address1,
                                          record.Address2,
                                          record.Address3,
                                          record.Address4,
                                          record.Address5),
                        postcode = record.PostCode,
                        phone = record.Telephone,
                        fax = record.Fax,
                        email = record.Email,
                        website = record.Website,
                        contactname = record.ContactName,
                        vat = record.VAT,
                        comment = record.Comment,
                        memo = record.Memo,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        print record
        recordtodelete = nbdb.query(Supplier). \
          filter(Supplier.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()



def update_contacts():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(Contact). \
                            order_by(desc(Contact.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(Contact).filter(Contact.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_contact,                           'accounts_Contact')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_contact,                           'accounts_Contact', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            customer = nbdb.query(Customer).filter(Customer.customer_code == record.ClientID).all()
            if len(customer) == 1:
                customerid = customer[0].id
            else:
                customerid = None
            supplier = nbdb.query(Supplier).filter(Supplier.supplier_code == record.ClientID).all()
            if len(supplier) == 1:
                supplierid = supplier[0].id
            else:
                supplierid = None
            newcontact = Contact(id = None,
                        clientcode = record.ClientID,
                        title = record.Title,
                        forename= record.Forename,
                        surname = record.Surname,
                        phone = record.Phone,
                        department = record.Department,
                        customer_id = customerid,
                        supplier_id = supplierid,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newcontact.lastupdated = record.LastUpdated
            nbdb.add(newcontact)
        elif record.RecordNumber in updated_records:
            customer = nbdb.query(Customer).filter(Customer.customer_code == record.ClientID).all()
            if len(customer) == 1:
                customerid = customer[0].id
            else:
                customerid = None
            supplier = nbdb.query(Supplier).filter(Supplier.supplier_code == record.ClientID).all()
            if len(supplier) == 1:
                supplierid = supplier[0].id
            else:
                supplierid = None
                
            lastrecord = nbdb.query(Contact). \
             filter(Contact.rr_recordno == record.RecordNumber).all()[0]
            old = ContactHistory(id = None,
                        contact_id = lastrecord.id,
                        clientcode = lastrecord.clientcode,
                        title = lastrecord.title,
                        forename = lastrecord.forename,
                        surname = lastrecord.surname,
                        phone = lastrecord.phone,
                        department = lastrecord.department,
                        customer_id = lastrecord.customer_id,
                        supplier_id = lastrecord.supplier_id,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = Contact(id = None,
                        clientcode = record.ClientID,
                        title = record.Title,
                        forename = record.Forename,
                        surname = record.Surname,
                        phone = record.Phone,
                        department = record.Department,
                        customer_id = customerid,
                        supplier_id = supplierid,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        print record
        recordtodelete = nbdb.query(Contact). \
          filter(Contact.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()


def update_depot():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(Depot). \
                            order_by(desc(Depot.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(Depot).filter(Depot.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_depot,                           'accounts_Depot')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_depot,                           'accounts_Depot', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            customer = nbdb.query(Customer).filter(Customer.customer_code == record.ClientID).all()
            if len(customer) == 1:
                customerid = customer[0].id
            else:
                customerid = None
            supplier = nbdb.query(Supplier).filter(Supplier.supplier_code == record.ClientID).all()
            if len(supplier) == 1:
                supplierid = supplier[0].id
            else:
                supplierid = None
            newdepot = Depot(id = None,
                        clientid = record.ClientID,
                        clientname = record.Name,
                        address = combine(record.Address1,
                                          record.Address2,
                                          record.Address3,
                                          record.Address4,
                                          record.Address5),
                        postcode = record.PostCode,
                        phone = record.Telephone,
                        fax = record.Fax,
                        email = record.Email,
                        comment = record.Comment,
                        customer_id = customerid,
                        supplier_id = supplierid,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newdepot.lastupdated = record.LastUpdated
            nbdb.add(newdepot)
        elif record.RecordNumber in updated_records:
            customer = nbdb.query(Customer).filter(Customer.customer_code == record.ClientID).all()
            if len(customer) == 1:
                customerid = customer[0].id
            else:
                customerid = None
            supplier = nbdb.query(Supplier).filter(Supplier.supplier_code == record.ClientID).all()
            if len(supplier) == 1:
                supplierid = supplier[0].id
            else:
                supplierid = None
                
            lastrecord = nbdb.query(Depot). \
             filter(Depot.rr_recordno == record.RecordNumber).all()[0]
            old = DepotHistory(id = None,
                        depot_id = lastrecord.id,
                        clientid = lastrecord.clientid,
                        clientname = lastrecord.clientname,
                        address = lastrecord.address,
                        postcode = lastrecord.postcode,
                        phone = lastrecord.phone,
                        fax = lastrecord.fax,
                        email = lastrecord.email,
                        comment = lastrecord.comment,
                        customer_id = lastrecord.customer_id,
                        supplier_id = lastrecord.supplier_id,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = Depot(id = None,
                        clientid = record.ClientID,
                        clientname = record.Name,
                        address = combine(record.Address1,
                                          record.Address2,
                                          record.Address3,
                                          record.Address4,
                                          record.Address5),
                        postcode = record.PostCode,
                        phone = record.Telephone,
                        fax = record.Fax,
                        email = record.Email,
                        comment = record.Comment,
                        customer_id = customerid,
                        supplier_id = supplierid,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        print record
        recordtodelete = nbdb.query(Depot). \
          filter(Depot.rr_recordno == record).all()[0]
        recordtodelete.deleted = True
            
    nbdb.commit()
    

def update_purchaseorder():
    global rrdata
    global nbdb
    lastrecord = nbdb.query(PurchaseOrder). \
                            order_by(desc(PurchaseOrder.lastupdated)). \
                            first()
    if lastrecord is None:
        lastupdated = datetime.datetime(1982,1,1,0,0)
    else:
        lastupdated = lastrecord.lastupdated
    lastnb_records = set([i.rr_recordno for i in nbdb.query(PurchaseOrder).filter(PurchaseOrder.deleted == False)])
    all_rr_data = rrdata.query(nb.sql.get_purchaseorder,                           'stock_Purchase Order')
    all_records = set([i.RecordNumber for i in all_rr_data])
    newdata = rrdata.query(nb.sql.get_purchaseorder,                           'stock_Purchase Order', lastupdated)
    
    recentmods = set([i.RecordNumber for i in newdata])
    
    new_records = recentmods.difference(lastnb_records)
    updated_records = recentmods.intersection(lastnb_records)
    deletedrecords = lastnb_records.difference(all_records)
    
    for record in newdata:
        record = sanitise(record)
        if record.RecordNumber in new_records:
            supplier = nbdb.query(Supplier).filter(Supplier.supplier_code == record.Supplier).all()
            if len(supplier) == 1:
                supplierid = supplier[0].id
            else:
                supplierid = None
            newpo = PurchaseOrder(id = None,
                        pon = record.PO_Num,
                        ordervalue = record.OrderValue,
                        supplier_id = supplierid,
                        orderref = record.OrderReference,
                        orderdate = record.OrderDate,
                        placedby = record.PlacedBy,
                        printedcomment = record.PrintedComment,
                        deliverycomment = record.DeliveryComment,
                        status = record.Status,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                        
            newpo.lastupdated = record.LastUpdated
            nbdb.add(newpo)
        elif record.RecordNumber in updated_records:
            supplier = nbdb.query(Supplier).filter(Supplier.supplier_code == record.Supplier).all()
            if len(supplier) == 1:
                supplierid = supplier[0].id
            else:
                supplierid = None
                
            lastrecord = nbdb.query(PurchaseOrder). \
             filter(PurchaseOrder.rr_recordno == record.RecordNumber).all()[0]
            old = PurchaseOrderHistory(id = None,
                        po_id = lastrecord.id,
                        pon = lastrecord.pon,
                        ordervalue = lastrecord.ordervalue,
                        supplier_id = lastrecord.supplier_id,
                        orderref = lastrecord.orderref,
                        orderdate = lastrecord.orderdate,
                        placedby = lastrecord.placedby,
                        printedcomment = lastrecord.printedcomment,
                        deliverycomment = lastrecord.deliverycomment,
                        status = lastrecord.status,
                        lastupdated = lastrecord.lastupdated,
                        rr_recordno = lastrecord.rr_recordno)
                        
            old.lastupdated = lastrecord.lastupdated
            
            nbdb.delete(lastrecord)
            newrecord = PurchaseOrder(id = None,
                        pon = record.PO_Num,
                        ordervalue = record.OrderValue,
                        supplier_id = supplierid,
                        orderref = record.OrderReference,
                        orderdate = record.OrderDate,
                        placedby = record.PlacedBy,
                        printedcomment = record.PrintedComment,
                        deliverycomment = record.DeliveryComment,
                        status = record.Status,
                        lastupdated = record.LastUpdated,
                        rr_recordno = record.RecordNumber,
                        deleted = False)
                      
            newrecord.lastupdated = record.LastUpdated
            
            nbdb.add(old)
            newrecord.history.append(old)
            nbdb.add(newrecord)
    for record in deletedrecords:
        print record
        recordtodelete = nbdb.query(PurchaseOrder). \
          filter(PurchaseOrder.rr_recordno == record).all()[0]
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