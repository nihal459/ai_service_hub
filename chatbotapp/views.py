from django.shortcuts import render,redirect,get_object_or_404
import openai
import os
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime

# Create your views here.
def index(request):
    return render (request, 'general/index.html')

openai.api_key = "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"

def chatbot(request):
    response_text = ""
    
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        
        if prompt == 'exit':
            return render(request, 'chatbot.html', {'response_text': 'Chatbot exited.'})
        
        messages = [{"role": "system", "content": "You are a Intelligent assistant."}]
        messages.append({"role": "user", "content": prompt})
        
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages, temperature=0.5
        )
        
        response_text = chat.choices[0].message.content

    context = {'response_text': response_text}
    return render(request, 'general/chatbot.html', context)



def register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw = request.POST.get("password")
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'service_center/register.html')
        else:
            user = User.objects.create_user(
                username=uname,
                password=passw,
                is_service=True,
            )
            # Add a success message
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('register')
    else:
        return render(request, "service_center/register.html")
    

def home(request):
    return render (request, 'service_center/home.html')


def login_service(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user.is_service:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'service_center/login_service.html')


def serviceprofile(request):
    # Retrieve the current user
    user = request.user
    
    if request.method == "POST":
        # Retrieve form data
        name = request.POST.get('name')
        location = request.POST.get('location')
        district = request.POST.get('district')
        state = request.POST.get('state')
        address = request.POST.get('address')
        description = request.POST.get('description')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        website = request.POST.get('website')
        new_profile_picture = request.FILES.get('profile_picture')
        
        # Update user's profile fields
        user.name = name
        user.location = location
        user.district = district
        user.state = state
        user.address = address
        user.description = description
        user.mobile_number = mobile_number
        user.email = email
        user.website = website
        
        # Check if a new profile picture is uploaded
        if new_profile_picture:
            user.profile_picture = new_profile_picture
        
        # Save the updated profile
        user.save()
        
        # Redirect to profile page or any other page you want
        return redirect('serviceprofile')  # Replace 'profile-page' with the name of your profile page URL
    else:
        # Render the template with the current user's profile details
        return render(request, 'service_center/serviceprofile.html', {'user': user})



def SignOut(request):
     logout(request)
     return redirect('login_service')




def user_register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw = request.POST.get("password")
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'user/user_register.html')
        else:
            user = User.objects.create_user(
                username=uname,
                password=passw,
                is_user=True,
            )
            # Add a success message
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('user_register')
    else:
        return render(request, "user/user_register.html")
    


def user_home(request):
    return render (request, 'user/user_home.html')


def user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user.is_user:
            login(request, user)
            return redirect('user_home')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'user/user_login.html')


def view_service_centers(request):
    service = User.objects.filter(is_service = True)
    context = {'service':service}
    return render (request, 'user/view_service_centers.html', context)


def SignOut2(request):
     logout(request)
     return redirect('user_login')



def user_profile(request):
    # Retrieve the current user
    user = request.user
    
    if request.method == "POST":
        # Retrieve form data
        name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        new_profile_picture = request.FILES.get('profile_picture')
        
        # Update user's profile fields
        user.name = name
        user.mobile_number = mobile_number
        user.email = email
        
        # Check if a new profile picture is uploaded
        if new_profile_picture:
            user.profile_picture = new_profile_picture
        
        # Save the updated profile
        user.save()
        
        # Redirect to profile page or any other page you want
        return redirect('user_profile')  # Replace 'profile-page' with the name of your profile page URL
    else:
        # Render the template with the current user's profile details
        return render(request, 'user/user_profile.html', {'user': user})
    

def book(request, pk):
    if request.method == 'POST':
        # Get the selected date from the form
        user_date = request.POST.get('date')
        msg = request.POST.get('msg')

        # Create a new Book object
        new_booking = Book.objects.create(
            service_center_id=pk,
            user_id=request.user.pk,
            user_date=user_date,
            message = msg,
        )

        # Optionally, you can add some confirmation message
        messages.success(request, 'Booking has been successfully created.')

        # Redirect to some page after successful booking
        return redirect('user_bookings')  # Replace 'some-success-url' with your desired URL

    # If it's a GET request, render the form
    service_center = get_object_or_404(User, pk=pk)
    context = {'service_center': service_center}
    return render(request, 'user/book.html', context)




def user_bookings(request):
    userid= request.user.pk
    bookings = Book.objects.filter(user=userid)
    context = {'bookings':bookings}
    return render (request, 'user/user_bookings.html', context)



def my_bookings(request):
    userid= request.user.pk
    bookings = Book.objects.filter(service_center=userid)
    context = {'bookings':bookings}
    return render (request, 'service_center/my_bookings.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from django.contrib import messages

def update_booking(request, pk):
    booking = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        new_date = request.POST.get('date')
        new_booking_status = request.POST.get('booking-status')

        if new_date:
            booking.confirm_date = new_date
            booking.save()

        if new_booking_status:
            booking.service_center_booking_status = new_booking_status
            booking.save()

        return redirect('my_bookings')  

    context = {'booking': booking}
    return render(request, 'service_center/update_booking.html', context)



def user_update_booking(request, pk):
    booking = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        new_date = request.POST.get('date')
        new_booking_status = request.POST.get('booking-status')

        if new_date:
            booking.user_date = new_date
            booking.save()

        if new_booking_status:
            booking.user_booking_status = new_booking_status
            booking.save()

        return redirect('user_bookings')  

    context = {'booking': booking}
    return render(request, 'user/user_update_booking.html', context)