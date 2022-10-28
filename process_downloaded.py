""" Processes the already downloaded files (see download.py) and saves
    results to reports/all_posts.csv and ./all_posts.json    

Raises:
    Exception: _description_

Returns:
    _type_: _description_
"""
from json import dump, load
import html2text
from download import POSTS_FILE, CATEGORIES_FILE
CSV_OUTPUT = "reports/all_posts.csv"
JSON_OUTPUT = "all_posts.json"

def get_post_categories(index_list, categories_dict):    
    cat_strings = [categories_dict[str(index)] for index in index_list]
    return cat_strings

def get_word_count(post):
    html = post["content"]["rendered"]
    text = html2text.html2text(html)
    HEURISTIC_ADJUSTMENT_BASED_ON_WP_COUNT = .965
    return int(len(text.split()) * HEURISTIC_ADJUSTMENT_BASED_ON_WP_COUNT)
    

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


def get_categories():
    with open(CATEGORIES_FILE, "r") as f:
        return load(f)

def get_posts():
    with open(POSTS_FILE, "r") as f:
        return load(f)

def get_massaged_posts():    
    categories_dict = get_categories()
    posts = get_posts()
    return massage_downloaded_posts(posts, categories_dict)

def save_posts_json(posts):
    with open(JSON_OUTPUT, mode='wt') as f:
         dump(posts, f)

def save_csv(csv):
    with open(CSV_OUTPUT, "wt") as f:
        f.write(csv)

def get_csv(massaged_posts):
    csv = "title,url,date,categories,word_count\n"
    for post in massaged_posts:
        # tokens = [post["title"], {post["url"], {post["date"]},
        csv += f'\"{post["title"]}\",\"{post["url"]}\",\"{post["date"]}\",\"{post["categories"]}\",\"{post["word_count"]}\"\n'
    return csv

if __name__ == "__main__":
    posts = get_massaged_posts()
    save_posts_json(posts)
    csv = get_csv(posts)
    save_csv(csv)