from address_book import Url

url = Url("https://codesolid.com")

def test_has_base():    
    assert url.base == "https://codesolid.com"

def test_categories():
    assert url.categories.startswith(url.base)
    assert url.categories.endswith("categories") 

def test_posts():
    assert url.posts.startswith(url.base)
    assert url.posts.endswith("posts") 
