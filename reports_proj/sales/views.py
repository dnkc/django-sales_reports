from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
import pandas as pd
# Create your views here.


# IN TEMPLATES FOLDER, THE FOLDER SHOULD BE SAME NAME AS APP

def home_view(request):
    form = SalesSearchForm(request.POST or None)
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        #print(date_from, date_to, chart_type)
        qs = Sale.objects.filter(created__date=date_from)
        print('##################')
        df1 = pd.DataFrame(qs.values())
        print(df1)

    context = {
        'form': form
    }
    return render(request, 'sales/home.html', context) # with dictionary can specify what you want to pass to template

class SaleListView(ListView): #class based view
    # need to specify model and template_name
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'

'''
HOW TO CREATE FUNCTION VIEWS OUT OF THE ABOVE CLASS BASED VIEWS:

class SaleListView(LoginRequiredMixin, ListView):
	model = Sale
	template_name = 'sales/main.html'

class SaleDetailView(LoginRequiredMixin, DetailView):
	model = Sale
	template_name = 'sales/detail.html'

def sale_list_view(request):
	qs = Sale.objects.all()
	return render(request, 'sales/main.html', {'object_list': qs})

def sale_detail_view(request, **kwargs):
    pk = kwargs.get('pk')
	obj = Sale.objects.get(pk=pk)
	# or
	# obj = get_object_or_404(Sale, pk=pk)
	return render(request, 'sales/detail.html', {'object':obj})
'''

'''
in the urls:
path('sales/', sale_list_view, name='list'),
path ('sales/<pk>', sale_detail_view, name='detail'),
'''