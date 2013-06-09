from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def problems_page(request):
    return render(request, 'problems.html')
