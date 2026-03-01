import os
from dotenv import load_dotenv
from mastodon import Mastodon

load_dotenv()

mastodon = Mastodon(access_token=os.environ["MASTODON_ACCESS_KEY"], api_base_url=os.environ["MASTODON_URL"])

MASTODON_TEXT_LIMIT = 500 # Different per server. jawns.club currently has 500 as limit
MASTODON_LINK_LENGTH = 23 # Mastodon links are always 23 characters

def post_to_mastodon(post, isNew):
    read_more_str = "... Read more: "
    read_more_link = f"https://travissouthard.com/{post.post_type}/{post.slug}"
    read_more_phrase_length = len(read_more_str) + MASTODON_LINK_LENGTH
    max_desc_length = MASTODON_TEXT_LIMIT - read_more_phrase_length

    status = post.description if len(post.description) < max_desc_length else f"{post.description[0:max_desc_length]}{read_more_str}{read_more_link}"

    toot = mastodon.status_post(status=status)

    post.mastodon_link = toot.url
    post.save()

