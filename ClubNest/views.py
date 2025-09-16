from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return HttpResponse("""
                <div style='display:flex; justify-content:center; align-items:center; height:100vh; background:linear-gradient(to right,#f8d7da,#f1b0b7);'>
                    <div style='background:#fff3f3; padding:30px; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.2); text-align:center;'>
                        <h2 style='color:#721c24;'>❌ Passwords do not match!</h2>
                        <a href='/clubnest/signup/' style='display:inline-block; margin-top:15px; padding:10px 18px; background:#dc3545; color:white; text-decoration:none; border-radius:6px;'>🔙 Try Again</a>
                    </div>
                </div>
            """)

        if User.objects.filter(username=email).exists():
            return HttpResponse("""
                <div style='display:flex; justify-content:center; align-items:center; height:100vh; background:linear-gradient(to right,#ffeeba,#f8d775);'>
                    <div style='background:#fff8e1; padding:30px; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.2); text-align:center;'>
                        <h2 style='color:#856404;'>⚠️ Email already registered!</h2>
                        <a href='/clubnest/signin/' style='display:inline-block; margin-top:15px; padding:10px 18px; background:#ffc107; color:black; text-decoration:none; border-radius:6px;'>🔑 Sign In</a>
                    </div>
                </div>
            """)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        return HttpResponse(f"""
            <div style='display:flex; justify-content:center; align-items:center; height:100vh; background:linear-gradient(to right,#a18cd1,#fbc2eb);'>
                <div style='background:#ffffff; padding:40px; border-radius:16px; box-shadow:0 6px 20px rgba(0,0,0,0.25); text-align:center; max-width:400px;'>
                    <h2 style='color:#4b0082;'>🎉 Welcome {first_name}!</h2>
                    <p style='margin:10px 0; font-size:15px; color:#333;'>Your account has been created successfully.</p>
                    <a href='/clubnest/signin/' style='display:inline-block; margin-top:20px; padding:12px 20px; background:#6a1bbd; color:white; text-decoration:none; border-radius:8px; font-weight:bold;'>🚀 Go to Sign In</a>
                </div>
            </div>
        """)

    return render(request, "signup.html")


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)   # user লগইন করানো হচ্ছে
            return redirect('home')   # লগইন হওয়ার পর home এ যাবে
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
