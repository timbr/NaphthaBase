import pyodbc
import optparse
from subprocess import Popen, PIPE
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

def main():
    p = optparse.OptionParser(description = 'Prints despatch label for a given customer.',
                              usage = '%prog <customer>')
    p.add_option('-p', '--printnow', action ='store_true', help='prints the generated pdf')

    options, arguments = p.parse_args()
    if len(arguments) == 1:
        data = getcustomeraddress(arguments[0])
        print data
        create_label_pdf(data.BatchNo, data.Material, weight)
        if options.printnow:
           cmd = '"c:\\Program Files\\Foxit Software\\Foxit Reader\\Foxit Reader.exe" /p batchlabel.pdf'
           proc = Popen(cmd, stdin = PIPE, stdout = PIPE, stderr = PIPE)
           cmdout, cmderr = proc.communicate()
           print cmdout
           print cmderr
    else:
        p.print_help()
    
def getcustomeraddress(customer):
    query = """
    SELECT
    Customer.Name,
    Customer.Address1,
    Customer.Address2,
    Customer.Address3,
    Customer.Address4,
    Customer.Address5,
    Customer.\"Post Code\" AS PostCode
    FROM Customer
    WHERE Customer.ID = '%(customer)s'
    """
    accountsDB = "S:\\NAPHTHAV6\\DATA\\Naphtha_accounts.mdb"
    accountsDBpassword = "bgSoiqOogNMOH"
    dbconnection = pyodbc.connect(DRIVER = '{Microsoft Access Driver (*.mdb)}', DBQ = accountsDB, PWD = accountsDBpassword)
    dbcursor = dbconnection.cursor()
    data = dbcursor.execute(query % {'customer': customer.upper()})
    d = data.fetchone()
    cleanup = [line.strip(',').strip('.') for line in d if len(line) > 0]
    if len(cleanup[0]) > 28:
        cleanup[0] = cleanup[0][:28]
    if len(cleanup[1]) + len(cleanup[2]) < 25:
        cleanup[1] = ', '.join(cleanup[1:3])
        cleanup.pop(2)
    return '\n'.join(cleanup)
    

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

def create_label_pdf(from_address, to_address, service):
    headingStyle = ParagraphStyle('Heading')
    headingStyle.fontName = 'Times-Bold'
    headingStyle.fontSize = 20
    headingStyle.leading = 1.2 * 36
    batchStyle = ParagraphStyle('Batch', headingStyle)
    batchStyle.fontSize = 22
    batchStyle.leading = 1.2 * 85
    materialStyle = ParagraphStyle('MaterialDesc', headingStyle)
    materialStyle.fontSize = 22
    materialStyle.leading = 1.2 * 48
    materialStyle.fontName = 'Times-Roman'
    quantityStyle = ParagraphStyle('Quantity', materialStyle)
    quantityStyle.fontSize = 20
    quantityStyle.leading = 1.2 * 60
    leftpos = 1
    label_template = []
    for origin in [0, 14.3]:
        label_template = label_template + [
        {'name': 'frameBatchHeading', 'style': headingStyle,
        'x': leftpos, 'y': origin+12.76, 'l': 5.2, 'h': 2.0,
        'text': "From:"},
        {'name': 'frameBatchDesc', 'style': batchStyle,
        'x': leftpos+9, 'y': origin+10.35, 'l': 8, 'h': 4.5,
        'text': "%s" % (from_address)},
        {'name': 'frameMaterialHeading', 'style': headingStyle,
        'x': leftpos, 'y': origin+9.59, 'l': 7.8, 'h': 2.0,
        'text': "Deliver To:"},
        {'name': 'frameMaterialDesc', 'style': materialStyle,
        'x': leftpos, 'y': origin+3, 'l': 18, 'h': 6.8,
        'text': "%s" % (to_address)},
        {'name': 'frameQuantHeading', 'style': headingStyle,
        'x': leftpos, 'y': origin+1.57, 'l': 7.6, 'h':2.0,
        'text': "QUANTITY:"},
        {'name': 'frameQuantDesc', 'style': quantityStyle,
        'x': leftpos+9.08, 'y': origin+0.9, 'l': 8.96, 'h': 3,
        'text': "%s KG" % (service)}] 
    create_label('despatchlabel.pdf', label_template)
    

if __name__ == '__main__':
    main()