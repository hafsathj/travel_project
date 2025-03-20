from django.shortcuts import render
from django.contrib.auth import logout
from django.http import JsonResponse
from django.urls import reverse
from .models import ActivityBooking, Destination, Activity
from django.shortcuts import get_object_or_404, render, redirect
from .models import Destination, Activity, UserPreference, ActivityBooking, Review
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import JsonResponse
from geopy.distance import geodesic
import json
from django.shortcuts import render, redirect
from .models import ActivityBooking, Destination, Activity
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.

def format_price(price):
    return f"{price / 1000:.1f}k" if price >= 1000 else f"{price:.2f}"

def index(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')
    activities = Activity.objects.all()
    destinations = Destination.objects.all()
    reviews = Review.objects.all().order_by('-created_at') 
    categories = Destination._meta.get_field('category').choices
    print(Destination.objects.all())
    if query:
        destinations = destinations.filter(name__icontains=query)

    if category:
        destinations = destinations.filter(category=category)

    for destination in destinations:
        destination.formatted_price = format_price(destination.price)
    
    for activity in activities:
        activity.formatted_price =format_price(activity.price)
    
    print(Activity.objects.all())
    return render(request, 'index.html', {'destination_list': destinations, 'activities': activities, 'categories': categories, 'reviews': reviews}) 

def about_us(request):
    return render(request,'about.html')

def shop(request):
    return render(request,'shop.html')

def destination(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')

    destinations = Destination.objects.all()
    print(Destination.objects.all())
    if query:
        destinations = destinations.filter(name__icontains=query)

    if category:
        destinations = destinations.filter(category=category)

    for destination in destinations:
        destination.formatted_price = format_price(destination.price)

    return render(request, 'destinations.html', {'destination_list': destinations})
   
def trekking(request):
    activities = Activity.objects.all()
    for activity in activities:
        activity.formatted_price =format_price(activity.price)
    return render(request,'trekking.html', {'activities': activities})

def booking(request):
    destinations = Destination.objects.all()
    activities = Activity.objects.all()
    categories = destinations.values_list("category", flat=True).distinct()
    activity_types = Activity.objects.values_list('activity_type', flat=True).distinct()
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        destination_id = request.POST.get("destination")
        activity_id = request.POST.get("activity")
        date = request.POST.get("date")
        time = request.POST.get("time")
        number_of_people = request.POST.get("number_of_people")

        # Validate required fields
        if not all([full_name, email, phone, activity_id, date, time, number_of_people]):
            messages.error(request, "All fields marked with * are required!")
            return redirect("booking")

        try:
            number_of_people = int(number_of_people)
            if number_of_people <= 0:
                messages.error(request, "Number of people must be at least 1.")
                return redirect("booking")
        except ValueError:
            messages.error(request, "Invalid number of people.")
            return redirect("booking")

        # Validate destination (optional)
        destination = None
        if destination_id:
            destination = get_object_or_404(Destination, id=destination_id)

        # Validate activity
        activity = get_object_or_404(Activity, id=activity_id)

        # Create and save the booking
        booking = ActivityBooking.objects.create(
            full_name=full_name,
            email=email,
            address=address,
            phone=phone,
            destination=destination,
            activity=activity,
            date=date,
            time=time,
            number_of_people=number_of_people,
        )

        messages.success(request, "Booking submitted successfully!")

        # Redirect to confirmation page, passing the booking ID
        return redirect(reverse("booking_confirmation", kwargs={"booking_id": booking.id}))

    return render(request, "booking.html", {"destinations": destinations, "activities": activities ,"categories": categories, "activity_types": activity_types})


def contact(request):
    return render(request,'contact.html')
def packages(request):
    return render(request,'packages.html')
def services(request):
    return render(request,'services.html')
def destination_details(request, destination_name):
    return render(request, 'destinationdetails.html', {'destination_name': destination_name})

def package_list(request):
    return render(request, 'package.html')

def search_destinations(request):
    destination_id = request.GET.get('location', '').strip()  # Destination ID
    category = request.GET.get('category', '').strip()  # Category
    activity = request.GET.get('activity', '').strip()  # Activity

    destinations = Destination.objects.all()

    # Apply filters based on user selection
    if destination_id:
        destinations = destinations.filter(id=destination_id)

    if category:
        destinations = destinations.filter(category=category)

    if activity:
        destinations = destinations.filter(activities__activity_type=activity).distinct()

    return render(request, 'search_results.html', {'destinations': destinations})



def map_view(request):
    destinations = list(Destination.objects.values("name", "latitude", "longitude", "category")) 

    return render(request, 'map.html', {'destinations_json': json.dumps(destinations)})

def nearby_destinations(request):
    try:
        user_lat = float(request.GET.get('lat'))
        user_lon = float(request.GET.get('lon'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)

    destinations = Destination.objects.all()
    nearby_places = []

    for destination in destinations:
        dest_coords = (destination.latitude, destination.longitude)
        user_coords = (user_lat, user_lon)
        distance = geodesic(user_coords, dest_coords).km  

        if distance <= 50:  
            nearby_places.append({
                'name': destination.name,
                'category': destination.category,
                'lat': destination.latitude,
                'lon': destination.longitude,
                'distance': round(distance, 2)
            })

    return JsonResponse({'nearby_destinations': nearby_places})

def recommend_destinations(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    similar_destinations = Destination.objects.filter(category=destination.category).exclude(id=destination.id)[:5]

    return render(request, 'recommendations.html', {
        'destination': destination,
        'recommended_destinations': similar_destinations
    })


def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    
    
    all_destinations = Destination.objects.exclude(id=destination.id)
    descriptions = [destination.description] + [d.description for d in all_destinations]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    ranked_destinations = sorted(zip(all_destinations, similarity_scores), key=lambda x: x[1], reverse=True)
    recommended_destinations = [dest[0] for dest in ranked_destinations[:5]]
    recommended_activities = Activity.objects.filter(destination=destination)
    destination.formatted_price = format_price(destination.price)

    return render(request, 'destinationdetails.html', {
        'destination': destination,
        'recommended_destinations': recommended_destinations,
        'recommended_activities': recommended_activities,
        #  'nearby_destinations': nearby_places
    })


def destinations_list(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')

    destinations = Destination.objects.all()
    print(Destination.objects.all())
    if query:
        destinations = destinations.filter(name__icontains=query)

    if category:
        destinations = destinations.filter(category=category)

    return render(request, 'destinations.html', {'destination_list': destinations})


def update_preferences(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        selected_category = request.POST.get('category')  # Corrected
        selected_activity_type = request.POST.get('activity')  # Corrected

        # Save user preferences
        preferences, created = UserPreference.objects.get_or_create(name=name)
        preferences.preferred_categories = [selected_category]  
        preferences.preferred_activities = [selected_activity_type] 
        preferences.save()

        matching_destinations = Destination.objects.filter(
        category=selected_category, activities__activity_type=selected_activity_type
        ).distinct()
       
    return render(request, 'preferences.html', {'preferences': preferences,
            'matching_destinations': matching_destinations,'category': selected_category, 'activity_type': selected_activity_type})




def booking_confirmation(request, booking_id):
    booking = get_object_or_404(ActivityBooking, id=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})


def user_bookings(request):
    name = request.GET.get('name', 'Guest')
    bookings = ActivityBooking.objects.filter(name=request.GET.get('name', 'Guest'))
    return render(request, 'travel/user_bookings.html', {'bookings': bookings})




def submit_review(request):
    if request.method == "POST":
        name = request.POST.get("name")
        destination_id = request.POST.get("destination")
        activity_id = request.POST.get("activity")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        # Ensure required fields are not empty
        if not (name and destination_id and rating and comment):
            messages.error(request, "Please fill in all required fields.")
            return redirect("index")  # Redirect back to the same page

        destination = Destination.objects.get(id=destination_id)
        activity = Activity.objects.get(id=activity_id) if activity_id else None

        # Save the review
        Review.objects.create(
            name=name,
            destination=destination,
            activity=activity,
            rating=int(rating),
            comment=comment,
        )

        messages.success(request, "Your review has been submitted successfully!")
        return redirect("index")  # Redirect after successful submission

    # Pass destinations and activities to template
    destination_list = Destination.objects.all()
    activities = Activity.objects.all()
    return render(request, "index.html", {"destination_list": destination_list, "activities": activities})


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        location = request.POST['location']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            return render(request, 'index.html', {'error': "Passwords do not match!"})

        if User.objects.filter(username=email).exists():
            return render(request, 'index.html', {'error': "Email already exists!"})

        user = User.objects.create_user(
            username=email, email=email, first_name=first_name, last_name=last_name, password=password
        )
        user.profile.phone_number = phone_number
        user.profile.location = location
        user.profile.save()
        return redirect('login')

    return render(request, 'index.html')



def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'index.html', {'error': "Invalid credentials!"})
    return render(request, 'index.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})


def logout_view(request):
    if request.method == "POST" or request.method == "GET":  
        logout(request)
        return redirect('index')  
    
@login_required
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")
        location = request.POST.get("location")

        # Update user details
        user.first_name = full_name.split()[0] if full_name else user.first_name
        user.last_name = " ".join(full_name.split()[1:]) if full_name and len(full_name.split()) > 1 else user.last_name
        user.email = email

        if password:  # Only update password if provided
            user.set_password(password)

        user.save()

        # Update profile details
        profile.phone_number = phone_number
        profile.location = location
        profile.save()

        messages.success(request, "Profile updated successfully! Please log in again if you changed your password.")
        
        if password:  # If password is changed, redirect to login
            return redirect("login")
        else:
            return redirect("profile")

    return render(request, "profile.html", {"profile": profile})

@login_required
def my_bookings(request):
    
    # user_bookings = ActivityBooking.objects.filter(user=request.user)
    # user_destinations = Destination.objects.filter(bookings__user=request.user).distinct()
    # user_activities = Activity.objects.filter(activity_bookings__user=request.user).distinct()
    user_bookings = ActivityBooking.objects.filter(profile=request.user.profile)
    user_destinations = Destination.objects.filter(bookings__user=request.user).distinct()
    user_activities = Activity.objects.filter(activity_bookings__user=request.user).distinct()

    context = {
        'bookings': user_bookings,
        'destinations': user_destinations,
        'activities': user_activities,
    }
    return render(request, 'mybooking.html', context)