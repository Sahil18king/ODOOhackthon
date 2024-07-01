

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from app2.models import Bussiness,Sell

def signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('name')
        lastname = request.POST.get('lname')
        username = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try a different username.")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('home')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters.")

        user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, password=password)
        
        subject = "Welcome to Bharat Hospital ❤️"
        message = f"Hello {user.first_name}!\nThank you for visiting our website.\nPlease feel free to reach out to us at +919428235545 or reply to this email if you have any questions or require further assistance. We look forward to providing you with excellent care and support."
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('home')
    else:
        return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def loginform(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('uname')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('signup')  # Assuming signup.html has both login and signup forms
    else:
        return render(request, 'signup.html')  # Render signup.html for both login and signup forms

def business_signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        number = request.POST.get('number')
        staff_py = True

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try a different username.")
            return redirect('business_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('business_signup')

        user = User.objects.create_user(username=username, is_staff=staff_py, first_name=firstname, last_name=lastname, email=email, password=password)

        business = Bussiness.objects.create(
            username=username,
            fname=firstname,
            lname=lastname,
            email=email,
            number=number,
            password=password,
        )

        subject = "Welcome to E-Waste Recyle ❤️"
        message = f"Hello {user.first_name}!\nThank you for visiting our website.\nPlease feel free to reach out to us at +919428235545 or reply to this email if you have any questions or require further assistance. We look forward to providing you with excellent care and support."
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('home')
    else:
        return render(request, 'Bussiness.html')
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Sell
from django.contrib.auth.decorators import login_required

@login_required
def sell(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        quantity = request.POST['quantity']
        description = request.POST['description']
        photo = request.FILES.get('photo')

        Sell.objects.create(
            user=request.user,
            name=name,
            price=price,
            quantity=quantity,
            photo=photo,
            description=description
        )

        messages.success(request, 'Your e-waste listing has been created successfully!')
        return redirect('sell')
    
    # Fetch the current user's listings
    user_listings = Sell.objects.filter(user=request.user)
    context = {'user_listings': user_listings}
    return render(request, 'sell.html', context)
    # user_listings = Sell.objects.filter(user=request.user).order_by('-created_at')
    
    # context = {
    #     'user_listings': user_listings
    # }
    
    # return render(request, 'sell.html', context)

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def deals(request):
    # Fetch all listings to display in deals.html
    sell_listings = Sell.objects.all()
    context = {'sell_listings': sell_listings}
    return render(request, 'deals.html', context)


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Sell
from django.contrib.auth.decorators import login_required

@login_required
def update_listing_status(request, listing_id):
    listing = get_object_or_404(Sell, id=listing_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        listing.status = new_status
        
        if new_status == 'revised_offer':
            revised_offer = request.POST.get('revised_offer')  # Retrieve revised_offer from POST data
            listing.revised_offer = revised_offer  # Assign revised_offer to the listing
        else:
            listing.revised_offer = None  # Clear revised_offer if status is not 'revised_offer'
        
        listing.save()  # Save the listing with updated status and revised_offer

        # Return JSON response with updated status and revised offer
        return JsonResponse({
            'status': new_status,
            'revised_offer': listing.revised_offer,
        })

    # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Invalid request method'}, status=400)
