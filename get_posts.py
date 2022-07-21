import requests
from json import dump
from pprint import pp

BLOG_URL = "https://codesolid.com"

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
        url, params = posts_url(url, page)
        page = page + 1
        r  = requests.get(url, params=params)
        if r.status_code != 200:
            break        
        json = r.json()
        all_posts = all_posts + json
    return all_posts



def get_post_categories(index_list, categories_dict):
    cat_strings = [categories_dict[index] for index in index_list]
    return cat_strings


categories_dict = get_blog_categories(BLOG_URL)
posts = get_posts(BLOG_URL)

# with open('all_posts_ordered.json', mode='wt') as f:
#     dump(posts, f)

for post in posts:
    categories = get_post_categories(post["categories"], categories_dict)
    categories_str = ";".join(categories)
    print(f'{post["date"][0:10]},{post["link"]},{categories_str}')


