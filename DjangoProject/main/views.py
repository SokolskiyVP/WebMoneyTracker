from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render

@login_required
def home(request):
    return render(request, 'main/Home.html')
@login_required
def tinkoff(request):
    return render(request, 'main/')

def page_not_found(request, exception):

    return HttpResponseNotFound('404/')


