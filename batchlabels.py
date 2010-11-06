""" batchlabels.py  -- Create Batch Labels.

Given a batch number this script will generate a pdf document with the Batch,
Material Description and Quantity added. This can then be printed onto A4
labels.
"""

from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

import naphthabase as nb

headingStyle = ParagraphStyle('Heading')
headingStyle.fontName = 'Times-Bold'
headingStyle.fontSize = 36
headingStyle.leading = 1.2 * 36
batchStyle = ParagraphStyle('Batch', headingStyle)
batchStyle.fontSize = 85
batchStyle.leading = 1.2 * 85
materialStyle = ParagraphStyle('MaterialDesc', headingStyle)
materialStyle.fontSize = 48
materialStyle.leading = 1.2 * 48
materialStyle.fontName = 'Times-Roman'
quantityStyle = ParagraphStyle('Quantity', materialStyle)
quantityStyle.fontSize = 60
quantityStyle.leading = 1.2 * 60
 
def create_label_pdf(batchnum, matdesc, quant):
    c = Canvas("batchlabel.pdf", A4)
    c.setLineWidth(0.12 * cm) # set underline width
    
    leftpos = 2.42*cm
    origin = 0
    
    frameBatchHeading = Frame(leftpos, origin+12.76*cm, 5.2*cm, 2.0*cm, showBoundary=0)
    p = Paragraph("<u>BATCH:</u>", headingStyle)   
    frameBatchHeading.addFromList([p],c)
    
    frameBatchDesc = Frame(leftpos+9*cm, origin+10.35*cm, 8*cm, 4.5*cm, showBoundary=0)
    p = Paragraph("%s" % (batchnum), batchStyle)
    frameBatchDesc.addFromList([p],c)
    
    frameMaterialHeading = Frame(leftpos, origin+9.59*cm, 7.8*cm, 2.0*cm, showBoundary=0)
    p = Paragraph("<u>MATERIAL:</u>", headingStyle)
    frameMaterialHeading.addFromList([p],c)
    
    frameMaterialDesc = Frame(leftpos, origin+3*cm, 18*cm, 6.8*cm, showBoundary=0)
    p = Paragraph("%s" % (matdesc), materialStyle)
    frameMaterialDesc.addFromList([p],c)
    
    frameQuantHeading = Frame(leftpos, origin+1.57*cm, 7.6*cm, 2.0*cm, showBoundary=0)
    p = Paragraph("<u>QUANTITY:</u>", headingStyle)   
    frameQuantHeading.addFromList([p],c)
    
    frameQuantDesc = Frame(leftpos+9.08*cm, origin+0.9*cm, 8.96*cm, 3*cm, showBoundary=0)
    p = Paragraph("%s KG" % (quant), quantityStyle)
    frameQuantDesc.addFromList([p],c)
    
    
    origin = 14.3*cm
    
    frameBatchHeading1 = Frame(leftpos, origin+12.76*cm, 5.2*cm, 2.0*cm, showBoundary=0)
    p = Paragraph("<u>BATCH:</u>", headingStyle)   
    frameBatchHeading1.addFromList([p],c)
    
    frameBatchDesc1 = Frame(leftpos+9*cm, origin+10.35*cm, 8*cm, 4.5*cm, showBoundary=0)
    p = Paragraph("%s" % (batchnum), batchStyle)
    frameBatchDesc1.addFromList([p],c)
    
    frameMaterialHeading1 = Frame(leftpos, origin+9.59*cm, 7.8*cm, 2.0*cm, showBoundary=0)
    p = Paragraph("<u>MATERIAL:</u>", headingStyle)
    frameMaterialHeading1.addFromList([p],c)
    
    frameMaterialDesc1 = Frame(leftpos, origin+3*cm, 18*cm, 6.8*cm, showBoundary=0)
    p = Paragraph("%s" % (matdesc), materialStyle)
    frameMaterialDesc1.addFromList([p],c)
    
    frameQuantHeading1 = Frame(leftpos, origin+1.57*cm, 7.6*cm, 2.0*cm, showBoundary=0)
    p = Paragraph("<u>QUANTITY:</u>", headingStyle)   
    frameQuantHeading1.addFromList([p],c)
    
    frameQuantDesc1 = Frame(leftpos+9.08*cm, origin+0.9*cm, 8.96*cm, 3*cm, showBoundary=0)
    p = Paragraph("%s KG" % (quant), quantityStyle)
    frameQuantDesc1.addFromList([p],c)
    
    
    c.save()
    
if __name__ == "__main__":
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print " PRINT BATCH LABELS"
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "\n\n"
    print "Enter Batch Number:"
    z=raw_input()
    if z == '':
        z = '21964'
    try:
        batchnum=int(z)
    except:
        print "bye"
    matcode = nb.MaterialCodes()
    stock = nb.Stock()
    details = stock.get_dict(batchnum)
    print details
    details = details[0]
    if details['BatchStatus'] == 'E':
        print 'Batch is empty'
    else:
        batchnum = str(batchnum)
        matdesc = matcode.get_mat(details['Code'])
        quant  = details['QuantityNow']
        print batchnum, matdesc, quant
        create_label_pdf(batchnum, matdesc, quant)
