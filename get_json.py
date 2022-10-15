"""Eventually should just get posts via Wordpress API.  
    Currently does more before saving to JSON.  
    Also does not save original json.

    There should be:
        * Something that just gets original json and saves it.
        * Something that processes it to either csv or JSON.  
        Each element processor should be a lambda or function, and should be ordered

Raises:
    Exception: _description_

Returns:
    _type_: _description_
"""
import requests
from json import dump
import html2text


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


def get_word_count(post):
    html = post["content"]["rendered"]
    text = html2text.html2text(html)
    return len(text.split())

def massage_downloaded_posts(posts, categories):
    massaged = []
    for post in posts:
        post_categories_as_list = get_post_categories(post["categories"], categories)
        post_categories = ";".join(post_categories_as_list)
        this_post = {
            "url": post["link"],
            "date": post["date"],
            "categories": post_categories,
            "title": post["title"]["rendered"],
            "word_count": get_word_count(post)
        }        
        massaged.append(this_post)
    return massaged

def get_massaged_posts():
    BLOG_URL = "https://codesolid.com"
    categories_dict = get_blog_categories(BLOG_URL)
    posts = get_posts(BLOG_URL)
    return massage_downloaded_posts(posts, categories_dict)

def save_posts_json(posts):
    with open('all_posts.json', mode='wt') as f:
         dump(posts, f)

if __name__ == "__main__":
    posts = get_massaged_posts()
    save_posts_json(posts)
