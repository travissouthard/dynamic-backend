import re
from datetime import datetime
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.syndication.views import Feed

from backend.settings import MEDIA_URL
from .models import Art, Blog, Project, BlogRollEntry, ResumeEntry

CONTEXT = {
    "name": "Recent Work",
    "desc": "Travis Southard's most recent work",
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

    context = CONTEXT.copy()
    context["name"] = "404"
    context["desc"] = "Oops! We couldn't find that!"

    response = HttpResponse(template.render(context, request))
    response.status_code = 404
    return response

def redirect_old_html_links(_, route):
    return HttpResponseRedirect(route)

def general_view(request, name):
    models = {
        "webring": BlogRollEntry,
        "resume": ResumeEntry,
    }
    try:
        if name == "index":
            return HttpResponseRedirect("/")
        if name == "full-feed":
            return home_view(request, is_full=True)
        if name in ["art", "blog", "projects"]:
            return list_view(request, name)
        template = loader.get_template(f"{name}.html")
        posts = models[name].objects.all()

        if name == "webring":
            posts = []
            post_objs = models[name].objects.prefetch_related("topics").all()
            for post in post_objs:
                posts.append({
                    "name": post.name,
                    "topics": [t.name for t in post.topics.all()]
                })
        if name == "resume":
            posts = models[name].objects.all().order_by(F("start").desc(nulls_first=True))

        context = CONTEXT.copy()
        context["name"] = _capitalize(name)
        context["post_list"] = posts
        context["desc"] = f"{name} | Travis Southard"
        return HttpResponse(template.render(context, request))
    except:
        return four_oh_four(request)

def home_view(request, is_full=False):
    template = loader.get_template("list-main.html")

    posts = Art.objects.all().union(Blog.objects.all(), Project.objects.all()).order_by("-published")

    context = CONTEXT.copy()
    context["post_list"] = posts
    context["is_full"] = is_full
    context["desc"] = "Travis Southard is a queer Philadelphian developer and artist."

    return HttpResponse(template.render(context, request))

def list_view(request, name):
    models = {
        "art": Art,
        "blog": Blog,
        "projects": Project,
    }
    template = loader.get_template("list-main.html")
    posts = models[name].objects.all().order_by("-published")

    context = CONTEXT.copy()
    context["name"] = _capitalize(name)
    context["post_list"] = posts
    context["desc"] = f"{name} by Travis Southard"
    if posts[0].image is not None:
        context["image"] = posts[0].image
        context["width"] = posts[0].image.width
        context["height"] = posts[0].image.height
        context["alt"] = posts[0].alt_text
    return HttpResponse(template.render(context, request))

def post_view(request, post_type, slug):
    try:
        models = {
            "art": Art,
            "blog": Blog,
            "projects": Project
        }
        if post_type not in ["art", "blog", "projects"]:
            return four_oh_four(request)
        template = loader.get_template("post-main.html")

        post = models[post_type].objects.get(slug=slug)
        slugs = [p.slug for p in models[post_type].objects.all()]
        i = slugs.index(post.slug)
        prev_slug = slugs[i - 1] if i > 0 else None
        next_slug = slugs[i + 1] if i + 1 < len(slugs) else None

        context = CONTEXT.copy()
        context["name"] = post.title
        context["post"] = post
        context["desc"] = post.description
        context["first_slug"] = slugs[0]
        context["prev_slug"] = prev_slug
        context["next_slug"] = next_slug
        context["last_slug"] = slugs[-1]
        if post.image is not None:
            context["image"] = post.image
            context["width"] = post.image.width
            context["height"] = post.image.height
            context["alt"] = post.alt_text

        return HttpResponse(template.render(context, request))
    except:
        return four_oh_four(request)

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
        mapping = dict.fromkeys(range(32))
        cleaned_desc = desc.translate(mapping)
        return cleaned_desc
    
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
