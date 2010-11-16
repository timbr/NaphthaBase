from nappy.models import Additionalitems, Contact, Customer, Depot, Formula, Formulastock
from django.contrib import admin


class AdditionalitemsAdmin(admin.ModelAdmin):
    list_display = ('haulierkey', 'name', 'nominalcode', 'lastupdated')

admin.site.register(Additionalitems, AdditionalitemsAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('clientid', 'forename', 'surname', 'phone', 'department', 'lastupdated')
    search_fields = ['clientid', 'forename', 'surname']

admin.site.register(Contact, ContactAdmin)


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,       {'fields': ['customerid', 'name']}),
        ('Contact',  {'fields': ['contactname', 'telephone', 'fax', 'email', 'website']}),
        ('Address',  {'fields': ['address1', 'address2', 'address3', 'address4', 'address5', 'postcode']}),
        ('Comments',  {'fields': ['comment', 'memo']}),
        ('Record',    {'fields': ['id', 'recordno', 'lastupdated']})
        ]
    
    list_display = ('customerid', 'name', 'telephone', 'contactname', 'lastupdated')
    search_fields = ['customerid', 'name']

admin.site.register(Customer, CustomerAdmin)


class DepotAdmin(admin.ModelAdmin):
    list_display = ['clientid', 'name', 'lastupdated']

admin.site.register(Depot, DepotAdmin)


class FormulaAdmin(admin.ModelAdmin):
    list_display = ['code', 'description', 'lastupdated']
    search_fields = ['code', 'description']

admin.site.register(Formula, FormulaAdmin)


class FormulastockAdmin(admin.ModelAdmin):
    list_display = ['batch', 'stockinfo', 'batchstatus', 'quantitynow', 'supplier', 'ponumber', 'lastupdated']
    search_fields = ['batch', 'stockinfo', 'ponumber']
    list_filter = ['batchstatus']

admin.site.register(Formulastock, FormulastockAdmin)