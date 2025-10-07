from django import template
from ClubNest.models import Profile

register = template.Library()

@register.filter
def user_joined(club, user):
    try:
        profile = Profile.objects.get(user=user)
        return club in profile.clubs.all()
    except Profile.DoesNotExist:
        return False
