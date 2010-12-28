# Create your views here.
from django.http import HttpResponse
from nappy.models import PurchaseOrder, PurchaseItem, Stock
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