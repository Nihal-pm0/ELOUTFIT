from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm, UserUpdateForm
from order.models import Order
from django.views.decorators.cache import never_cache


def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
from django.views.decorators.csrf import csrf_protect


@csrf_protect
@never_cache
def custom_login(request):
    # 🔒 BLOCK ACCESS AFTER LOGIN
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            if user.is_superuser:
                messages.success(request, 'Welcome back, Admin!')
                return redirect('/admin/')
            else:
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '🎉 Account created successfully! Welcome to Revibe.threadsss!')
            return redirect('home')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '✅ Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:3]
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'recent_orders': recent_orders,
    }
    return render(request, 'accounts/profile.html', context)

# app/views.py
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/profile.html', {
        'password_form': form
    })

@login_required
def profile(request):
    # Your existing profile view logic
    return render(request, 'accounts/profile.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse


def custom_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            # Generate token and UID
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build reset link
            reset_url = request.build_absolute_uri(
                reverse('custom_password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Send email
            subject = "Password Reset Request"
            message = f"""
            Hello {user.username},
            
            You requested a password reset. Click the link below to reset your password:
            
            {reset_url}
            
            If you didn't request this, please ignore this email.
            
            Best regards,
            Your App Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('custom_password_reset_done')
            
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
    
    return render(request, 'accounts/custom_password_reset.html')

def custom_password_reset_done(request):
    return render(request, 'accounts/custom_password_reset_done.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/custom_password_reset_confirm.html'
    
    def get_success_url(self):
        return reverse('custom_password_reset_complete')

def custom_password_reset_complete(request):
    return render(request, 'accounts/custom_password_reset_complete.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
def ajax_password_reset(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        try:
            user = User.objects.get(email=email)
            # ... same logic as custom view ...
            
            return JsonResponse({
                'success': True,
                'message': 'Password reset link has been sent to your email.'
            })
            
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'No user found with this email address.'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        })