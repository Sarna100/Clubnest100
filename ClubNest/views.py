from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

from .forms import UserForm, ProfileForm
from .models import Profile


from ClubNest.models import Profile

def home(request):
    if request.user.is_authenticated:
        Profile.objects.get_or_create(user=request.user)  # auto create if not exist
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about_us.html')


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


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile(request):
    # Just display profile info - no forms here
    return render(request, 'profile.html')



@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)  # প্রোফাইল না থাকলে তৈরি করবে

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)  # request.FILES!

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
from django.shortcuts import render
from django.shortcuts import render

from datetime import date

from django.shortcuts import render

from datetime import date






# app/views.py
from django.shortcuts import render
from .models import Club


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Club

from django.shortcuts import render
from django.db.models import Q
from .models import Club  # Make sure Club is your model name

from django.shortcuts import render
from django.db.models import Q
from .models import Club

def club_list(request):
    query = request.GET.get('q')
    if query:
        clubs = Club.objects.filter(
            Q(name__icontains=query) |
            Q(caption__icontains=query)
        )
    else:
        clubs = Club.objects.all()

    return render(request, 'club_list.html', {
        'clubs': clubs,
    })




from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Club

@login_required
def join_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    profile = request.user.profile
    if club not in profile.clubs.all():
        profile.clubs.add(club)
        messages.success(request, f"Thank you for joining {club.name}!")
    else:
        messages.info(request, f"You are already a member of {club.name}.")

    return redirect('club_detail', slug=club.slug)
    # ক্লাব লিস্ট পেজে রিডাইরেক্ট করবে


from django.shortcuts import render, get_object_or_404
from .models import Club

def club_detail(request, slug):
    club = get_object_or_404(Club, slug=slug)
    return render(request, 'club_detail.html', {'club': club})



from django.shortcuts import render
from .models import Event
import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, Participation
from datetime import date


from datetime import date
from django.shortcuts import render
from .models import Event, Participation

from datetime import date
from django.shortcuts import render
from .models import Event, Participation

def events_page(request):
    events = Event.objects.all()
    today = date.today()
    user = request.user if request.user.is_authenticated else None  # AnonymousUser safe

    events_status = []
    for event in events:
        joined = False
        attended = False
        participation_id = None

        if user:
            joined = Participation.objects.filter(event=event, user=user).exists()
            if event.date < today and joined:
                try:
                    p = Participation.objects.get(event=event, user=user)
                    attended = True
                    participation_id = p.id
                except Participation.DoesNotExist:
                    attended = False
                    participation_id = None

        events_status.append({
            'event': event,
            'joined': joined,
            'attended': attended,
            'participation_id': participation_id
        })

    return render(request, 'events.html', {
        'events_status': events_status,
        'today': today
    })



# Join Event
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    participation, created = Participation.objects.get_or_create(user=user, event=event, defaults={'attended': True})

    if created:
        messages.success(
            request,
            "You have successfully joined the event! After the event finishes, you can download your certificate."
        )
    else:
        messages.info(request, "You have already joined this event.")

    return redirect('events_page')


# Certificate download view
from django.http import FileResponse
from .utils import generate_certificate
from .models import Certificate

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Participation, Certificate, Event
from django.utils import timezone


@login_required
def view_certificate(request, participation_id):
    # শুধুমাত্র logged-in user এর participation এবং attended event
    participation = get_object_or_404(
        Participation,
        id=participation_id,
        user=request.user,
        attended=True
    )

    # Certificate exists কিনা চেক করুন, না থাকলে create করুন
    certificate, created = Certificate.objects.get_or_create(
        participation=participation,
        defaults={
            'issued_at': timezone.now()
        }
    )

    context = {
        "participation": participation,
        "certificate": certificate,
        "event": participation.event,
        "user": request.user
    }
    return render(request, "my_certificate.html", context)


from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Participation


@login_required
def generate_certificate_view(request, participation_id):
    participation = get_object_or_404(
        Participation,
        id=participation_id,
        user=request.user,
        attended=True
    )

    context = {
        "event": participation.event,
        "user": request.user
    }

    html_string = render_to_string('certificate_pdf.html', context)

    response = HttpResponse(content_type='application/pdf')
    filename = f"certificate_{participation.event.title}_{request.user.username}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Create PDF - no error handling
    from xhtml2pdf import pisa
    pisa.CreatePDF(html_string, dest=response)

    return response
