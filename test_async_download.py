import asyncio
import async_download as ad
import pytest

def test_get_total_posts():
    posts = ad.get_total_posts()
    assert posts > 100

def test_get_post_page_count():
    pages = ad.get_post_page_count()
    assert pages > 10 and pages < 1000

def test_get_total_categories():
    categories = ad.get_total_categories()
    assert categories > 5 and categories < 30

def test_get_blog_categories():
    categories = ad.get_blog_categories()
    assert categories is not None
    assert "Python" in categories.values()

@pytest.mark.skip("Broken")
def test_get_posts_sync():
    posts = ad.get_posts()
    assert posts is not None


def test_get_one_post():
    posts = ad.get_page_of_posts(1)    
    assert len(posts) == 10
    
def test_get_posts_threaded():
    posts = ad.get_posts_threaded()   
    assert len(posts) == 12
    
@pytest.mark.asyncio
async def test_async_all_post():
    posts = await ad.get_posts_async()   
    print(posts)
