from django.urls import path

from app1 import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about_us,name='about_us'),
    path('shop/',views.shop,name='shop'),
    path('destination/',views.destination,name='destinations'),
    path('trekking/',views.trekking,name='trekking'),
    path('booking/',views.booking,name='booking'),
    path('contact/',views.contact,name='contact'),
    path('package/',views.packages,name='packages'),
    path('services/',views.services,name='Services'),
    path('search/', views.search_destinations, name='search_destinations'),
    path('recommendations/<int:destination_id>/', views.recommend_destinations, name='recommend_destinations'),
    path('preferences/', views.update_preferences, name='update_preferences'),
    path('destination/<int:destination_id>/', views.destination_detail, name='destination_detail'),
     path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
     path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('destinations/', views.destinations_list, name='destination_list'),
    path('map/',views.map_view, name='map_view'),
    path('nearby-destinations/', views.nearby_destinations, name='nearby_destinations'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    # path('my-bookings/', views.user_bookings, name='user_bookings'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('profile/', views.profile_view, name='profile'),
    path('my-bookings/', views.my_bookings, name='my-bookings'),
    # path('save_destination/<int:destination_id>/', views.save_destination, name='save_destination'),
    path('save-destination/', views.save_destination, name="save_destination"),
    path('saved_destinations/', views.saved_destinations, name='saved_destinations'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)