import re
import string
from datetime import date, datetime
from django.core.files import File
from ..models import Art, Blog, Project, BlogRollEntry, ResumeEntry, Topic


def handle_end_datestring(date_str):
    if (date_str is None or date_str.lower() == "present"):
        return None
    return datetime.strptime(date_str, "%B %Y").date()


def create_resume_entry(item):
    job_pattern = r"(?:<a href=[\\]?\"(.*)[\\]?\">)?([A-Za-z0-9\s]*)(?:<\/a>)?\s\|\s([A-Za-z\s,-]*)<br\s*\/>([A-Za-z0-9\s]*)-([A-Za-z\s0-9]*)(?:<br\s*/>(.*))?"
    job_match = re.search(job_pattern, item["content"])
    co_link, company, location, start, end, description = job_match.groups()
    ResumeEntry.objects.create(
        title = item["title"],
        company = company,
        co_link = co_link,
        start = datetime.strptime(start, "%B %Y").date(),
        end = handle_end_datestring(end),
        location = location,
        description = description,
    )

def create_blogroll_entry(item):
    topics = []
    for t in item["topics"]:
        topic, _ = Topic.objects.get_or_create(name = t)
        topic.save()
        topics.append(topic)

    blog_roll_entry = BlogRollEntry.objects.create(
        name = item["name"],
        link = item["link"],
    )

    for t in topics:
        blog_roll_entry.topics.add(t)

def create_post(model, item, path):
    code_link = item["codeLink"] if "codeLink" in item.keys() else None
    post = model.objects.create(
        title = item["title"],
        slug = item["slug"],
        site_link = item["siteLink"],
        code_link = code_link,
        description = item["description"],
        alt_text = item["altText"] if "altText" in item.keys() else None,
        last_updated = datetime.fromisoformat(item["lastUpdated"]).date(),
        published = datetime.fromisoformat(item["pubDate"]).date(),
    )
    if item["imagePath"]:
        file_name = item["imagePath"].split("/")[-1]
        image_path = "/".join(path.split("/")[0:2]) + "/" + item["imagePath"]
        
        with open(image_path, "rb") as f:
            post.image.save(file_name, File(f), save=True)


def import_site_data(site_data, path):
    models = {"art": Art, "blog": Blog, "micro": Blog, "projects": Project, "resume": ResumeEntry, "blogroll": BlogRollEntry}
    for item in site_data:
        if "category" not in item.keys():
            continue
        key = item["category"]
        if models[key].objects.filter(title=item["title"]).exists():
            continue

        if key == "resume":
            create_resume_entry(item)
        elif key == "blogroll":
            create_blogroll_entry(item)
        else:
            try:
                post_data = {
                    "title": item["title"],
                    "slug": item["post_name"],
                    "siteLink": "",
                    "description": item["content"],
                    "pubDate": item["post_date_gmt"],
                    "lastUpdated": item["post_modified_gmt"],
                }
                create_post(models[key], post_data, path)
            except KeyError:
                print(key, item)
