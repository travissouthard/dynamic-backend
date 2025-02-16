import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

def send_webmention(source, target):
    try:
        resp = requests.post(
            "https://telegraph.p3k.io/webmention", 
            data={
                "token": os.environ["WEBMENTION_API_KEY"], 
                "source": source, 
                "target": target
            }
        )
        data = resp.json()
        return data["status"]
    except Exception as e:
        return e
    

def collect_and_send_webmentions(desc, post_type, slug):
    try:
        link_list = re.findall(r"href=(.*)", desc)
        response_list = []
        for target in link_list:
            home = "https://travissouthard.com"
            if target[0-len(home)] == home or target[0] == ".":
                continue
            source = home + f"/{post_type}/{slug}"
            resp = send_webmention(source, target)
            response_list.append(resp)
        return response_list
    except Exception as e:
        return e