from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BasicTestForm, UserProfileForm
from .models import BasicTestResponse, UserProfile
from .ml.predict import predict_basic_test_result
from .models import UserProfile

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)  # Redirect to original page after login
            return redirect('profile')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    if 'next' in request.GET:
        messages.error(request, "Please log in to access this page.")

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        age = request.POST['age']
        education_level = request.POST['education_level']
        preferred_field = request.POST['preferred_field']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            age=age,
            education_level=education_level,
            preferred_field=preferred_field
        )

        messages.success(request, "Account created successfully.")
        return redirect('login')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    latest_result = BasicTestResponse.objects.filter(user=request.user).order_by('-created_at').first()
    return render(request, 'profile.html', {
        'profile': profile,
        'basic_result': latest_result.result if latest_result else None,
    })

def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

@login_required(login_url='login')
def basic_test(request):
    if request.method == 'POST':
        form = BasicTestForm(request.POST)
        if form.is_valid():
            responses = {key: int(val) for key, val in form.cleaned_data.items()}
            result = predict_basic_test_result(responses)
            BasicTestResponse.objects.create(user=request.user, responses=responses, result=result)
            return redirect('results')
    else:
        form = BasicTestForm()
    return render(request, 'basic-test.html', {'form': form})

def results(request):
    try:
        latest_result = BasicTestResponse.objects.filter(user=request.user).latest('created_at')
        return render(request, 'results.html', {'basic_result': latest_result.result})
    except BasicTestResponse.DoesNotExist:
        return render(request, 'results.html', {'basic_result': None})
