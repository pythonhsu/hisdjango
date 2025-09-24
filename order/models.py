from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=64)


class Product(models.Model):
    #pid=models.PositiveBigIntegerField() #若要自動編號,不必再增加欄位,django會自己加入自動增號的欄位
    name=models.CharField(max_length=32)
    unit=models.CharField(max_length=32)
    price=models.FloatField()
    supplierid=models.PositiveBigIntegerField()
    categoryid=models.PositiveBigIntegerField()

class OrderDetail(models.Model):
    no=models.PositiveBigIntegerField()
    date=models.DateField()
    pid=models.PositiveBigIntegerField()    
    qty=models.PositiveBigIntegerField()
    cid=models.CharField(max_length=4)
    channel=models.PositiveBigIntegerField()

class Member(models.Model):
    email=models.CharField(max_length=64)
    pwd=models.CharField(max_length=255)
    uname=models.CharField(max_length=64)
