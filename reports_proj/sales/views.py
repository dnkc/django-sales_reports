from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
import pandas as pd
# Create your views here.
from .utils import get_salesman_from_id, get_customer_from_id, get_chart
from reports.forms import ReportForm
# IN TEMPLATES FOLDER, THE FOLDER SHOULD BE SAME NAME AS APP
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def home_view(request):
    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    no_data = None
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')

        #print(date_from, date_to, chart_type)
        sale_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sale_qs) > 0:
            sales_df = pd.DataFrame(sale_qs.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id) # returns
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%y-%m-%d'))
            sales_df['updated'] = sales_df['updated'].apply(lambda x: x.strftime('%y-%m-%d'))
            sales_df.rename({'customer_id': 'Customer', 'salesman_id':'Salesperson', 'id': 'sales_id'}, axis=1, inplace=True)
            #sales_df['sales_id'] = sales_df['id']
            # need to set dataframe to HTML to display
            positions_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id(),
                    }
                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)

            #combining sales and positions df
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')

            df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')

            chart = get_chart(chart_type, sales_df, results_by)

            positions_df = positions_df.to_html()
            sales_df = sales_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()

        else:
            no_data = 'No data is available in this date range.'

    context = {
        'search_form': search_form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df': df,
        'chart': chart,
        'report_form': report_form,
        'no_data': no_data,
    }
    return render(request, 'sales/home.html', context) # with dictionary can specify what you want to pass to template

class SaleListView(LoginRequiredMixin, ListView): #class based view
    # need to specify model and template_name
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(LoginRequiredMixin, DetailView):
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