from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
# Create your views here.


# IN TEMPLATES FOLDER, THE FOLDER SHOULD BE SAME NAME AS APP

def home_view(request):
    hello = 'hello world from the view'
    return render(request, 'sales/home.html', {'h': hello}) # with dictionary can specify what you want to pass to template

class SaleListView(ListView): #class based view
    # need to specify model and template_name
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'