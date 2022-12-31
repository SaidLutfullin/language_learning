from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
import os

class Diary(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('users', str(self.pk), instance)
        return None

    date = models.DateField('Дата')
    user = models.ForeignKey('authentication.user', on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=100)
    text = CKEditor5Field('Текст', config_name='extends')

    class Meta:
        ordering = ['-date', 'title']
