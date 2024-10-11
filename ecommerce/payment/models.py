from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class ShippingAddress(models.Model):
  
  full_name = models.CharField(max_length=250)
  
  email = models.EmailField(max_length=255)
  
  first_address = models.CharField(max_length=300)
  
  second_address = models.CharField(max_length=300)
  
  city = models.CharField(max_length=255)
  
  state = models.CharField(max_length=255, null=True, blank=True)
  
  zipcode = models.CharField(max_length=255, null=True, blank=True)
  
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  
  class Meta:
    
    verbose_name_plural = 'Shipping Address'
  
  def __str__(self):
    
    return 'Shipping Address - ' + str(self.id)
  