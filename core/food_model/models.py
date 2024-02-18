from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django.core.validators import RegexValidator


class Restaurant(models.Model):
  restaurant_name = models.CharField(max_length=255)
  owner_name = models.CharField(max_length=255)
  address = models.TextField(blank=False, null=False)
  image = models.ImageField(upload_to='restaurant_images/')
  pincode = models.PositiveIntegerField()
  phone_number = models.PositiveIntegerField()
  is_approved = models.BooleanField(default=False)
  is_rejected = models.BooleanField(default=False)
  created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
  created_on = models.DateTimeField(auto_now_add=True)
  # status = models.CharField(max_length=255, choices=[('approved','Approved'),('rejected','Rejected'),])

  def __str__(self):
    return self.restaurant_name
  
class RestaurantCategory(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name
  
class MenuItem(models.Model):
  restaurant = models.ForeignKey('Pending', related_name='restaurant_details', on_delete=models.CASCADE)
  category = models.ForeignKey('MenuCategory', related_name='item', on_delete=models.CASCADE)
  food_name = models.CharField(max_length=255)
  price = models.IntegerField()
  description = models.TextField(blank=False, null=False)
  image = models.ImageField(upload_to='menu_images/')
  rating = models.IntegerField()
  is_sold = models.BooleanField(default=False)
  created_by = models.ForeignKey(User, related_name='item', on_delete=models.CASCADE)
  status = models.CharField(max_length=20, choices=[('approved', 'Approved'), ('rejected', 'Rejected')])

  def __str__(self):
    return self.food_name
  
class MenuCategory(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name
  

class Pending(models.Model):
  restaurant_name = models.CharField(max_length=255)
  category = models.ForeignKey('RestaurantCategory',related_name = 'categories', on_delete=models.CASCADE)
  owner_name = models.CharField(max_length=255)
  address = models.TextField(blank=False, null=False)
  image = models.ImageField(upload_to='restaurant_images/')
  pincode = models.PositiveIntegerField()
  phone_number = models.PositiveIntegerField()
  is_approved = models.BooleanField(default=False)
  is_rejected = models.BooleanField(default=False)
  created_by = models.ForeignKey(User, related_name='item_related', on_delete=models.CASCADE)
  created_on = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
  # status = models.CharField(max_length=255, choices=[('approved','Approved'),('rejected','Rejected'),])

  def __str__(self):
    return self.restaurant_name
  
#user profile
class Profile(models.Model):
  phone_regex = RegexValidator(
        regex=r'^\d{3}-\d{3}-\d{4}$',
        message="Phone number must be the format of xxx-xxx-xxxx.",
    )
  
  created_by = models.OneToOneField(User, on_delete=models.CASCADE)
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  address = models.TextField(blank=False, null=False)
  pincode = models.IntegerField()
  city = models.CharField(max_length=255)
  phonenumber = models.CharField(max_length=12, validators=[phone_regex])
  temp_phonenumber = models.CharField(max_length=12, validators=[phone_regex])
  image = models.ImageField(upload_to='profile_images/', null=True)
  terms_and_services = models.BooleanField(default=False, null=False)


  def __str__(self):
    return self.firstname
  

class OrderModel(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\d{3}-\d{3}-\d{4}$',
        message="Phone number must be the format of xxx-xxx-xxxx.",
    )
    email_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$',
        message="Enter the correct email input.",
    )

    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField(
        'MenuItem', related_name='order', blank=True)
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=45, blank = True, validators=[email_regex])
    phonenumber = models.CharField(max_length=15, validators=[phone_regex])
    address = models.TextField(blank=True)

    def __str__(self):
      return self.created_by


class Order(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\d{3}-\d{3}-\d{4}$',
        message="Phone number must be the format of xxx-xxx-xxxx.",
    )

    email_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$',
        message="Enter the correct email input.",
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Pending', on_delete=models.CASCADE)
    items = models.ManyToManyField('MenuItem', related_name='food')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username} - {self.created_at}"