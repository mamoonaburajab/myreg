
from django.http import HttpResponse

def home(request):
    return HttpResponse("Home Page")

def user(request):
    return HttpResponse("User Page")

def about(request):
    return HttpResponse("About Page")
from django.shortcuts import render

def main(request):
    return render(request, 'main.html')
