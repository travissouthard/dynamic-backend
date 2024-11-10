import re
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.syndication.views import Feed

from backend.settings import MEDIA_URL
from .models import Art, Blog, Project

CONTEXT = {
    "name": "Home",
    "desc": "A page by Travis Southard",
    "image": "/blog/travis-flowers.jpg",
    "image_type": "jpg",
    "width": "600",
    "height": "450",
    "alt": "Travis in a field of flowers",
    "media_url": MEDIA_URL,
}

def _capitalize(s):
    return s[0].upper() + s[1:]

def four_oh_four(request):
    template = loader.get_template("fourohfour.html")
    
    context = CONTEXT
    context["name"] = "404"

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
        
        context = CONTEXT
        context["name"] = _capitalize(name)
        return HttpResponse(template.render(context, request))
    except:
        return four_oh_four(request)

def home_view(request):
    template = loader.get_template("list-main.html")

    posts = Art.objects.all().union(Blog.objects.all(), Project.objects.all()).order_by("-published")

    context = CONTEXT
    context["post_list"] = posts

    return HttpResponse(template.render(context, request))

def list_view(request, name):
    models = {
        "art": Art,
        "blog": Blog,
        "projects": Project
    }
    template = loader.get_template("list-main.html")
    posts = [x for x in models[name].objects.all()]
    context = CONTEXT
    context["name"] = _capitalize(name)
    context["post_list"] = posts
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
    # Find good way to get prev and next posts

    context = CONTEXT
    context["name"] = post.title
    context["post"] = post

    return HttpResponse(template.render(context, request))

class RSSFeed(Feed):
    title="Travis Southard Blog"
    link="/rss"
    description="Travis Southard is a software engineer, cyclist, and artist living in Philadelphia, PA"
    language="en"
    author_name="Travis Southard"
    author_email="hello@travissouthard.com"
    author_link="https://travissouthard.com"
    
    def items(self):
        posts = Art.objects.all().union(Blog.objects.all(), Project.objects.all()).order_by("-published")
        return posts
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        htmlEntities = {
            "amp": "&",
            "quot": "\"",
            "apos": "'",
            "lt": "<",
            "gt": ">",
        }
        desc_w_fixed_links = re.sub(r"((img\s?(\n\s*)?src)|(a\s?(\n\s*)?href))=", f"\1=\"{self.author_link}", item.description)
        desc = f"<img src='{ MEDIA_URL }{ item.image }' alt='{ item.alt_text }'>{ desc_w_fixed_links }"
        for entity_name, symbol in htmlEntities.items():
            desc = re.sub(symbol, f"&{entity_name};", desc)
        return desc
    
    def item_link(self, item):
        return f"{self.author_link}/{ item.post_type }/{ item.slug }"
    
    def item_author_name(self):
        return self.author_name
    
    def item_author_email(self):
        return self.author_email
    
    def item_author_link(self):
        return self.author_link
    
    def _get_datetime_from_date(self, d):
        return datetime(year=d.year, month=d.month, day=d.day)
    
    def item_pubdate(self, item):
        return self._get_datetime_from_date(item.published)
    
    def item_updateddate(self, item):
        return self._get_datetime_from_date(item.last_updated)
