class Url:
    def __init__(self, base: str = None):
        self.base = base
        self.categories = f"{self.base}/wp-json/wp/v2/categories"
        self.posts = f"{self.base}/wp-json/wp/v2/posts"
        
    def posts_url(self, page):
        """Returns the URL and params for a single page of posts"""
        url = f"{self.posts}?orderby=date&order=desc"
        params = {"page": page}
        return url, params
        
    def categories_url(self, page):
        url = self.categories
        params = {"page": page}
        return url, params