from django.contrib import admin

from .models import Activity, ActivityBooking, Destination, Review, UserPreference,Profile

# Register your models here.
admin.site.register(Destination)
admin.site.register(Activity)
admin.site.register(UserPreference)
admin.site.register(Review)
admin.site.register(ActivityBooking)
admin.site.register(Profile)