import pyodbc
import optparse
from subprocess import Popen, PIPE
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

def main():
    p = optparse.OptionParser(description = 'Prints batch labels for a given batch.',
                              usage = '%prog <batchnumber> [weight]')
    p.add_option('-p', '--printnow', action ='store_true', help='prints the generated pdf')
    p.add_option('-s', '--showpdf', action ='store_true', help='displays the generated pdf')

    options, arguments = p.parse_args()
    if len(arguments) > 0:
        data = getstockinfo(arguments[0])
        if data != None:
            if len(arguments) == 1:
                print 'Batch: %s' % data.BatchNo
                print 'Description: %s' % data.Material
                print 'Quantity: %sKg' % data.Quantity
                print '\n\n'
                print 'Enter label weight (or press enter to use %sKg): ' % data.Quantity
                weight = raw_input()
                if weight == '':
                    weight = data.Quantity
            else:
                weight = arguments[1]
            create_label_pdf(data.BatchNo, data.Material, weight)
            if options.showpdf:
                cmd = '"c:\\Program Files\\Foxit Software\\Foxit Reader\\Foxit Reader.exe" batchlabel.pdf'
                proc = Popen(cmd, stdin = PIPE, stdout = PIPE, stderr = PIPE)
                cmdout, cmderr = proc.communicate()
                print cmdout
                print cmderr
            if options.printnow:
                cmd = '"c:\\Program Files\\Foxit Software\\Foxit Reader\\Foxit Reader.exe" /p batchlabel.pdf'
                proc = Popen(cmd, stdin = PIPE, stdout = PIPE, stderr = PIPE)
                cmdout, cmderr = proc.communicate()
                print cmdout
                print cmderr
        else:
            print 'Batch Number %s not found.' % arguments[0]
    else:
        p.print_help()
    
def getstockinfo(batchnumber):
    global data
    query = """
    SELECT
    Formula.Description AS Material,
    \"Formula Stock\".Batch AS BatchNo,
    \"Formula Stock\".Location AS StockInfo,
    \"Formula Stock\".Quantity
    FROM \"Formula Stock\" INNER JOIN Formula ON \"Formula Stock\".Key = Formula.Key
    WHERE Formula.\"Customer Key\" <> 'ANY'
    AND \"Formula Stock\".Batch = '%(batch)s'
    """
    naphthav6 = "S:\\NAPHTHAV6\\DATA\\Naphtha.mdb"
    dbconnection = pyodbc.connect(DRIVER = '{Microsoft Access Driver (*.mdb)}', DBQ = naphthav6)
    dbcursor = dbconnection.cursor()
    data = dbcursor.execute(query % {'batch': batchnumber})
    return data.fetchone()

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
    

if __name__ == '__main__':
    main()