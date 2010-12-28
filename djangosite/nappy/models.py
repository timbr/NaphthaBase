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