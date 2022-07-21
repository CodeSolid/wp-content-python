import requests
from json import dump
from pprint import pp

BLOG_URL = "https://codesolid.com"


def posts_url(url, page):
    """Returns the URL and params for a single page of posts"""
    url = f"{url}/wp-json/wp/v2/posts?orderby=date&order=desc"
    params = {"page": page}
    return url, params

def get_categories(url):
    url = f"{url}/wp-json/wp/v2/categories"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Unable to get post categories")
    json = r.json()
    print(json)

def get_posts(url):
    all_posts = []
    page = 1
    while True:    
        url, params = posts_url(url, page)
        page = page + 1
        r  = requests.get(url, params=params)
        if r.status_code != 200:
            break        
        json = r.json()
        all_posts = all_posts + json
    return all_posts



def format_list(items):
    return ";".join(items)

# posts = get_posts(BLOG_URL)
# with open('all_posts_ordered.json', mode='wt') as f:
#     dump(posts, f)


# for post in posts:
#    print(f'{post["date"][0:10]},{post["link"]}')

get_categories(BLOG_URL)
