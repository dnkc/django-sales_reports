from django.shortcuts import render

# Create your views here.


# IN TEMPLATES FOLDER, THE FOLDER SHOULD BE SAME NAME AS APP

def home_view(request):
    hello = 'hello world from the view'
    return render(request, 'sales/main.html', {'h': hello}) # with dictionary can specify what you want to pass to template