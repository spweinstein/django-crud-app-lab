from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

CATEGORIES = (
    ('C', 'Computer'),
    ('P', 'Phone'),
    ('T', 'Tablet')
)

class Accessory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Accessories' # adding Meta class so that link doesn't dipslay as "Accessorys"

class Device(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    category = models.CharField(max_length=1, choices=CATEGORIES, default=CATEGORIES[0][0])
    age = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessories = models.ManyToManyField(Accessory, blank=True) # added blank=True so that device can be created without any accessories

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    def usage_sessions_today(self):
        return self.usage_session_set.filter(date=date.today()).count()

class UsageSession(models.Model):
    date = models.DateField('Usage Date')
    minutes = models.IntegerField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return f"Used {self.device} for {self.minutes} minutes on {self.date}"

    class Meta:
        ordering = ['-date']
