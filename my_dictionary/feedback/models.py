from django.db import models

class Contact(models.Model):
    name = models.CharField('Имя', max_length=200)
    email = models.EmailField('E-mail', max_length=200)
    message = models.TextField('Сообщение', max_length=1000)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
