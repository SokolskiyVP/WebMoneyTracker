from django.shortcuts import render

def home(request):
    return render(request, 'main/Home.html')

def tinkoff(request):
    return render(request, 'main/')




