from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

def four_oh_four(request):
    template = loader.get_template("fourohfour.html")
    context = {"name": "404"}
    response = HttpResponse(template.render(context, request))
    response.status_code = 404
    return response

def redirect_old_html_links(_, route):
    return HttpResponseRedirect(route)

def general_view(request, name):
    try:
        if name == "index":
            return HttpResponseRedirect("/")
        if name in ["art", "blog", "projects"]:
            return list_view(request, name)
        template = loader.get_template(f"{name}.html")
        page_name = name[0].upper() + name[1:]
        context = {"name": page_name}
        return HttpResponse(template.render(context, request))
    except:
        return four_oh_four(request)

def home_view(request):
    template = loader.get_template("list-main.html")
    context = {"name": "Home", "post_list": []}
    return HttpResponse(template.render(context, request))

def list_view(request, name):
    template = loader.get_template("list-main.html")
    page_name = name[0].upper() + name[1:]
    context = {"name": page_name, "post_list": ["one", "two", "three"]}
    return HttpResponse(template.render(context, request))

def post_view(request, post_type, slug):
    if post_type not in ["art", "blog", "projects"]:
        return four_oh_four(request)
    template = loader.get_template("post-main.html")
    page_name = slug[0].upper() + slug[1:]
    context = {"name": page_name, "post": post_type}
    return HttpResponse(template.render(context, request))

def rss_view(request, _):
    template = loader.get_template("rss.xml")
    context = {}
    return HttpResponse(template.render(context, request))