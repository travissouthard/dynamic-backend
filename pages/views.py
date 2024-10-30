from django.http import HttpResponse
from django.template import loader

def homeView(request):
    template = loader.get_template("home.html")
    context = {"name": "Home"}
    return HttpResponse(template.render(context, request))

def aboutView(request):
    template = loader.get_template("about.html")
    context = {"name": "About"}
    return HttpResponse(template.render(context, request))