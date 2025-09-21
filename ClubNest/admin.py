from django.contrib import admin



from django.contrib import admin
from .models import Club, Profile

admin.site.register(Club)
admin.site.register(Profile)

from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'category', 'attendees')
    list_filter = ('category', 'date')
    search_fields = ('title', 'society', 'location')