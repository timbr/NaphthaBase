from django.db import models

# Create your models here.
class Material(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'material'

    def __unicode__(self):
        return self.code
    
    def listall(self):
        return [self.code, self.description, self.lastupdated, self.rr_recordno]


class Hauliers(models.Model):
    haulierkey = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    nominalcode = models.CharField(max_length=10)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'hauliers'

    def __unicode__(self):
        return self.haulierkey


class Carrier(models.Model):
    won = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'carrier'

    def __unicode__(self):
        return self.won, self.description


class Customer(models.Model):
    customer_code = models.CharField(max_length=10)
    name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=20, null=True)
    fax = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)
    website = models.CharField(max_length=50, null=True)
    contactname = models.CharField(max_length=30, null=True)
    vat = models.CharField(max_length=20, null=True)
    comment = models.CharField(max_length=100, null=True)
    memo = models.CharField(max_length=100, null=True)
    creditlimit = models.CharField(max_length=15, null=True)
    terms = models.CharField(max_length=20, null=True)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'customer'
    
    def __unicode__(self):
        return self.customer_code


class Supplier(models.Model):
    supplier_code = models.CharField(max_length=10)
    name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=20, null=True)
    fax = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)
    website = models.CharField(max_length=50, null=True)
    contactname = models.CharField(max_length=30, null=True)
    vat = models.CharField(max_length=20, null=True)
    comment = models.CharField(max_length=100, null=True)
    memo = models.CharField(max_length=100, null=True)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'supplier'
    
    def __unicode__(self):
        return self.supplier_code


class Contact(models.Model):
    clientcode = models.CharField(max_length=10)
    title = models.CharField(max_length=10, null=True)
    forename = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=50, null=True)
    customer = models.ForeignKey(Customer, null=True)
    supplier = models.ForeignKey(Supplier, null=True)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'contact'
    
    def __unicode__(self):
        return self.forename+' '+self.surname


class Depot(models.Model):
    clientid = models.CharField(max_length=10)
    clientname = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=20, null=True)
    fax = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)
    comment = models.CharField(max_length=100, null=True)
    customer = models.ForeignKey(Customer, null=True)
    supplier = models.ForeignKey(Supplier, null=True)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'depot'
    
    def __unicode__(self):
        return self.clientname


class PurchaseOrder(models.Model):
    pon = models.CharField(max_length=10)
    ordervalue = models.CharField(max_length=15, null=True)
    supplier = models.ForeignKey(Supplier, null=True)
    orderref = models.CharField(max_length=20)
    orderdate = models.DateTimeField('order date')
    placedby = models.CharField(max_length=50)
    printedcomment = models.CharField(max_length=100, null=True)
    deliverycomment = models.CharField(max_length=100, null=True)
    status = models.IntegerField(null=True)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'purchaseorder'
    
    def getstatus(self):
        po_status = {
            0: 'Undefined',
            1: 'Awaiting',
            2: 'Printed',
            3: 'Delivered',
            4: 'Part Delivered',
            5: 'Invoiced',
            6: 'Verified',
            7: 'Updated',
            8: 'Cancelled'}
        return po_status[self.status]
    
    def __unicode__(self):
        return self.pon
 
 
class PurchaseItem(models.Model):
    pon = models.CharField(max_length=10)
    purchaseorder = models.ForeignKey(PurchaseOrder, null=True)
    itemno = models.IntegerField()
    material = models.ForeignKey(Material, null=True)
    quantity = models.CharField(max_length=15)
    price = models.CharField(max_length=15)
    duedate = models.DateTimeField('due date')
    delivered_quantity = models.CharField(max_length=15)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'purchaseitem'
    
    def __unicode__(self):
        return self.pon


class Stock(models.Model):
    batch = models.CharField(max_length=10)
    material = models.ForeignKey(Material, null=True)
    stockinfo = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=1)
    supplier = models.ForeignKey(Supplier, null=True)
    purchaseitem = models.ForeignKey(PurchaseItem, null=True)
    costprice = models.CharField(max_length=20, null=True)
    batchup_quantity = models.CharField(max_length=20)
    batchup_date = models.DateTimeField('batch-up date')
    stockquantity = models.CharField(max_length=20)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'stock'
    
    def getstatus(self):
        stock_status = {
            'E': 'Empty',
            'S': 'In Stock',
            'C': 'Not Sure (C)',
            'R': 'Not Sure (R)'}
        return stock_status[self.status]
    
    def __unicode__(self):
        return self.batch

class SalesOrder(models.Model):
    won = models.CharField(max_length=10)
    followon_link = models.CharField(max_length=10, null=True)
    customer = models.ForeignKey(Customer, null=True)
    customer_orderno = models.CharField(max_length=20, null=True)
    picklist_comment = models.CharField(max_length=200, null=True)
    ordervalue = models.CharField(max_length=15, null=True)
    status = models.IntegerField()
    orderdate = models.DateTimeField('order date')
    despatchdate = models.DateTimeField('despatch date')
    invoicedate = models.DateTimeField('invoice date')
    operator = models.CharField(max_length=20)
    delivery_name = models.CharField(max_length=100, null=True)
    delivery_address = models.CharField(max_length=200, null=True)
    delivery_postcode = models.CharField(max_length=20, null=True)
    printed_comments = models.CharField(max_length=200, null=True)
    invoice_comments = models.CharField(max_length=200, null=True)
    invoice_terms = models.CharField(max_length=100, null=True)
    item_count = models.IntegerField()
    carrier =  models.ForeignKey(Carrier, null=True)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'salesorder'
    
    def getstatus(self):
        so_status = {
            0: 'Awaiting',
            1: 'Delivered',
            2: 'Not Sure (3)',
            3: 'Invoiced',
            4: 'Updated',
            5: 'Not Sure (5)',
            6: 'Verified',
            7: 'Not Sure (7)',
            8: 'Not Sure (8)'}
        return so_status[self.status]
    
    def __unicode__(self):
        return self.pon
    
    def __unicode__(self):
        return self.won

class SalesItem(models.Model):
    won = models.CharField(max_length=10)
    salesorder = models.ForeignKey(SalesOrder, null=True)
    material = models.ForeignKey(Material, null=True)
    quantity = models.CharField(max_length=15)
    price = models.CharField(max_length=15)
    required_date = models.DateTimeField('required date')
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'salesitem'
    
    def __unicode__(self):
        return self.won


class DeletedSales(models.Model):
    won = models.CharField(max_length=10)
    salesorder = models.ForeignKey(SalesOrder, null=True)
    operator = models.CharField(max_length=20)
    reason = models.CharField(max_length=50)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'deletedsales'
    
    def __unicode__(self):
        return self.won


class Despatch(models.Model):
    won = models.CharField(max_length=10)
    materialcode = models.CharField(max_length=20)
    stock = models.ForeignKey(Stock, null=True)
    salesitem = models.ForeignKey(SalesItem, null=True)
    batch = models.CharField(max_length=20)
    quantity = models.CharField(max_length=20)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'despatch'
    
    def __unicode__(self):
        return self.won


class StockMovement(models.Model):
    stock = models.ForeignKey(Stock, null=True)
    action = models.CharField(max_length=10, null=True)
    customer = models.ForeignKey(Customer, null=True)
    salesitem = models.ForeignKey(SalesItem, null=True)
    salesprice = models.CharField(max_length=20, null=True)
    movement_description = models.CharField(max_length=100, null=True)
    movement_quantity = models.CharField(max_length=20, null=True)
    item_order = models.IntegerField()
    user_id = models.CharField(max_length=20, null=True)
    lastupdated = models.DateTimeField('last updated')
    rr_recordno = models.IntegerField()
    
    class Meta:
        db_table = 'stockmovement'
        ordering = ['rr_recordno']
        
    def getstatus(self):
        movment_status = {
            'G': 'Goods In',
            'D': 'Despatch',
            'M': 'Stock Adjustment',
            'P': 'Opening Stock'}
        return movment_status[self.action]
    
    def __unicode__(self):
        return self.stock.batch