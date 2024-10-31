from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

def redirect_old_html_links(_, route):
    return HttpResponseRedirect(route)

def home_view(request):
    template = loader.get_template("home.html")
    context = {"name": "Home"}
    return HttpResponse(template.render(context, request))

def about_view(request):
    template = loader.get_template("about.html")
    context = {"name": "About"}
    return HttpResponse(template.render(context, request))

def project_list_view(request):
    template = loader.get_template("projects.html")
    context = {"name": "Projects"}
    return HttpResponse(template.render(context, request))

def art_list_view(request):
    template = loader.get_template("art.html")
    context = {"name": "Art"}
    return HttpResponse(template.render(context, request))

def blog_list_view(request):
    template = loader.get_template("blog.html")
    context = {"name": "Blog"}
    return HttpResponse(template.render(context, request))

def webring_view(request):
    template = loader.get_template("webring.html")
    context = {"name": "Webring"}
    return HttpResponse(template.render(context, request))

def resume_view(request):
    template = loader.get_template("resume.html")
    context = {"name": "Resume"}
    return HttpResponse(template.render(context, request))

def rss_view(request):
    template = loader.get_template("rss.xml")
    context = {}
    return HttpResponse(template.render(context, request))