from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

from sqlalchemy.interfaces import PoolListener

class SetTextFactory(PoolListener):
    """Solves problem with pound signs"""
    def connect(self, dbapi_con, con_record):
        dbapi_con.text_factory = str

dbpath = 'C:/Users/Tim/Desktop/NaphthaBase/NaphthaBase.db'
engine = create_engine('sqlite:///%s' % dbpath, echo=True)
#engine = create_engine('sqlite:///%s' % dbpath, listeners=[SetTextFactory()],  echo=True)
Base = declarative_base(engine)

class Material(Base):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    description = Column(String)
    lastupdated = Column(DateTime, nullable = True)
    rr_recordno = Column(String)

    def __init__(self, id, code, description, lastupdated, rr_recordno):
        self.id = id
        self.code = code
        self.description = description
        self.rr_recordno = rr_recordno

    def __repr__(self):
        return "<Material - %s: %s>" % (self.code, self.description)
    

class Hauliers(Base):
    __tablename__ = 'hauliers'

    id = Column(Integer, primary_key=True)
    haulierkey = Column(String)
    name = Column(String)
    nominalcode = Column(String)
    lastupdated = Column(DateTime)
    rr_recordno = Column(String)

    def __init__(self, id, haulierkey, name, nominalcode, lastupdated, rr_recordno):
        self.id = id
        self.haulierkey = haulierkey
        self.name = name
        self.nominalcode = nominalcode
        self.lastupdated = lastupdated
        self.rr_recordno = rr_recoderno

    def __repr__(self):
        return "<Haulier - %s: %s>" % (self.haulierkey, self.name)
    

class Carrier(Base):
    __tablename__ = 'carrier'

    id = Column(Integer, primary_key=True)
    won = Column(String)
    description = Column(String)
    lastupdated = Column(DateTime)
    rr_recordno = Column(String)

    def __init__(self, id, won, description, lastupdated, rr_recordno):
        self.id = id
        self.won = won
        self.description = description
        self.lastupdated = lastupdated
        self.rr_recordno = rr_recordno

    def __repr__(self):
        return "<Carrier - WO%s: %s>" % (self.won, self.description)

    
class Customer(Base):
    __tablename__ = 'customer'
    
    id = Column(Integer, primary_key=True)
    customer_code = Column(String)
    name = Column(String)
    address = Column(String)
    postcode = Column(String)
    phone = Column(String)
    fax = Column(String)
    email = Column(String)
    website = Column(String)
    contactname = Column(String)
    vat = Column(String)
    comment = Column(String)
    memo = Column(String)
    creditlimit = Column(String)
    terms = Column(String)
    lastupdated = Column(DateTime)
    rr_recordno = Column(Integer)
    
    def __init__(self, id, customer_code, name, address, postcode, phone, fax, email, website, contactname, vat, comment, memo, creditlimit, terms, lastupdated, rr_recordno):
        self.id = id
        self.customer_code = customer_code
        self.name = name
        self.address = address
        self.postcode = postcode
        self.phone = phone
        self.fax = fax
        self.email = email
        self.website = website
        self.contactname = contactname
        self.vat = vat
        self.comment =comment
        self.memo = memo
        self.creditlimit = creditlimit
        self.terms = terms
        self.latupdated = lastupdated
        self.rr_recordno = rr_recordno
    
    def __repr__(self):
        return "<Customer - '%s': '%s'>" % (self.customer_code, self.name)

        
class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True)
    supplier_code = Column(String)
    name = Column(String)
    address = Column(String)
    postcode = Column(String)
    phone = Column(String)
    fax = Column(String)
    email = Column(String)
    website = Column(String)
    contactname = Column(String)
    vat = Column(String)
    comment = Column(String)
    memo = Column(String)
    lastupdated = Column(DateTime)
    rr_recordno = Column(Integer)
    
    def __init__(self, id, supplier_code, name, address, postcode, phone, fax, email, website, contactname, vat, comment, memo, lastupdated, rr_recordno):
        self.id = id
        self.supplier_code = supplier_code
        self.name = name
        self.address = address
        self.postcode = postcode
        self.phone = phone
        self.fax = fax
        self.email = email
        self.website = website
        self.contactname = contactname
        self.vat = vat
        self.comment =comment
        self.memo = memo
        self.latupdated = lastupdated
        self.rr_recordno = rr_recordno
    
    def __repr__(self):
        return "<Supplier - '%s': '%s'>" % (self.supplier_code, self.name)

    
class Contact(Base):
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    clientcode = Column(String)
    title = Column(String)
    forename = Column(String)
    surname = Column(String)
    phone = Column(String)
    department = Column(String)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    lastupdated = Column(DateTime)
    rr_recordno = Column(Integer)
    
    customer = relationship(Customer, backref=backref('contacts', order_by=id))
    supplier = relationship(Supplier, backref=backref('contacts', order_by=id))
    
    def __init__(self, id, clientcode, title, forename, surname, phone, department, customer, supplier, lastupdated, rr_recordno):
        self.id = id
        self.clientcode = clientcode
        self.title = title
        self.forename = forename
        self.surname = surname
        self.phone = phone
        self.department = department
        self.lastupdated = lastupdated
        self.rr_recordno = rr_recordno

    def __repr__(self):
        return "<Contact - %s: %s %s>" % (self.clientcode, self.forename, self.surname)


class Depot(Base):
    __tablename__ = 'depot'

    id = Column(Integer, primary_key=True)
    clientid = Column(String)
    clientname = Column(String)
    address = Column(String)
    postcode = Column(String)
    phone = Column(String)
    fax = Column(String)
    email = Column(String)
    comment = Column(String)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    lastupdated = Column(DateTime)
    rr_recordno = Column(Integer)
    
    customer = relationship(Customer, backref=backref('depot', order_by=id))
    supplier = relationship(Supplier, backref=backref('depot', order_by=id))

    def __init__(self, id, clientid, clientname, addres, postcode, phone, fax, email, comment, lastupdated, rr_recordno):
        self.id = id
        self.clientid = clientid
        self.clientname = clientname
        self.address = self.address
        self.postcode = self.postcode
        self.phone = self.phone
        self.fax = self.fax
        self.email = self.email
        self.comment = self.comment
        self.lastupdated = self.lastupdated
        self.rr_recordno = rr_recordno

    def __repr__(self):
        return "<Depot - %s: %s>" % (self.clientid, self.clientname)
    

class PurchaseOrder(Base):
    __tablename__ = 'purchaseorder'

    id = Column(Integer, primary_key=True)
    pon = Column(String)
    ordervalue = Column(String)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    orderref = Column(String)
    orderdate = Column(DateTime)
    placedby = Column(String)
    printedcomment = Column(String)
    deliverycomment = Column(String)
    status = Column(Integer)
    lastupdated = Column(DateTime)
    rr_recordno = Column(Integer)
    
    supplier = relationship(Supplier, backref=backref('purchaseorders', order_by=id))
    
    def __init__(self, id, pon, ordervalue, supplier_id, orderref, orderdate, placedby, printedcomment, deliverycomment, status, lastupdated, rr_recordno):
        self.id = id
        self.pon = pon
        self.ordervalue = ordervalue
        self.orderref = orderref
        self.orderdate = orderdate
        self.placedby = placedby
        self.printedcomment = printedcomment
        self.deliverycomment = deliverycomment
        self.status = status
        self.lastupdated = lastupdated
        self.rr_recordno = rr_recordno
        
    def __repr__(self):
        return "<PurchaseOrder - %s>" % (self.pon)
    

class PurchaseItem(Base):
    __tablename__ = 'purchaseitem'

    id = Column(Integer, primary_key=True)
    pon = Column(String)
    itemno = Column(Integer)
    purchaseorder_id = Column(Integer, ForeignKey('purchaseorder.id'))
    material_id = Column(Integer, ForeignKey('material.id'))
    quantity = Column(String)
    price = Column(String)
    duedate = Column(Date)
    delivered_quantity = Column(String)
    lastupdated = Column(DateTime)
    rr_recordno = Column(Integer)
    
    purchaseorder = relationship(PurchaseOrder, backref=backref('purchaseitems', order_by=id))
    material = relationship(Material, backref=backref('purchaseitems', order_by=id))

    def __init__(self, id, pon, itemno, quantity, price, duedate, delivered_quantity, lastupdated, rr_recordno):
        self.id = id
        self.pon = pon
        self.itemno = itemno
        self.quantity = quantity
        self.price = price
        self.duedate = duedate
        self.delivered_quantity = delivered_quantity
        self.lastupdated = lastupdated
        self.rr_recordno = rr_recordno

    def __repr__(self):
        return "<PurchaseItem - id:%s , PON%s>" % (self.id, self.pon)
    

class Stock(Base):
    __tablename__ = 'stock'
    
    id = Column(Integer, primary_key=True)
    batch = Column(String)
    material_id = Column(Integer, ForeignKey('material.id'))
    stockinfo = Column(String)
    status = Column(String)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    purchaseitem_id = Column(Integer, ForeignKey('purchaseitem.id'))
    costprice = Column(String)
    batchup_quantity = Column(String)
    batchup_date = Column(DateTime)
    stockquantity = Column(String)
    lastupdated = Column(DateTime)
    rr_recordno = Column(Integer)
    
    material = relationship(Material, backref=backref('stock', order_by=id))
    supplier = relationship(Supplier, backref=backref('stock', order_by=id))
    purchaseitem = relationship(PurchaseItem, backref=backref('stock', order_by=id))
    
    def __init__(self, id, batch, stockinfo, status, costprice, batchup_quantity, batchup_date, stockquantity, lastupdated, rr_recordno):
        self.id = id
        self.batch = batch
        self.stockinfo = stockinfo
        self.status = status
        self.costprice = costprice
        self.batchup_quantity = batchup_quantity
        self.batchup_date = batchup_date
        self.stockquantity = stockquantity
        self.lastupdated = lastupdated
        self.rr_recordno = rr_recordno

    def __repr__(self):
        return "<Stock - %s: %s>" % (self.batch, self.status)

        
class SalesOrder(Base):
    __tablename__ = 'salesorder'

    id = Column(Integer, primary_key=True)
    won = Column(String)
    followon_link = Column(String)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer_orderno = Column(String)
    picklist_comment = Column(String)
    ordervalue = Column(String)
    status = Column(Integer)
    orderdate = Column(DateTime)
    despatchdate = Column(DateTime)
    invoicedate = Column(DateTime)
    operator = Column(String)
    delivery_name = Column(String)
    delivery_address = Column(String)
    delivery_postcode = Column(String)
    printed_comments = Column(String)
    invoice_comments = Column(String)
    invoice_terms = Column(String)
    item_count = Column(Integer)
    carrier_id = Column(Integer, ForeignKey('carrier.id'))
    lastupdated = Column(DateTime)
    rr_recordno = Column(Integer)
    
    customer = relationship(Customer, backref=backref('salesorder', order_by=id))
    carrier = relationship(Carrier, backref=backref('salesorder', order_by=id))
    
    def __init__(self, id, won, followon_link, picklist_comment, ordervalue, status, orderdate, despatchdate, invoicedate, operator, delivery_name, delivery_address, delivery_postcode, printed_comments, invoice_comments, invoice_terms, item_count, lastupdated, rr_recordno):
        self.id = id
        self.won = won
        self.followon_link = followon_link
        self.picklist_comment = picklist_comment
        self.ordervalue = ordervalue
        self.status = status
        self.orderdate = orderdate
        self.despatchdate = despatchdate
        self.invoicedate = invoicedate
        self.operator = operator
        self.delivery_name = delivery_name
        self.delivery_address = delivery_address
        self.delivery_postcode = delivery_postcode
        self.printed_comments = printed_comments
        self.invoice_comments = invoice_comments
        self.invoice_terms = invoice_terms
        self.item_count = item_count
        self.lastupdated = lastupdated
        self.rr_recordno = rr_recordno
    
    def __repr__(self):
        return "<SalesOrder - %s>" % (self.won)
    

class SalesItem(Base):
    __tablename__ = 'salesitem'
    
    id = Column(Integer, primary_key=True)
    won = Column(String)
    salesorder_id = Column(Integer, ForeignKey('salesorder.id'))
    material_id = Column(Integer, ForeignKey('material.id'))
    quantity = Column(String)
    price = Column(String)
    required_date = Column(DateTime)
    lastupdated = Column(DateTime)
    rr_recordno = Column(Integer)
    
    salesorder = relationship(SalesOrder, backref=backref('salesitems', order_by=id))
    material = relationship(Material, backref=backref('salesitems', order_by=id))
    def __init__(self, id, won, quantity, price, required_date, lastupdated, rr_recordno):
        self.id = id
        self.won = won
        self.quantity = quantity
        self.price = price
        self.required_date = required_date
        self.lastupdated = lastupdated
        self.rr_recordno = rr_recordno

    def __repr__(self):
        return "<SalesItem - %s>" % (self.won)
    

class DeletedSales(Base):
    __tablename__ = 'deletedsales'

    id = Column(Integer, primary_key=True)
    won = Column(String)
    salesorder_id = Column(Integer, ForeignKey('salesorder.id'))
    operator = Column(String)
    reason = Column(String)
    lastupdated = Column(DateTime)
    rr_recordno = Column(Integer)
    
    salesorder = relationship(SalesOrder, backref=backref('deletedsales', order_by=id))
    
    def __init_(self, id, won, operator, reason, lastupdated, rr_recordno):
        self.id = id
        self.won = won
        self.operator = operator
        self.reason = reason
        self.lastupdated = lastupdated
        self.rr_recordno = rr_recordno
    
    def __repr__(self):
        return "<DeletedSales - %s: %s>" % (self.won, self.reason)
    

class Despatch(Base):
    __tablename__ = 'despatch'
    
    id = Column(Integer, primary_key=True)
    won = Column(String)
    materialcode = Column(String)
    stock_id = Column(Integer, ForeignKey('stock.id'))
    salesitem_id = Column(Integer, ForeignKey('salesitem.id'))
    batch = Column(String)
    quantity = Column(String)
    lastupdated = Column(DateTime)
    rr_recordno = Column(Integer)
    
    stock = relationship(Stock, backref=backref('despatched', order_by=id))
    salesitem = relationship(SalesItem, backref=backref('despatched', order_by=id))
    
    def __init__(self, id, won, materialcode, batch, quantity, lastupdated, rr_recordno):
        self.id = id
        self.won = won
        self.materialcode = materialcode
        self.batch = batch
        self.quantity = quantity
        self.lastupdated = lastupdated
        self.rr_recordno = rr_recordno
    
    def __repr__(self):
        return "<Despatch - WON%s: %s, %sKg>" % (self.won, self.materialcode, self.quantity)
       
    
class StockMovement(Base):
    __tablename__ = 'stockmovement'

    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey('stock.id'))
    action = Column(String)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    salesitem_id = Column(Integer, ForeignKey('salesitem.id'))
    salesprice = Column(String)
    pon = Column(String)
    movement_description = Column(String)
    movement_quantity = Column(String)
    item_order = Column(Integer)
    user_id = Column(String)
    lastupdated = Column(DateTime)
    rr_recordno = Column(Integer)
    
    stock = relationship(Stock, backref=backref('stockmovement', order_by=id))
    customer = relationship(Customer, backref=backref('stockmovement', order_by=id))
    salesitem = relationship(SalesItem, backref=backref('stockmovement', order_by=id))
    
    def __init__(self, id, action, salesprice, pon, movement_description, movement_quantity, item_order, user_id, lastupdated, rr_recordno):
        self.id = id
        self.action = action
        self.salesprice = salesprice
        self.pon = pon
        self.movement_description = movement_description
        self.movement_quantity = movement_quantity
        self.item_order = item_order
        self.user_id = user_id
        self.lastupdated = lastupdated
        self.rr_recordno = rr_recordno
    
    def __repr__(self):
        return "<StockMovement - %s: %s %sKg>" % (self.action, self.movement_description, self.movement_quantity)
    

def loadSession():
    metadata = Base.metadata
    Session = sessionmaker(bind = engine)
    session = Session()
    return session