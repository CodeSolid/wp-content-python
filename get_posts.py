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




# with open('all_posts_ordered.json', mode='wt') as f:
#     dump(posts, f)

def massage_downloaded_posts(posts, categories):
    massaged = []
    for post in posts:
        post_categories_as_list = get_post_categories(post["categories"], categories)
        post_categories = ";".join(post_categories_as_list)
        this_post = {
            "url": post["link"],
            "date": post["date"],
            "categories": post_categories,
            "title": post["title"]["rendered"]
        }        
        massaged.append(this_post)
    return massaged

def get_massaged_posts():
    categories_dict = get_blog_categories(BLOG_URL)
    posts = get_posts(BLOG_URL)
    return massage_downloaded_posts(posts, categories_dict)

def get_csv(massaged_posts):
    csv = "title,url,date,categories\n"
    for post in massaged_posts:
        csv += f"{post["title"]},{post["url"]},{post["date"]},{post["categories"]}\n"
    return csv
    

posts = get_massaged_posts()
csv = get_csv(posts)
print(csv)





