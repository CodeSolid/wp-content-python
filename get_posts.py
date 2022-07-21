import configparser
import requests
from json import dump
from pprint import pp

def get_config():
    config = configparser.ConfigParser()
    config.read('blog.ini')
    return config["main"]

def wp_url(url, page):
    """Returns the URL and params for a single page of posts"""
    url = f"{url}/wp-json/wp/v2/posts?orderby=date&order=desc"
    params = {"page": page}
    return url, params

def get_posts(url):
    all_posts = []
    page = 1
    while True:    
        url, params = wp_url(base_url, page)
        page = page + 1
        r  = requests.get(url, params=params)
        if r.status_code != 200:
            break        
        json = r.json()
        all_posts = all_posts + json
    return all_posts

config = get_config()
base_url = config.get("blog_url")

posts = get_posts(base_url)
with open('all_posts_ordered.json', mode='wt') as f:
    dump(posts, f)
for post in posts:
   print(f'{post["date"][0:10]},{post["link"]}')

# print("Getting posts for the URL defined in blog.ini")
# print("This may take some time.  Please wait...")
# for post in get_posts(base_url):
#     # print(post["link"])
#     pp(post)

# print(f"Posts retrieved: {len(all_posts)}")
# d = all_posts[0].copy()
# del(d["content"])
#pp(d)

