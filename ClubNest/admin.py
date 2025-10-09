from django.contrib import admin
from .models import Club, Profile, Event, Membership, Participation, Certificate


# ==============================
# Club Admin
# ==============================
@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


# ==============================
# Membership Admin
# ==============================
@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'club', 'is_approved', 'joined_at')
    list_filter = ('is_approved', 'club')
    search_fields = ('profile__user__username', 'club__name')
    actions = ['approve_members']

    def get_user(self, obj):
        return obj.profile.user.username
    get_user.short_description = "User"

    def approve_members(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} members approved successfully.")
    approve_members.short_description = "✅ Approve selected join requests"



# ==============================
# Profile Admin
# ==============================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'semester')
    search_fields = ('user__username', 'department', 'semester')


# ==============================
# Event Admin
# ==============================
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'date', 'time', 'category', 'attendees')
    list_filter = ('category', 'date', 'club')
    search_fields = ('title', 'club__name', 'location')  # "society" এর জায়গায় "club__name" দেওয়া হলো


# ==============================
# Participation Admin
# ==============================
@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'attended')
    list_filter = ('attended', 'event__club')


# ==============================
# Certificate Admin
# ==============================
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('participation', 'unique_id', 'issued_at')
    search_fields = ('participation__user__username', 'participation__event__title')
