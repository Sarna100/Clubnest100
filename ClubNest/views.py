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
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph, Frame
    from reportlab.lib.styles import ParagraphStyle
    from django.http import HttpResponse
    from django.shortcuts import get_object_or_404
    import io, os

    participation = get_object_or_404(
        Participation,
        id=participation_id,
        user=request.user,
        attended=True
    )

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # === Font Registration ===
    arial_path = "C:/Windows/Fonts/arial.ttf"
    if os.path.exists(arial_path):
        pdfmetrics.registerFont(TTFont('Arial', arial_path))
        font_name = 'Arial'
    else:
        font_name = 'Helvetica'

    # === Background ===
    p.setFillColorRGB(1, 0.98, 0.94)
    p.rect(0, 0, width, height, fill=1)

    # === Border ===
    p.setLineWidth(15)
    p.setStrokeColorRGB(0.55, 0.27, 0.07)
    p.rect(0.5 * inch, 0.5 * inch, width - 1 * inch, height - 1 * inch, fill=0)

    # === Watermark ===
    p.saveState()
    p.setFillColorRGB(0.8, 0.7, 0.4)
    p.setFont("Helvetica-Bold", 120)
    p.setFillAlpha(0.06)
    p.drawCentredString(width / 2, height / 2, "UAP")
    p.restoreState()

    # === Header ===
    p.setFillColor(colors.HexColor("#8B4513"))
    p.setFillColorRGB(0.36, 0.25, 0.20)
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2, height - 1.8 * inch, "UNIVERSITY OF ASIA PACIFIC")

    p.setFont("Helvetica", 14)
    p.drawCentredString(width / 2, height - 2.3 * inch, "74/A, Green Road, Farmgate,Dhaka-1205, Bangladesh")

    p.setLineWidth(3)
    p.line(1 * inch, height - 2.7 * inch, width - 1 * inch, height - 2.7 * inch)

    # === Certificate Title ===
    p.setFillColor(colors.HexColor("#8B4513"))
    p.setFont("Helvetica-Bold", 36)
    p.setFillColor(colors.HexColor("#8B4513"))
    p.drawCentredString(width / 2, height - 3.5 * inch, "CERTIFICATE")

    p.setFont("Helvetica", 20)
    p.setFillColor(colors.darkgoldenrod)
    p.drawCentredString(width / 2, height - 4.0 * inch, "of Achievement")

    # === Event Title ===
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.brown)
    event_title = str(participation.event.title)


    # === Paragraph Style ===
    style = ParagraphStyle(
        name='Normal',
        fontName=font_name,
        fontSize=13,
        leading=18,
        alignment=1,  # center
        textColor=colors.HexColor("#5D4037"),
    )

    # === Certificate Body Text ===
    user_name = str(participation.user.get_full_name() or participation.user.username)
    event_society = str(participation.event.society or "Club Nest")
    event_date = participation.event.date.strftime("%B %d, %Y")

    certificate_text = f"""
    This is to certify that <font color="#8B4513"><b>{user_name.upper()}</b></font> has successfully participated and demonstrated exceptional enthusiasm in the event <font color="#8B4513"> <b>{event_title}</b> </font>organized by <font color="#8B4513"> <b>{event_society}</b></font> at the University of Asia Pacific, held on <font color="#8B4513"> <b>{event_date}</b></font>. 
    <br/><br/>
    <i>We extend our heartfelt congratulations and wish continued success in all future academic and professional pursuits. May this achievement be a stepping stone to greater accomplishments.</i>
    """

    # === Paragraph Frame (Below title, above signatures) ===
    frame_top = height -  4.3  * inch
    frame_height = 2.7 * inch

    frame = Frame(
        1.3 * inch,  # left margin
        frame_top - frame_height,  # bottom Y
        width - 2.6 * inch,  # width
        frame_height,  # height
        showBoundary=0
    )
    paragraph = Paragraph(certificate_text, style)
    frame.addFromList([paragraph], p)

    # === Signatures ===
    p.setLineWidth(2)
    p.setFont("Helvetica", 12)

    # Left Signature
    p.line(1.5 * inch, 1.8 * inch, 3.5 * inch, 1.8 * inch)
    p.drawCentredString(2.5 * inch, 1.6 * inch, "Dr. Manoj Bhardwaj")
    p.setFont("Helvetica", 11)
    p.drawCentredString(2.5 * inch, 1.45 * inch, "Faculty Coordinator")
    p.drawCentredString(2.5 * inch, 1.3 * inch, "Tech Nation Club")

    # Right Signature
    p.setFont("Helvetica", 12)
    p.line(width - 3.5 * inch, 1.8 * inch, width - 1.5 * inch, 1.8 * inch)
    p.drawCentredString(width - 2.5 * inch, 1.6 * inch, "Dr. Veena Singh")
    p.setFont("Helvetica", 11)
    p.drawCentredString(width - 2.5 * inch, 1.45 * inch, "IIC President")
    p.drawCentredString(width - 2.5 * inch, 1.3 * inch, "UAP")

    # === Finalize PDF ===
    p.save()
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    filename = f"certificate_{participation.event.title}_{participation.user.username}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(pdf)
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
from datetime import date
from django.shortcuts import render
from .models import Event, Participation

def upcoming_events(request):
    today = date.today()
    user = request.user if request.user.is_authenticated else None

    # আজ বা ভবিষ্যতের event গুলোই দেখাবে
    events = Event.objects.filter(date__gte=today).order_by('date')

    events_status = []

    for event in events:
        joined = attended = False
        participation_id = None

        if user:
            joined = Participation.objects.filter(event=event, user=user).exists()

        events_status.append({
            'event': event,
            'joined': joined,
            'attended': attended,
            'participation_id': participation_id
        })

    # ✅ একই template ব্যবহার করা হচ্ছে (events.html)
    return render(request, 'events.html', {
        'events_status': events_status,
        'today': today,
        'query': '',
    })
