from django.shortcuts import render


# Create your views here.


def chat(request, *args, **kwargs):
    return render(request, 'front/index.html')
