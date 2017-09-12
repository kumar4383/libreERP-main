from django.contrib.auth.models import User , Group
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings as globalSettings
# Related to the REST Framework
from rest_framework import viewsets , permissions , serializers
from rest_framework.exceptions import *
from url_filter.integrations.drf import DjangoFilterBackend
from .serializers import *
from API.permissions import *
from django.db.models import Q
from django.http import HttpResponse
from allauth.account.adapter import DefaultAccountAdapter
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from ERP.models import service
# Create your views here.
from reportlab import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors , utils
from reportlab.platypus import Paragraph, Table, TableStyle, Image, Frame, Spacer, PageBreak, BaseDocTemplate, PageTemplate, SimpleDocTemplate, Flowable
from PIL import Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet, TA_CENTER
from reportlab.graphics import barcode , renderPDF
from reportlab.graphics.shapes import *
from reportlab.graphics.barcode.qr import QrCodeWidget
import datetime
import json
import pytz

themeColor = colors.HexColor('#227daa')


styles=getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']

now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

settingsFields = application.objects.get(name = 'app.clientRelationships').settings.all()


class FullPageImage(Flowable):
    def __init__(self , img):
        Flowable.__init__(self)
        self.image = img

    def draw(self):
        img = utils.ImageReader(self.image)

        iw, ih = img.getSize()
        aspect = ih / float(iw)
        width, self.height = PAGE_SIZE
        width -= 3.5*cm
        self.canv.drawImage(os.path.join(BASE_DIR , self.image) , -1 *MARGIN_SIZE + 1.5*cm , -1* self.height + 5*cm , width, aspect*width)

class expanseReportHead(Flowable):

    def __init__(self, request , contract):
        Flowable.__init__(self)
        self.req = request
        self.contract = contract
    #----------------------------------------------------------------------
    def draw(self):
        """
        draw the floable
        """
        print self.contract.status
        if self.contract.status in ['quoted']:
            docTitle = 'SALES QUOTATION'
        elif self.contract.status in ['approved', 'billed' , 'recieved']:
            docTitle = 'TAX INVOICE'

        passKey = '%s%s'%(str(self.req.user.date_joined.year) , self.req.user.pk) # also the user ID
        docID = '%s%s%s' %(self.contract.deal.pk, now.year , self.contract.pk)


        pSrc = '''
        <font size=14>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<u>%s</u></font><br/><br/><br/>
        <font size=9>
        <strong>Generated by:</strong> %s<br/>
        <strong>On:</strong> %s<br/><br/>
        <strong>Document ID:</strong> %s<br/><br/>
        </font>
        ''' % ( docTitle , '%s %s (%s)' %(self.req.user.first_name ,self.req.user.last_name , passKey )  , now.strftime("%d-%B-%Y - %H:%M:%S") , docID)

        story = []
        head = Paragraph(pSrc , styleN)
        head.wrapOn(self.canv , 200*mm, 50*mm)
        head.drawOn(self.canv , 0*mm, -10*mm)

        # barcode_value = "1234567890"
        # barcode39 = barcode.createBarcodeDrawing('EAN13', value = barcode_value,barWidth=0.3*mm,barHeight=10*mm)
        #
        # barcode39.drawOn(self.canv,160*mm,0*mm)
        # self.canv.drawImage(os.path.join(BASE_DIR , 'logo.png') , 80*mm , 0*mm , 2*cm, 2*cm)

def addPageNumber(canvas, doc):
    """
    Add the page number
    """
    print doc.contract
    passKey = '%s%s'%(str(doc.request.user.date_joined.year) , doc.request.user.pk) # also the user ID
    docID = '%s%s%s' %(doc.contract.deal.pk, now.year , doc.contract.pk)

    qrw = QrCodeWidget('http://cioc.co.in/documents?id=%s&passkey=%s&app=crmInvoice' %(docID , passKey))
    b = qrw.getBounds()

    w=b[2]-b[0]
    h=b[3]-b[1]

    d = Drawing(60,60,transform=[60./w,0,0,60./h,0,0])
    d.add(qrw)
    renderPDF.draw(d, canvas ,180*mm,270*mm)

    pass

    # page_num = canvas.getPageNumber()
    # text = "<font size='8'>Page #%s</font>" % page_num
    # p = Paragraph(text , styleN)
    # p.wrapOn(canvas , 50*mm , 10*mm)
    # p.drawOn(canvas , 100*mm , 10*mm)



class PageNumCanvas(canvas.Canvas):

    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    #----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()

    #----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            # self.draw_page_number(page_count)
            self.drawLetterHeadFooter()
            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)


    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """
        Add the page number
        """

        text = "<font size='8'>Page #%s of %s</font>" % (self._pageNumber , page_count)
        p = Paragraph(text , styleN)
        p.wrapOn(self , 50*mm , 10*mm)
        p.drawOn(self , 100*mm , 10*mm)

    def drawLetterHeadFooter(self):
        self.setStrokeColor(themeColor)
        self.setFillColor(themeColor)
        self.rect(0,0,1500,70, fill=True)
        # print dir(self)
        compNameStyle = styleN.clone('footerCompanyName')
        compNameStyle.textColor = colors.white;

        p = Paragraph(settingsFields.get(name = 'companyName').value , compNameStyle)
        p.wrapOn(self , 50*mm , 10*mm)
        p.drawOn(self , 85*mm  , 18*mm)

        p1 = Paragraph(settingsFields.get(name = 'companyAddress').value , compNameStyle)
        p1.wrapOn(self , 150*mm , 10*mm)
        p1.drawOn(self , 55*mm  , 10*mm)


        p2 = Paragraph( settingsFields.get(name = 'contactDetails').value, compNameStyle)
        p2.wrapOn(self , 200*mm , 10*mm)
        p2.drawOn(self , 40*mm  , 4*mm)

        from svglib.svglib import svg2rlg
        drawing = svg2rlg(os.path.join(globalSettings.BASE_DIR , 'static_shared','images' , 'cioc_icon.svg'))
        sx=sy=0.5
        drawing.width,drawing.height = drawing.minWidth()*sx, drawing.height*sy
        drawing.scale(sx,sy)
        #if you want to see the box around the image
        # drawing._showBoundary = True
        renderPDF.draw(drawing, self,10*mm  , self._pagesize[1]-20*mm)

        #width = self._pagesize[0]
        # page = "Page %s of %s" % (, page_count)
        # self.setFont("Helvetica", 9)
        # self.drawRightString(195*mm, 272*mm, page)


def genInvoice(response , contract, request):


    MARGIN_SIZE = 8 * mm
    PAGE_SIZE = A4



    # c = canvas.Canvas("hello.pdf")
    # c.drawString(9*cm, 19*cm, "Hello World!")

    pdf_doc = SimpleDocTemplate(response, pagesize = PAGE_SIZE,
        leftMargin = MARGIN_SIZE, rightMargin = MARGIN_SIZE,
        topMargin = 4*MARGIN_SIZE, bottomMargin = 3*MARGIN_SIZE)

    # data = [['', '', '', 'Grand Total', '' , pFooterGrandTotal]]

    pdf_doc.contract = contract
    pdf_doc.request = request

    tableHeaderStyle = styles['Normal'].clone('tableHeaderStyle')
    tableHeaderStyle.textColor = colors.white;

    pHeadProd = Paragraph('<strong>Product</strong>' , tableHeaderStyle)
    pHeadDetails = Paragraph('<strong>Details</strong>' , tableHeaderStyle)
    pHeadQty = Paragraph('<strong>Qty</strong>' , tableHeaderStyle)
    pHeadPrice = Paragraph('<strong>Rate</strong>' , tableHeaderStyle)
    pHeadTax = Paragraph('<strong>Tax</strong>' , tableHeaderStyle)
    pHeadTotal = Paragraph('<strong>Total</strong>' , tableHeaderStyle)

    # bookingTotal , bookingHrs = getBookingAmount(o)

    pFooterQty = Paragraph('%s' % ('o.quantity') , styles['Normal'])
    pFooterTax = Paragraph('%s' %('tax') , styles['Normal'])
    pFooterTotal = Paragraph('%s' % (1090) , styles['Normal'])
    pFooterGrandTotal = Paragraph('%s' % ('INR 150') , tableHeaderStyle)

    data = [[ pHeadProd, pHeadDetails, pHeadPrice , pHeadQty, pHeadTax , pHeadTotal]]

    totalQuant = 0
    totalTax = 0
    grandTotal = 0

    for i in json.loads(contract.data):
        # print i['desc']
        # print i['quantity']
        # print i['type']
        # print i['tax']
        # print i['rate']
        # print i['total']
        # print i['totalTax']
        # print i['subtotal']

        pDescSrc = '%s <br/> charged at the rate of <strong>%s INR / %s </strong> ' %(i['desc'], i['rate'], i['type'])

        totalQuant += i['quantity']
        totalTax += i['totalTax']
        grandTotal += i['subtotal']

        pBodyProd = Paragraph('Service' , styles['Normal'])
        pBodyTitle = Paragraph( pDescSrc , styles['Normal'])
        pBodyQty = Paragraph(str(i['quantity']) , styles['Normal'])
        pBodyPrice = Paragraph(str(i['rate']) , styles['Normal'])
        pBodyTax = Paragraph(str(i['totalTax']) , styles['Normal'])
        pBodyTotal = Paragraph(str(i['subtotal']) , styles['Normal'])

        data.append([pBodyProd, pBodyTitle, pBodyPrice, pBodyQty, pBodyTax , pBodyTotal])


    data += [['', '', '', '', str(totalTax) , str(grandTotal)],
            ['', '', '',  Paragraph('Grand Total (INR)' , tableHeaderStyle), '' , Paragraph(str(grandTotal) , tableHeaderStyle)]]
    t=Table(data)
    ts = TableStyle([('ALIGN',(1,1),(-3,-3),'RIGHT'),
                ('VALIGN',(0,1),(-1,-3),'TOP'),
                ('VALIGN',(0,-2),(-1,-2),'TOP'),
                ('VALIGN',(0,-1),(-1,-1),'TOP'),
                ('SPAN',(-3,-1),(-2,-1)),
                ('TEXTCOLOR',(0,0),(-1,0) , colors.white),
                ('BACKGROUND',(0,0),(-1,0) , themeColor),
                ('LINEABOVE',(0,0),(-1,0),0.25,themeColor),
                ('LINEABOVE',(0,1),(-1,1),0.25,themeColor),
                ('BACKGROUND',(-2,-2),(-1,-2) , colors.HexColor('#eeeeee')),
                ('BACKGROUND',(-3,-1),(-1,-1) , themeColor),
                ('LINEABOVE',(-2,-2),(-1,-2),0.25,colors.gray),
                ('LINEABOVE',(0,-1),(-1,-1),0.25,colors.gray),
                # ('LINEBELOW',(0,-1),(-1,-1),0.25,colors.gray),
            ])
    t.setStyle(ts)
    t._argW[0] = 3*cm
    t._argW[1] = 8*cm
    t._argW[2] = 2*cm
    t._argW[3] = 2*cm
    t._argW[4] = 2*cm
    t._argW[5] = 2*cm

    #add some flowables



    story = []

    expHead = expanseReportHead(request , contract)
    story.append(Spacer(2.5,2*cm))
    story.append(expHead)
    story.append(Spacer(2.5,0.75*cm))

    adrs = contract.deal.company.address

    summryParaSrc = """
    <font size='11'><strong>Customer details:</strong></font> <br/><br/>
    <font size='9'>
    %s<br/>
    %s<br/>
    %s<br/>
    %s<br/>
    %s , %s<br/>
    %s<br/>
    </font>
    """ %(contract.deal.contacts.all()[0].name , contract.deal.company.name, adrs.street , adrs.city , adrs.state , adrs.pincode , adrs.country)
    story.append(Paragraph(summryParaSrc , styleN))
    story.append(t)
    story.append(Spacer(2.5,0.5*cm))

    if contract.status in ['billed' , 'approved' , 'recieved']:
        summryParaSrc = settingsFields.get(name = 'regulatoryDetails').value
        story.append(Paragraph(summryParaSrc , styleN))

        summryParaSrc = settingsFields.get(name = 'bankDetails').value
        story.append(Paragraph(summryParaSrc , styleN))

        tncPara = settingsFields.get(name = 'tncInvoice').value

    else:
        tncPara = settingsFields.get(name = 'tncQuotation').value

    story.append(Paragraph(tncPara , styleN))

    # scans = ['scan.jpg' , 'scan2.jpg', 'scan3.jpg']
    # for s in scans:
    #     story.append(PageBreak())
    #     story.append(FullPageImage(s))


    pdf_doc.build(story,onFirstPage=addPageNumber, onLaterPages=addPageNumber, canvasmaker=PageNumCanvas)



class DownloadInvoice(APIView):
    renderer_classes = (JSONRenderer,)
    def get(self , request , format = None):
        if 'contract' not in request.GET:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        o = Contract.objects.get(id = request.GET['contract'])
        genInvoice(response , o , request)

        return response

class ContactLiteViewSet(viewsets.ModelViewSet):
    permission_classes = (isOwner , )
    serializer_class = ContactLiteSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'company' , 'mobile', 'email']
    def get_queryset(self):
        return Contact.objects.all()

class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = (isOwner , )
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name']
    def get_queryset(self):
        return Contact.objects.all()

class DealLiteViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly , readOnly, )
    serializer_class = DealLiteSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'result', 'company']
    def get_queryset(self):
        return Deal.objects.filter(active = True)

class DealViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated , )
    serializer_class = DealSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'state', 'result', 'company']
    def get_queryset(self):

        if 'created' in self.request.GET and 'won' in self.request.GET and 'lost' in self.request.GET:
            qs1 , qs2 , qs3 = Deal.objects.none(), Deal.objects.none(), Deal.objects.none()
            if self.request.GET['created'] == '1':
                qs1 = Deal.objects.filter(state = 'created')
            if self.request.GET['won'] == '1':
                qs2 = Deal.objects.filter(result = 'won')
            if self.request.GET['lost'] == '1':
                qs2 = Deal.objects.filter(result = 'lost')

            toReturn = qs1 | qs2 | qs3
        else:
            toReturn = Deal.objects.all()

        # print self.request.GET
        # print toReturn

        toReturn = toReturn.filter(active = True)
        if 'company__contains' in self.request.GET:
            comName = self.request.GET['company__contains']
            toReturn = toReturn.filter(company__in = service.objects.filter(name__contains=comName))

        if 'created' in self.request.GET and self.request.GET['created'] == 'false':
            toReturn = toReturn.exclude(state = 'created')

        if 'board' in self.request.GET:
            toReturn = toReturn.filter(result = 'na')

        return toReturn

class RelationshipViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly , readOnly , )
    serializer_class = RelationshipSerializer
    def get_queryset(self):
        return service.objects.filter(deals__in = Deal.objects.filter(active = True).filter(result='won')).distinct()

class ContractViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated  , )
    serializer_class = ContractSerializer
    def get_queryset(self):
        return Contract.objects.all()

class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = (isOwner , )
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['contact' , 'deal', 'notes' , 'data']
    def get_queryset(self):
        return Activity.objects.order_by('-created')
