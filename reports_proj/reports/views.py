from django.shortcuts import render, get_object_or_404
from profiles.models import Profile #used for setting author of report
from django.contrib.auth.models import User
from django.http import JsonResponse
from .utils import get_report_image
from .models import Report
from django.views.generic import ListView, DetailView, TemplateView
# Create your views here.

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from sales.models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer
import csv
from django.utils.dateparse import parse_date
from datetime import datetime
from django.utils.timezone import make_aware
def create_report_view(request):
    if request.is_ajax():
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')
        ####################################################
        get_author = User.objects.filter(username='testuser')[0].id
        get_author = str(get_author)
        #################### DELETE get_author, implement below comment
        author = Profile.objects.get(user=get_author)
        # author = Profile.objects.get(user=request.user)
        ###########################################################
        img = get_report_image(image)

        Report.objects.create(
            name=name,
            remarks=remarks,
            image=img,
            author=author,
        )

        return JsonResponse({'msg': 'send'})
    return JsonResponse()

class ReportListView(ListView): #class based view
    # need to specify model and template_name
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'

def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if display
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

class UploadTemplateView(TemplateView):
    template_name = 'reports/from_file.html'


def csv_upload_view(request):
    #print('file is being sent')
    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file') # from html input name="file"
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)
        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    transaction_id = row[1]
                    product = row[2]
                    quantity = int(row[3])
                    customer = row[4]
                    date = str(parse_date(row[5]))
                    date = make_aware(datetime.strptime(date, '%Y-%m-%d'))
                    try:
                        product_obj = Product.objects.get(name__iexact=product) #iexact = ignores case sensitivity
                    except Product.DoesNotExist:
                        product_obj = None

                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        # if creating, _ = True, if already exists _ = False
                        get_salesman = User.objects.filter(username='testuser')[0].id
                        get_salesman = str(get_salesman)
                        salesman_obj = Profile.objects.get(user=get_salesman)
                        positions_obj = Position.objects.create(product=product_obj,
                                                                quantity=quantity,
                                                                created=date
                                                                )
                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj,
                                                                 salesman=salesman_obj, created=date,
                                                                 )
                        sale_obj.positions.add(positions_obj)
                        sale_obj.save()
                return JsonResponse({'ex': False})
        else:
            return JsonResponse({'ex': True})
    return HttpResponse()