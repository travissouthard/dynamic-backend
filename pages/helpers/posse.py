import os
from dotenv import load_dotenv
from mastodon import Mastodon

load_dotenv()

mastodon = Mastodon(access_token=os.environ["MASTODON_ACCESS_KEY"], api_base_url=os.environ["MASTODON_URL"])

def post_to_mastodon(post):
    types = {
        "art": "piece of art",
        "blog": "blog post",
        "project": "project",
    }
    post_type = types[post.post_type]

    status = f"I just added a new {post_type} to my website!\n\n\"{post.title}\"\n\nCheck it out at: https://travissouthard/{post.post_type}/{post.slug}"
    
    post = mastodon.status_post(status=status)