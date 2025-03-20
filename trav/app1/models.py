from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    
class Destination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=100, choices=[
        ('beach', 'Beach'),
        ('mountain', 'Mountain'),
        ('historical', 'Historical'),
        ('city', 'City'),
        ('adventure', 'Adventure'),
        ('nature','Nature'),
    ])
    latitude = models.FloatField(default=0.000)
    longitude = models.FloatField(default=0.000)
    price = models.DecimalField(max_digits=10,decimal_places=2, default=0.00)
    map_link = models.URLField(blank=True, null=True)
    image=models.ImageField(upload_to='destination/', null=True, blank=True)
    

    def __str__(self):
        return self.name
    
class Activity(models.Model):
    name = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=100, choices=[
        ('boating', 'Boating'),
        ('kayaking', 'Kayaking'),
        ('trekking', 'Trekking'),
        ('sightseeing', 'Sightseeing'), 
        ('camping', 'Camping'),
        ('adventure', 'Adventure'),
        ('hiking', 'Hiking'),
        ('diving', 'Diving')
    ])
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="activities")
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='activity/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.price}"  # Show price as it is

class ActivityBooking(models.Model):
    
    profile = models.ForeignKey("Profile", on_delete=models.SET_NULL, null=True, blank=True) 
    full_name= models.CharField(max_length=255, null=True, blank=True)
    email=models.EmailField(null=True,blank=True)
    address=models.TextField(null=True, blank=True)
    phone=models.CharField(max_length=15,null=True,blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="activity_bookings")
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled')
    ], default='pending')

    def save(self, *args, **kwargs):
        if self.activity and self.activity.price is not None:
            self.total_price = self.number_of_people * self.activity.price
        else:
            self.total_price = 0  # Prevent errors if price is missing
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.full_name or 'Unknown'} - {self.activity.name} on {self.date}"
    

    

class UserPreference(models.Model):
    name=models.CharField(max_length=100,null=True, blank=True)
    preferred_categories = models.JSONField(default=list) 
    preferred_activities = models.JSONField(default=list) 

    def __str__(self):
        return f"Preferences of {self.name}"


class Review(models.Model):
    name= models.CharField(max_length=100, null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="reviews")
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name} for {self.destination.name}"

