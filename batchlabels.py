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

def create_label(filename, label_template):
    c = Canvas(filename, A4)
    c.setLineWidth(0.12 * cm) # set underline width 
    for frame_item in label_template:
        x, y, l, h = frame_item['x'], frame_item['y'], \
                     frame_item['l'], frame_item['h']
        style = frame_item['style']
        text = frame_item['text']
        frame = Frame(x*cm, y*cm, l*cm, h*cm, showBoundary = 0)
        p = Paragraph(text, style)
        frame.addFromList([p], c)
    c.save()
    
def create_label_pdf(batchnum, matdesc, quant):
    leftpos = 2.42
    label_template = []
    for origin in [0, 14.3]:
        label_template = label_template + [
        {'name': 'frameBatchHeading', 'style': headingStyle,
        'x': leftpos, 'y': origin+12.76, 'l': 5.2, 'h': 2.0,
        'text': "<u>BATCH:</u>"},
        {'name': 'frameBatchDesc', 'style': batchStyle,
        'x': leftpos+9, 'y': origin+10.35, 'l': 8, 'h': 4.5,
        'text': "%s" % (batchnum)},
        {'name': 'frameMaterialHeading', 'style': headingStyle,
        'x': leftpos, 'y': origin+9.59, 'l': 7.8, 'h': 2.0,
        'text': "<u>MATERIAL:</u>"},
        {'name': 'frameMaterialDesc', 'style': materialStyle,
        'x': leftpos, 'y': origin+3, 'l': 18, 'h': 6.8,
        'text': "%s" % (matdesc)},
        {'name': 'frameQuantHeading', 'style': headingStyle,
        'x': leftpos, 'y': origin+1.57, 'l': 7.6, 'h':2.0,
        'text': "<u>QUANTITY:</u>"},
        {'name': 'frameQuantDesc', 'style': quantityStyle,
        'x': leftpos+9.08, 'y': origin+0.9, 'l': 8.96, 'h': 3,
        'text': "%s KG" % (quant)}] 
    create_label('batchlabel.pdf', label_template)

    
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
    details = stock.get_dict(batchnum)[0]
    if details['BatchStatus'] == 'E':
        print 'Batch is empty'
    else:
        batchnum = str(batchnum)
        matdesc = matcode.get_mat(details['Code'])
        quant  = details['QuantityNow']
        print '\nBatch:', batchnum
        print 'Material:', matdesc
        print 'Quantity:', quant
        print '\n\nEnter new weight or press return to use %s KG' % quant
        new_weight = raw_input()
        if new_weight != '':
            quant = int(new_weight)
            print '\nUsing %s KG' % quant
            
        create_label_pdf(batchnum, matdesc, quant)
