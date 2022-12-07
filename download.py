"""Gets the JSON from the codesolid.com website and saves it as:
        posts.json - post data
        categories.json - categories data

Raises:
    Exception: _description_

Returns:
    _type_: _description_
"""
import requests
from json import dump

BLOG_URL = "https://codesolid.com"
POSTS_FILE = "posts.json"
CATEGORIES_FILE = "categories.json"

def posts_url(url, page):
    """Returns the URL and params for a single page of posts"""
    url = f"{url}/wp-json/wp/v2/posts?orderby=date&order=desc"
    params = {"page": page}
    return url, params

def get_blog_categories(url):
    """Get the current blog categories and convert it to an id-based dictionary"""
    url = f"{url}/wp-json/wp/v2/categories"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Unable to get post categories")
    json = r.json()
    return {item["id"]: item["name"] for item in json}
    
def get_posts(url):
    all_posts = []
    page = 1
    while True:    
        formatted_url, params = posts_url(url, page)
        page = page + 1
        print(f"Getting url: {formatted_url} with params {params}...")
        r  = requests.get(formatted_url, params=params)
        if r.status_code != 200:
            break        
        json = r.json()
        all_posts = all_posts + json
    return all_posts

def save_json(filename, json_dict):
    with open(filename, mode='wt') as f:
         dump(json_dict, f)

if __name__ == "__main__":
    categories = get_blog_categories(BLOG_URL)
    save_json(CATEGORIES_FILE, categories)

    posts = get_posts(BLOG_URL)
    save_json(POSTS_FILE, posts)
