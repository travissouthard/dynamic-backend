from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from backend.settings import MEDIA_URL
from .models import Art, Blog, Project

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
        image_url = "/blog/travis-flowers.jpg"
        context = {
            "name": page_name,
            "desc": "A page by Travis Southard",
            "image": image_url,
            "image_type": image_url.split(".")[-1],
            "width": "600",
            "height": "450",
            "alt": "Travis in a field of flowers"
            }
        return HttpResponse(template.render(context, request))
    except:
        return four_oh_four(request)

def home_view(request):
    template = loader.get_template("list-main.html")

    posts = [a for a in Art.objects.all()] + [b for b in Blog.objects.all()] + [p for p in Project.objects.all()]
    posts = sorted(posts, key = lambda x: x.published, reverse=True)

    context = {"name": "Home", "post_list": posts, "media_url": MEDIA_URL}
    return HttpResponse(template.render(context, request))

def list_view(request, name):
    models = {
        "art": Art,
        "blog": Blog,
        "projects": Project
    }
    template = loader.get_template("list-main.html")
    posts = [x for x in models[name].objects.all()]
    page_name = name[0].upper() + name[1:]
    context = {"name": page_name, "post_list": posts, "media_url": MEDIA_URL}
    return HttpResponse(template.render(context, request))

def post_view(request, post_type, slug):
    models = {
        "art": Art,
        "blog": Blog,
        "projects": Project
    }
    if post_type not in ["art", "blog", "projects"]:
        return four_oh_four(request)
    template = loader.get_template("post-main.html")

    post = models[post_type].objects.get(slug=slug)

    context = {"name": post.title, "post": post, "media_url": MEDIA_URL}
    return HttpResponse(template.render(context, request))

def rss_view(request, _):
    template = loader.get_template("rss.xml")
    posts = [a for a in Art.objects.all()] + [b for b in Blog.objects.all()] + [p for p in Project.objects.all()]
    posts = sorted(posts, key = lambda x: x.published, reverse=True)
    context = {"post_list": posts}
    return HttpResponse(template.render(context, request))