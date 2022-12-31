from django.db import models
from django.urls import reverse
from loguru import logger


class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')
    text = models.TextField(blank=True, verbose_name='Текст статьи')
    date = models.DateField(verbose_name='Дата публикации')
    is_main_page = models.BooleanField(default=False, verbose_name='Главная страница?')
    is_published = models.BooleanField(default=False, verbose_name='Опублковать?')
    preview_photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото превью')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles', kwargs={'id': self.pk})

    class Meta:
        verbose_name = 'Статьи'
        verbose_name_plural = 'Статьи'
        ordering = ['-date', 'title']

    @logger.catch
    def save(self, *args, **kwargs):
        if self.is_main_page:
            previous_main_page = Article.objects.filter(is_main_page=True).first()
            if previous_main_page is not None and previous_main_page != self:
                previous_main_page.is_main_page = False
                previous_main_page.save()
        super(Article, self).save(*args, **kwargs)
