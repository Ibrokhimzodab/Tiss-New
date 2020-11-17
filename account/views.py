from django.shortcuts import render

# Create your views here.
def f(request):
    return render(request, template_name="index.html")
