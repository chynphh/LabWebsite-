from django.shortcuts import render


def home(request):
    return render(request, 'htmltest/home-page-1.html')
