from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from ShareApp.models import UserProfile


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        email = data['email']
        role = data['role']
        if role not in ['ops','client']:
            return JsonResponse({'error':'Invalid role'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists!'})
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user,role=role)
        user.save()
        return JsonResponse({'message': 'User created successfully!'})
    return None


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'User login successfully!','role':user.userprofile.role})
        else:
            return JsonResponse({'message': 'Invalid credentials!'})
    return None


@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message': 'User logged out successfully!'})
        else:
            return JsonResponse({'message': 'User is not logged in'}, status=400)
    return None


