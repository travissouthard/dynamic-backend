import json
import string
from datetime import date
from django.core.files import File
from ..models import Art, Blog, Project, BlogRollEntry, ResumeEntry, Topic

def create_resume_entry(model, item):
    model.objects.create(
        title = item["title"],
        company = item["company"],
        co_link = item["coLink"],
        start = date.fromtimestamp(item["start"] / 1000),
        end = date.fromtimestamp(item["end"] / 1000) if item["end"] is not None else None,
        location = item["location"],
        description = item["description"],
    )

def create_blogroll_entry(model, item):
    topics = []
    for t in item["topics"]:
        topic, _ = Topic.objects.get_or_create(name = t)
        topic.save()
        topics.append(topic)

    blog_roll_entry = model.objects.create(
        name = item["name"],
        link = item["link"],
    )

    for t in topics:
        blog_roll_entry.topics.add(t)

def create_post(model, item, path):
    code_link = item["codeLink"] if "codeLink" in item else None
    post = model.objects.create(
        title = item["title"],
        slug = "-".join([word.lower().strip(string.punctuation) for word in item["title"].split(" ")]),
        site_link = item["siteLink"],
        code_link = code_link,
        description = item["description"],
        alt_text = item["altText"],
        last_updated = date.fromtimestamp(item["lastUpdated"] / 1000),
        published = date.fromtimestamp(item["lastUpdated"] / 1000),
    )
    if item["imagePath"]:
        file_name = item["imagePath"].split("/")[-1]
        image_path = "/".join(path.split("/")[0:2]) + "/" + item["imagePath"]
        
        with open(image_path, "rb") as f:
            post.image.save(file_name, File(f), save=True)

def import_site_data(json_file, path):
    site_data = json.load(json_file)
    keys = [("art", Art), ("blog", Blog), ("projects", Project), ("resume", ResumeEntry), ("webring", BlogRollEntry)]

    for key, model in keys:
        for item in site_data[key]:
            if key == "resume":
                create_resume_entry(model, item)
            elif key == "webring":
                create_blogroll_entry(model, item)
            else:
                try:
                    create_post(model, item, path)
                except KeyError:
                    print(key, item)
