from django.shortcuts import render
from profiles.models import Profile #used for setting author of report
from django.contrib.auth.models import User
from django.http import JsonResponse
from .utils import get_report_image
from .models import Report
from django.views.generic import ListView, DetailView
# Create your views here.

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