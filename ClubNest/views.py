from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse

from .forms import UserForm, ProfileForm
from .models import Profile, Club, Membership, Event, Participation, Certificate

# ---------- BASIC PAGES ----------
def home(request):
    if request.user.is_authenticated:
        Profile.objects.get_or_create(user=request.user)
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about_us.html')

# ---------- USER AUTH ----------
def signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return HttpResponse("""
                <h2 style='color:red;text-align:center;margin-top:20%;'>❌ Passwords do not match!</h2>
                <a href='/clubnest/signup/' style='display:block;text-align:center;'>🔙 Try Again</a>
            """)

        if User.objects.filter(username=email).exists():
            return HttpResponse("""
                <h2 style='color:orange;text-align:center;margin-top:20%;'>⚠️ Email already registered!</h2>
                <a href='/clubnest/signin/' style='display:block;text-align:center;'>🔑 Sign In</a>
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
            <h2 style='color:green;text-align:center;margin-top:20%;'>🎉 Welcome {first_name}!</h2>
            <p style='text-align:center;'>Your account has been created successfully.</p>
            <a href='/clubnest/signin/' style='display:block;text-align:center;'>🚀 Go to Sign In</a>
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

# ---------- PROFILE ----------
@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
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

# ---------- CLUB ----------
# ClubNest/views.py - club_list function e change koro
def club_list(request):
    user = request.user if request.user.is_authenticated else None
    query = request.GET.get('q', '').strip()

    if query:
        clubs = Club.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(caption__icontains=query)
        )
    else:
        clubs = Club.objects.all()

    clubs_with_status = []

    for club in clubs:
        membership = None
        if user:
            try:
                # TRY-EXCEPT diye wrap koro
                membership = Membership.objects.filter(club=club, profile__user=user).first()
            except:
                membership = None

        clubs_with_status.append({
            'club': club,
            'membership': membership
        })

    return render(request, 'club_list.html', {'clubs_with_status': clubs_with_status})


# ClubNest/views.py - join_club function
@login_required
def join_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    profile, _ = Profile.objects.get_or_create(user=request.user)

    try:
        membership, created = Membership.objects.get_or_create(profile=profile, club=club)

        if not created:
            if membership.is_approved:
                messages.info(request, "You are already a member of this club.")
            else:
                messages.info(request, "Your join request is pending approval.")
        else:
            messages.success(request, "Join request sent! Please wait for admin approval.")
    except Exception as e:
        messages.error(request, "System is updating. Please try again later.")

    return redirect('club_list')
def club_detail(request, slug):
    club = get_object_or_404(Club, slug=slug)
    today = date.today()
    upcoming_events = Event.objects.filter(club=club, date__gte=today).order_by('date')
    return render(request, 'club_detail.html', {
        'club': club,
        'events': upcoming_events
    })

# ---------- EVENTS ----------
def events_page(request):
    today = date.today()
    user = request.user if request.user.is_authenticated else None
    query = request.GET.get('q', '').strip()

    if query:
        events = Event.objects.filter(club__name__icontains=query)
    else:
        events = Event.objects.all()

    events_status = []

    for event in events:
        joined = attended = False
        participation_id = None

        if user:
            joined = Participation.objects.filter(event=event, user=user).exists()
            if event.date < today and joined:
                p = Participation.objects.filter(event=event, user=user).first()
                if p:
                    attended = True
                    participation_id = p.id

        events_status.append({
            'event': event,
            'joined': joined,
            'attended': attended,
            'participation_id': participation_id
        })

    return render(request, 'events.html', {
        'events_status': events_status,
        'today': today,
        'query': query
    })

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    participation, created = Participation.objects.get_or_create(
        user=user,
        event=event,
        defaults={'attended': True}
    )

    if created:
        messages.success(request, "You have successfully joined the event!")
    else:
        messages.info(request, "You have already joined this event.")

    return redirect('events_page')

# ---------- CERTIFICATE ----------
@login_required
def view_certificate(request, participation_id):
    participation = get_object_or_404(
        Participation,
        id=participation_id,
        user=request.user,
        attended=True
    )

    certificate, created = Certificate.objects.get_or_create(
        participation=participation,
        defaults={'issued_at': date.today()}
    )

    return render(request, "my_certificate.html", {
        "participation": participation,
        "certificate": certificate,
        "event": participation.event,
        "user": request.user
    })

@login_required
def generate_certificate_view(request, participation_id):
    from django.template.loader import render_to_string
    from xhtml2pdf import pisa

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

    pisa.CreatePDF(html_string, dest=response)
    return response


# sponsors/views.py

from django.shortcuts import render
from .models import Sponsor

def sponsor_list(request):
    # Retrieve only active sponsors, ordered by priority and then name
    sponsors = Sponsor.objects.filter(is_active=True).order_by('priority', 'name')
    context = {
        'sponsors': sponsors,
        'page_title': "Our Sponsors & Partners"
    }
    return render(request, 'sponsor_list.html', context)