import datetime
from django.db import models
from django.contrib.auth.models import User
import _datetime


class Bussiness(models.Model):
    username= models.CharField(max_length=30)
    fname= models.CharField(max_length=20)
    lname= models.CharField(max_length=20)
    email= models.CharField(max_length=200)
    password= models.CharField(max_length=20)
    number= models.CharField(max_length=10)
    


from django.utils import timezone
class Sell(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='ewaste_photos/')
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('revised', 'Revised Offer')], blank=True, null=True)
    revised_offer = models.TextField(blank=True, null=True)  # New field for revised offer
    

    def __str__(self):
        return f"{self.name} - {self.user.username}"