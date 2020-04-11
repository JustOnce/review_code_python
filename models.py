from django.contrib.auth.models import User
from django.db import models


class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Юзер')
    inn = models.IntegerField(verbose_name='ИНН')
    account = models.FloatField(verbose_name='Счёт')

    def __str__(self):
        return '{id} {inn}'.format(id=str(self.id), inn=self.inn)
