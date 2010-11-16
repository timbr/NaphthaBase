# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Additionalitems(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    haulierkey = models.CharField(max_length=10, db_column=u'HaulierKey', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=30, db_column=u'Name', blank=True) # Field name made lowercase.
    nominalcode = models.CharField(max_length=10, db_column=u'NominalCode', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'AdditionalItems'

class Contact(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    clientid = models.CharField(max_length=10, db_column=u'ClientID', blank=True) # Field name made lowercase.
    title = models.CharField(max_length=10, db_column=u'Title', blank=True) # Field name made lowercase.
    forename = models.CharField(max_length=40, db_column=u'Forename', blank=True) # Field name made lowercase.
    surname = models.CharField(max_length=40, db_column=u'Surname', blank=True) # Field name made lowercase.
    phone = models.CharField(max_length=15, db_column=u'Phone', blank=True) # Field name made lowercase.
    department = models.CharField(max_length=40, db_column=u'Department', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Contact'

class Customer(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    customerid = models.CharField(max_length=10, db_column=u'CustomerID', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=30, db_column=u'Name', blank=True) # Field name made lowercase.
    address1 = models.CharField(max_length=30, db_column=u'Address1', blank=True) # Field name made lowercase.
    address2 = models.CharField(max_length=30, db_column=u'Address2', blank=True) # Field name made lowercase.
    address3 = models.CharField(max_length=30, db_column=u'Address3', blank=True) # Field name made lowercase.
    address4 = models.CharField(max_length=30, db_column=u'Address4', blank=True) # Field name made lowercase.
    address5 = models.CharField(max_length=30, db_column=u'Address5', blank=True) # Field name made lowercase.
    postcode = models.CharField(max_length=10, db_column=u'PostCode', blank=True) # Field name made lowercase.
    telephone = models.CharField(max_length=15, db_column=u'Telephone', blank=True) # Field name made lowercase.
    fax = models.CharField(max_length=15, db_column=u'Fax', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=30, db_column=u'Email', blank=True) # Field name made lowercase.
    website = models.CharField(max_length=30, db_column=u'Website', blank=True) # Field name made lowercase.
    contactname = models.CharField(max_length=30, db_column=u'ContactName', blank=True) # Field name made lowercase.
    vat = models.CharField(max_length=30, db_column=u'VAT', blank=True) # Field name made lowercase.
    comment = models.TextField(db_column=u'Comment', blank=True) # Field name made lowercase.
    memo = models.TextField(db_column=u'Memo', blank=True) # Field name made lowercase.
    creditlimit = models.CharField(max_length=30, db_column=u'CreditLimit', blank=True) # Field name made lowercase.
    terms = models.CharField(max_length=30, db_column=u'Terms', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Customer'

class Depot(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    clientid = models.CharField(max_length=10, db_column=u'ClientID', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=40, db_column=u'Name', blank=True) # Field name made lowercase.
    address1 = models.CharField(max_length=40, db_column=u'Address1', blank=True) # Field name made lowercase.
    address2 = models.CharField(max_length=40, db_column=u'Address2', blank=True) # Field name made lowercase.
    address3 = models.CharField(max_length=40, db_column=u'Address3', blank=True) # Field name made lowercase.
    address4 = models.CharField(max_length=40, db_column=u'Address4', blank=True) # Field name made lowercase.
    address5 = models.CharField(max_length=40, db_column=u'Address5', blank=True) # Field name made lowercase.
    postcode = models.CharField(max_length=10, db_column=u'PostCode', blank=True) # Field name made lowercase.
    telephone = models.CharField(max_length=15, db_column=u'Telephone', blank=True) # Field name made lowercase.
    fax = models.CharField(max_length=15, db_column=u'Fax', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=40, db_column=u'Email', blank=True) # Field name made lowercase.
    comment = models.TextField(db_column=u'Comment', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Depot'

class Formula(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    code = models.CharField(max_length=10, db_column=u'Code', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=40, db_column=u'Description', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Formula'

class Formulastock(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    batch = models.CharField(max_length=10, db_column=u'Batch', blank=True) # Field name made lowercase.
    batchstatus = models.CharField(max_length=10, db_column=u'BatchStatus', blank=True) # Field name made lowercase.
    quantitynow = models.CharField(max_length=15, db_column=u'QuantityNow', blank=True) # Field name made lowercase.
    originaldeliveredquantity = models.CharField(max_length=15, db_column=u'OriginalDeliveredQuantity', blank=True) # Field name made lowercase.
    stockinfo = models.TextField(db_column=u'StockInfo', blank=True) # Field name made lowercase.
    supplier = models.CharField(max_length=15, db_column=u'Supplier', blank=True) # Field name made lowercase.
    ponumber = models.CharField(max_length=10, db_column=u'PONumber', blank=True) # Field name made lowercase.
    purchasecost = models.CharField(max_length=15, db_column=u'PurchaseCost', blank=True) # Field name made lowercase.
    batchup_date = models.DateTimeField(null=True, db_column=u'BatchUp_Date', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'FormulaStock'

class Formulastockusage(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    batch = models.CharField(max_length=10, db_column=u'Batch', blank=True) # Field name made lowercase.
    code = models.CharField(max_length=10, db_column=u'Code', blank=True) # Field name made lowercase.
    revision = models.IntegerField(null=True, db_column=u'Revision', blank=True) # Field name made lowercase.
    customer = models.CharField(max_length=10, db_column=u'Customer', blank=True) # Field name made lowercase.
    wonumber = models.CharField(max_length=10, db_column=u'WONumber', blank=True) # Field name made lowercase.
    price = models.CharField(max_length=15, db_column=u'Price', blank=True) # Field name made lowercase.
    usagereference = models.TextField(db_column=u'UsageReference', blank=True) # Field name made lowercase.
    stockaction = models.TextField(db_column=u'StockAction', blank=True) # Field name made lowercase.
    itemorder = models.CharField(max_length=10, db_column=u'ItemOrder', blank=True) # Field name made lowercase.
    quantitymovement = models.CharField(max_length=15, db_column=u'QuantityMovement', blank=True) # Field name made lowercase.
    userid = models.CharField(max_length=10, db_column=u'UserID', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'FormulaStockUsage'

class Missingordernumber(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    wo_num = models.CharField(max_length=10, db_column=u'WO_Num', blank=True) # Field name made lowercase.
    userid = models.CharField(max_length=30, db_column=u'UserID', blank=True) # Field name made lowercase.
    reason = models.CharField(max_length=40, db_column=u'Reason', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'MissingOrderNumber'

class Purchaseitem(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    po_num = models.CharField(max_length=10, db_column=u'PO_Num', blank=True) # Field name made lowercase.
    code = models.CharField(max_length=10, db_column=u'Code', blank=True) # Field name made lowercase.
    quantity = models.CharField(max_length=15, db_column=u'Quantity', blank=True) # Field name made lowercase.
    price = models.CharField(max_length=15, db_column=u'Price', blank=True) # Field name made lowercase.
    duedate = models.DateField(null=True, db_column=u'DueDate', blank=True) # Field name made lowercase.
    deliveredquantity = models.CharField(max_length=15, db_column=u'DeliveredQuantity', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'PurchaseItem'

class Purchaseorder(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    po_num = models.CharField(max_length=10, db_column=u'PO_Num', blank=True) # Field name made lowercase.
    ordervalue = models.CharField(max_length=15, db_column=u'OrderValue', blank=True) # Field name made lowercase.
    supplier = models.CharField(max_length=10, db_column=u'Supplier', blank=True) # Field name made lowercase.
    orderreference = models.CharField(max_length=30, db_column=u'OrderReference', blank=True) # Field name made lowercase.
    orderdate = models.DateField(null=True, db_column=u'OrderDate', blank=True) # Field name made lowercase.
    placedby = models.CharField(max_length=30, db_column=u'PlacedBy', blank=True) # Field name made lowercase.
    printedcomment = models.TextField(db_column=u'PrintedComment', blank=True) # Field name made lowercase.
    deliverycomment = models.TextField(db_column=u'DeliveryComment', blank=True) # Field name made lowercase.
    status = models.IntegerField(null=True, db_column=u'Status', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'PurchaseOrder'

class Salesorder(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    wo_num = models.CharField(max_length=10, db_column=u'WO_Num', blank=True) # Field name made lowercase.
    link = models.CharField(max_length=10, db_column=u'Link', blank=True) # Field name made lowercase.
    customerkey = models.CharField(max_length=10, db_column=u'CustomerKey', blank=True) # Field name made lowercase.
    customerordernumber = models.CharField(max_length=30, db_column=u'CustomerOrderNumber', blank=True) # Field name made lowercase.
    despatchnotes = models.TextField(db_column=u'DespatchNotes', blank=True) # Field name made lowercase.
    ordervalue = models.CharField(max_length=15, db_column=u'OrderValue', blank=True) # Field name made lowercase.
    status = models.IntegerField(null=True, db_column=u'Status', blank=True) # Field name made lowercase.
    orderdate = models.DateField(null=True, db_column=u'OrderDate', blank=True) # Field name made lowercase.
    despatchdate = models.DateField(null=True, db_column=u'DespatchDate', blank=True) # Field name made lowercase.
    invoicedate = models.DateField(null=True, db_column=u'InvoiceDate', blank=True) # Field name made lowercase.
    operator = models.CharField(max_length=30, db_column=u'Operator', blank=True) # Field name made lowercase.
    despatchcompanyname = models.CharField(max_length=40, db_column=u'DespatchCompanyName', blank=True) # Field name made lowercase.
    despatchaddress1 = models.CharField(max_length=40, db_column=u'DespatchAddress1', blank=True) # Field name made lowercase.
    despatchaddress2 = models.CharField(max_length=40, db_column=u'DespatchAddress2', blank=True) # Field name made lowercase.
    despatchaddress3 = models.CharField(max_length=40, db_column=u'DespatchAddress3', blank=True) # Field name made lowercase.
    despatchpostcode = models.CharField(max_length=15, db_column=u'DespatchPostCode', blank=True) # Field name made lowercase.
    deliverynotecomment1 = models.CharField(max_length=40, db_column=u'DeliveryNoteComment1', blank=True) # Field name made lowercase.
    deliverynotecomment2 = models.CharField(max_length=40, db_column=u'DeliveryNoteComment2', blank=True) # Field name made lowercase.
    deliverynotecomment3 = models.CharField(max_length=40, db_column=u'DeliveryNoteComment3', blank=True) # Field name made lowercase.
    deliverynotecomment4 = models.CharField(max_length=40, db_column=u'DeliveryNoteComment4', blank=True) # Field name made lowercase.
    deliverynotecomment5 = models.CharField(max_length=40, db_column=u'DeliveryNoteComment5', blank=True) # Field name made lowercase.
    invoicecomment1 = models.CharField(max_length=40, db_column=u'InvoiceComment1', blank=True) # Field name made lowercase.
    invoicecomment2 = models.CharField(max_length=40, db_column=u'InvoiceComment2', blank=True) # Field name made lowercase.
    invoicecomment3 = models.CharField(max_length=40, db_column=u'InvoiceComment3', blank=True) # Field name made lowercase.
    invoicecomment4 = models.CharField(max_length=40, db_column=u'InvoiceComment4', blank=True) # Field name made lowercase.
    invoicecomment5 = models.CharField(max_length=40, db_column=u'InvoiceComment5', blank=True) # Field name made lowercase.
    invoicecomment6 = models.CharField(max_length=40, db_column=u'InvoiceComment6', blank=True) # Field name made lowercase.
    invoiceterms = models.CharField(max_length=40, db_column=u'InvoiceTerms', blank=True) # Field name made lowercase.
    itemcount = models.IntegerField(null=True, db_column=u'ItemCount', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'SalesOrder'

class Salesorderadditional(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    parent = models.CharField(max_length=10, db_column=u'Parent', blank=True) # Field name made lowercase.
    haulier = models.CharField(max_length=40, db_column=u'Haulier', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'SalesOrderAdditional'

class Salesorderdespatch(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    key = models.CharField(max_length=10, db_column=u'Key', blank=True) # Field name made lowercase.
    stockcode = models.CharField(max_length=10, db_column=u'StockCode', blank=True) # Field name made lowercase.
    batchdespatched = models.CharField(max_length=10, db_column=u'BatchDespatched', blank=True) # Field name made lowercase.
    despatchedquantity = models.CharField(max_length=15, db_column=u'DespatchedQuantity', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'SalesOrderDespatch'

class Salesorderitem(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    parent = models.CharField(max_length=10, db_column=u'Parent', blank=True) # Field name made lowercase.
    stockcode = models.CharField(max_length=10, db_column=u'StockCode', blank=True) # Field name made lowercase.
    orderquantity = models.CharField(max_length=15, db_column=u'OrderQuantity', blank=True) # Field name made lowercase.
    price = models.CharField(max_length=15, db_column=u'Price', blank=True) # Field name made lowercase.
    requireddate = models.DateField(null=True, db_column=u'RequiredDate', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'SalesOrderItem'

class Supplier(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    supplierid = models.CharField(max_length=10, db_column=u'SupplierID', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=40, db_column=u'Name', blank=True) # Field name made lowercase.
    address1 = models.CharField(max_length=40, db_column=u'Address1', blank=True) # Field name made lowercase.
    address2 = models.CharField(max_length=40, db_column=u'Address2', blank=True) # Field name made lowercase.
    address3 = models.CharField(max_length=40, db_column=u'Address3', blank=True) # Field name made lowercase.
    address4 = models.CharField(max_length=40, db_column=u'Address4', blank=True) # Field name made lowercase.
    address5 = models.CharField(max_length=40, db_column=u'Address5', blank=True) # Field name made lowercase.
    postcode = models.CharField(max_length=10, db_column=u'PostCode', blank=True) # Field name made lowercase.
    telephone = models.CharField(max_length=15, db_column=u'Telephone', blank=True) # Field name made lowercase.
    fax = models.CharField(max_length=15, db_column=u'Fax', blank=True) # Field name made lowercase.
    email = models.CharField(max_length=40, db_column=u'Email', blank=True) # Field name made lowercase.
    website = models.CharField(max_length=40, db_column=u'Website', blank=True) # Field name made lowercase.
    contactname = models.CharField(max_length=40, db_column=u'ContactName', blank=True) # Field name made lowercase.
    vat = models.CharField(max_length=40, db_column=u'VAT', blank=True) # Field name made lowercase.
    comment = models.TextField(db_column=u'Comment', blank=True) # Field name made lowercase.
    memo = models.TextField(db_column=u'Memo', blank=True) # Field name made lowercase.
    lastupdated = models.DateTimeField(null=True, db_column=u'LastUpdated', blank=True) # Field name made lowercase.
    recordno = models.IntegerField(null=True, db_column=u'RecordNo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Supplier'

