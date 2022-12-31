from django.contrib import admin
from .models import Article
from .forms import ArticleAdminForm

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_published', 'is_main_page')
    list_display_links = ('title',)
    search_fields = ('title', 'text')
    form = ArticleAdminForm
    list_editable = ('is_published',)
    list_filter = ('is_published', 'date', 'title')
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Article, ArticleAdmin)
