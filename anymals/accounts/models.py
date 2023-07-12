from django.db import models
from django.utils.translation import gettext_lazy as _



from django.contrib.auth.models import AbstractUser
from django.db import models

choice_type = (
    ('Блиц','Блиц'),
    ('Рапид','Рапид'),
    ('Классика','Классика'),


)

choice_color = (
    ('Белый','Белый'),
    ('Чёрный','Чёрный'),

)



choice_message = (
    ('Разрешена','Разрешена'),
    ('Запрещена','Запрещена'),

)

choice_profile = (
    ('Открытый','Открытый'),
    ('Закрытый','Закрытый'),

)


choice_sex = (
    ('Мужской','Мужской'),
    ('Женский','Женский'),

)


choice_notification = (
    ('Да','Да'),
    ('Нет','Нет'),

)

choice_joined = (
    ('Да,для всех пользователей','Да,для всех пользователей'),
    ('Да,только для друзей','Да,только для друзей'),
    ('Никому','Никому')

)

choice_timezone = (
    ('UTC+1','UTC+1'),
    ('UTC+2','UTC+2'),
    ('UTC+3','UTC+')

)

import uuid


class User(AbstractUser):

    email = models.EmailField(unique=True)

    message = models.CharField(max_length=30,choices=choice_message,default='')

    profiles = models.CharField(max_length=30,choices=choice_profile,default='')


    notification = models.CharField(max_length=30,choices=choice_notification,default='')

    joined = models.CharField(max_length=30,choices=choice_joined,default='')


    timezone = models.CharField(max_length=30,choices=choice_timezone,default='')

    date_of_birth = models.CharField(max_length=30,default = '')
    sex = models.CharField(max_length=30,choices=choice_sex,default='')
    image = models.ImageField(default="profile1.jpg", null=True, blank=True)
    type = models.CharField(max_length=30,choices=choice_type,default='')
    color = models.CharField(max_length=30, choices=choice_color, default='')
    username = models.CharField(("username"), max_length=25, unique=True, blank=False, null=False)



    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Настройки шахмат"
        verbose_name_plural = "Настройки шахмат"


