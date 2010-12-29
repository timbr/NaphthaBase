# Create your views here.
from django.http import HttpResponse
from nappy.models import PurchaseOrder, PurchaseItem, Stock, SalesOrder, SalesItem, DeletedSales, Customer, Supplier, Contact, Depot, Material
from django.template import Context, loader
from decimal import Decimal


def po(request):
    latest_purchase_orders = PurchaseOrder.objects.all().filter(orderdate__gt='2010-11-01').order_by('-pon')
    po_list = [entry.pon for entry in latest_purchase_orders]
    t = loader.get_template('index.html')
    
    purchase_items = (PurchaseItem.objects.filter(pon__in = po_list))
    
    c = Context({'latest_purchase_orders': latest_purchase_orders,
    'purchase_items': purchase_items})
    
    
    print purchase_items
    return HttpResponse(t.render(c))

def singlepo(request, po_num):
    po = PurchaseOrder.objects.filter(pon = po_num)
    if len(po) != 1:
        return HttpResponse("PO number %s has %s records in the database" % (po_num, len(po)))
    po = po[0]
    print po
    t = loader.get_template('PurchaseOrder.html')
    c = Context({'po': po, 'links': {'prev': int(po_num) - 1, 'next': int(po_num) + 1}})
    return HttpResponse(t.render(c))

def singlebatch(request, batch_num):
    batch = Stock.objects.filter(batch = batch_num)
    if len(batch) != 1:
        return HttpResponse("Batch number %s has %s records in the database" % (batch_num, len(batch)))
    batch = batch[0]
    print batch
    if batch.purchaseitem != None:
        handling = Decimal(batch.costprice) - Decimal(batch.purchaseitem.price)
        if handling != Decimal('0.045'):
            chargecolor = '#FF0000'
        else:
            chargecolor = '#00FF00'
    else:
        handling = ''
        chargecolor = ''
    t = loader.get_template('Batch.html')
    c = Context({'batch': batch, 'links': {'prev': int(batch_num) - 1, 'next': int(batch_num) + 1}, 'other': {'handling': handling, 'chargecolor': chargecolor}})
    return HttpResponse(t.render(c))

def singlewo(request, wo_num):
    missingwo = DeletedSales.objects.filter(won = wo_num)
    wo = SalesOrder.objects.filter(won = wo_num)
    if len(wo) != 1:
        if len(missingwo) == 1:
            return HttpResponse("Sales order %s has been deleted by %s because:  %s" % (wo_num, missingwo[0].operator, missingwo[0].reason))
        else:
            return HttpResponse("Sales Order number %s has %s records in the database" % (wo_num, len(wo)))
    wo = wo[0]
    print wo
    t = loader.get_template('SalesOrder.html')
    c = Context({'wo': wo, 'links': {'prev': int(wo_num) - 1, 'next': int(wo_num) + 1}})
    return HttpResponse(t.render(c))

def singlecustomer(request, customer_code):
    customer = Customer.objects.filter(customer_code = customer_code.upper())
    if len(customer) != 1:
        return HttpResponse("Customer code %s has %s records in the database" % (customer_code, len(customer)))
    customer = customer[0]
    t = loader.get_template('Customer.html')
    c = Context({'customer': customer})
    return HttpResponse(t.render(c))

def singlesupplier(request, supplier_code):
    supplier = Supplier.objects.filter(supplier_code = supplier_code.upper())
    if len(supplier) != 1:
        return HttpResponse("Supplier code %s has %s records in the database" % (supplier_code, len(supplier)))
    supplier = supplier[0]
    t = loader.get_template('Supplier.html')
    c = Context({'supplier': supplier})
    return HttpResponse(t.render(c))

def singlematerial(request, material_code):
    material = Material.objects.filter(code = material_code.upper())
    if len(material) != 1:
        return HttpResponse("Material code %s has %s records in the database" % (material_code, len(material)))
    material = material[0]
    instock = material.stock_set.all().filter(status = 'S').order_by('-batch')
    purchases = material.purchaseitem_set.all().order_by('-pon')[:10]
    sales = material.salesitem_set.all().order_by('-won')[:10]
    t = loader.get_template('Material.html')
    c = Context({'instock': instock, 'material': material, 'purchases': purchases, 'sales' : sales})
    return HttpResponse(t.render(c))