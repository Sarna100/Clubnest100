from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('about-us/', views.about_us, name='about_us'),

    # ✅ Fixed: only one path for club list
    path('clubs/', views.club_list, name='club_list'),

    # ✅ Join club by ID
    path('join/<int:club_id>/', views.join_club, name='join_club'),

    # ✅ Club detail by slug
    path('clubs/<slug:slug>/', views.club_detail, name='club_detail'),

    path('events/', views.events_page, name="events_page"),
]
