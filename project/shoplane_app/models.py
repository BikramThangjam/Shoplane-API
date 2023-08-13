from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.TextField()
    brand = models.CharField(max_length=200)
    shipping = models.TextField()
    description = models.TextField()
    price = models.FloatField()
    category = models.CharField(max_length=200)
    featured = models.BooleanField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["name"], name="name-index"), #single index
            models.Index(fields=["category","brand"], name="category-brand-index"), # compound index
        ]

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField()
    orderNo = models.IntegerField(unique=True)
    orderDate = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.IntegerField()
    product = models.IntegerField()
    quantity = models.IntegerField()
    price = models.FloatField()

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.IntegerField()
    user = models.IntegerField()
    rate = models.FloatField()
    review = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
class BillingAddress(models.Model):
    order = models.IntegerField(unique=True)
    address =  models.TextField()
    city = models.CharField(max_length=200)
    
class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount = models.FloatField()
    orders = models.ManyToManyField(Order)

class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Username should be provided")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=60)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=16)
    
    USERNAME_FIELD = 'username'
    objects = UserManager()

