from django.db import models

class Words(models.Model):
    user = models.ForeignKey('authentication.user', on_delete=models.CASCADE)
    russian_word = models.CharField('Русское слово', max_length=100)
    foreign_word = models.CharField('Иностранное слово', max_length=100)
    context = models.CharField('Контекст', max_length=100)
    box_number = models.IntegerField('Номер коробки', default=1)
    asking_date = models.DateField('Дата повторения')
    
    def __str__(self):
        return str(self.russian_word)

    class Meta:
        ordering = ['-pk']
