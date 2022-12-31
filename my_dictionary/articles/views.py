from django.views.generic import ListView, DetailView
from .models import Article
from loguru import logger


class ArticleMixin():
    model = Article
    template_name = 'articles/articles.html'
    context_object_name = 'articles' 
    articles = Article.objects.filter(is_published=True, is_main_page=False)

    @logger.catch
    def get_queryset(self):
        return self.articles

class Articles(ArticleMixin, ListView):
    paginate_by = 10


class ShowArticle(DetailView):
    model = Article
    template_name = 'articles/conrete_article.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'


class Main(ArticleMixin, ListView):

    @logger.catch
    def get_queryset(self):
        main_page = Article.objects.filter(is_published=True, is_main_page=True)
        if main_page.exists():
            self.template_name = 'articles/conrete_article.html'
            self.context_object_name = 'article'
            return main_page.first()
        else:
            self.paginate_by = 10
            return self.articles
