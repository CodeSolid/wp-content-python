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
from address_book import Url
import aiohttp
import math
import asyncio
import concurrent.futures
import base64
import requests.auth as auth

BLOG_URL = "https://codesolid.com"
POSTS_FILE = "posts.json"
CATEGORIES_FILE = "categories.json"
MAX_ITEMS_PER_PAGE = 10
url_obj = Url(BLOG_URL)
# pMVV$3yfIFzOvAJ&Kg7YD*%a
token = base64.b64encode('user:pMVV$3yfIFzOvAJ&Kg7YD*%a'.encode())
header = {'Authorization': 'Basic dXNlcjpwTVZWJDN5ZklGek92QUomS2c3WUQqJWE='}

def _get_post_status():    
    # basic = auth.HTTPBasicAuth('user', 'pMVV$3yfIFzOvAJ&Kg7YD*%a')    
    # r = requests.head(url_obj.posts, auth=basic)
    r = requests.head(url_obj.posts)
    return r.headers

def get_total_posts():
    results = _get_post_status()
    return int(results.get('x-Wp-Total'))

def _get_categories_status():    
    r = requests.head(url_obj.categories)
    return r.headers

def get_total_categories():
    results = _get_categories_status()
    return int(results.get('x-Wp-Total'))

def get_category_page_count():
    return get_pages_from_items(get_total_categories())

def get_post_page_count():
    return get_pages_from_items(get_total_posts())

def get_pages_from_items(items: int) -> int:
    count = math.floor(items / MAX_ITEMS_PER_PAGE)    
    if math.remainder(items, MAX_ITEMS_PER_PAGE) != 0.0:
        count += 1
    return count

def get_blog_categories():
    """Get the current blog categories and convert it to an id-based dictionary"""
    categories = {}
    pages = get_category_page_count()
    for page_idx in range(1, pages + 1): 
        url, params = url_obj.categories_url(page_idx)
        r = requests.get(url, params=params)
        if r.status_code != 200:
            raise Exception("Unable to get post categories")
        json = r.json()
        for item in json:
            categories[item["id"]] = item["name"]
    return categories

    
def get_posts():
    pages = get_post_page_count()
    all_posts = []
    for page in range(1, pages + 1):
        formatted_url, params = url_obj.posts_url(page)
        # print(f"Getting url: {formatted_url} with params {params}...")
        r  = requests.get(formatted_url, params=params)
        if r.status_code != 200:
            break        
        json = r.json()
        all_posts = all_posts + json
    return all_posts

async def async_demo():
    return "Hello!"

def get_page_of_posts(page: int):
    formatted_url, params = url_obj.posts_url(page)
    r  = requests.get(formatted_url, params=params)
    if r.status_code != 200:
        raise Exception(f"Received status code {r.status_code}")
    return r.json()       

def get_posts_threaded():
    pages = get_post_page_count()
    all_posts = []
    results = {}
    FIRST_PAGE = 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:        
        future_to_page = {executor.submit(get_page_of_posts, page) : page for page in range(FIRST_PAGE, pages + FIRST_PAGE)}
        for future in concurrent.futures.as_completed(future_to_page):
            page = future_to_page[future]
            result = future.result()
            results[page] = result    
    for page in range(FIRST_PAGE, pages + FIRST_PAGE):
        all_posts += results[page]
    return all_posts

async def get_page_of_posts_async(page: int):
    formatted_url, params = url_obj.posts_url(page)
    r  = requests.get(formatted_url, params=params)
    if r.status_code != 200:
        raise Exception(f"Received status code {r.status_code}")
    return r.json()        
    
async def get_posts_async():
    pages = get_post_page_count()
    all_posts = []
    requests = []
    FIRST_PAGE = 1    
    for page in range(FIRST_PAGE, pages + FIRST_PAGE):
        requests.append(get_page_of_posts_async(page))            
    results = await asyncio.gather(*requests)
        
    return results

def save_json(filename, json_dict):
    with open(filename, mode='wt') as f:
         dump(json_dict, f)

def legacy_download():
    categories = get_blog_categories()
    save_json(CATEGORIES_FILE, categories)

    # Was posts = get_posts()
    posts = get_posts_threaded()
    save_json(POSTS_FILE, posts)

if __name__ == "__main__":
    legacy_download()
