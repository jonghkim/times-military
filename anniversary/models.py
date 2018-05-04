# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class restaurant(models.Model):
    name = models.CharField(max_length = 80)
    desc = models.TextField(default= '-')
    phonenumber = models.CharField(max_length = 80, default= '-')
    url = models.CharField(max_length = 80, default= '-')
    restaurant_type = models.CharField(max_length = 80)

    REST_TYPE = ['치킨','한식','일식','양식','중식','후식','베트남']
    REST_CHOICES = [(REST_TYPE[i], REST_TYPE[i]) for i in range(0,7)]
    restaurant_type = models.CharField(max_length = 80, choices=REST_CHOICES, default='한식')
    restaurant_star = models.CharField(max_length = 80, default= '-')

    date =  models.DateTimeField(default = timezone.now())

    def __str__(self):
        return self.name

class choice(models.Model):
    rest = models.ForeignKey(restaurant)

    ip = models.CharField(max_length = 80, default= '-')
    user_name = models.CharField(max_length = 80, default= '-')
    comment = models.TextField(default = '-')

    restaurant_star = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date =  models.DateTimeField(default = timezone.now())

    def __str__(self):
        return self.rest.name
