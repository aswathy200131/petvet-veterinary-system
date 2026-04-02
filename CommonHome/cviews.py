from django.shortcuts import render,HttpResponse,HttpResponseRedirect

from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")

