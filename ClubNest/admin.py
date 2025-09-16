from django.contrib import admin
from .models import UpcomingEvent

@admin.register(UpcomingEvent)
class UpcomingEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location')
    search_fields = ('title', 'location')
    list_filter = ('date',)


    fields = ('title', 'caption', 'date', 'time', 'location', 'image')
# admin.site.register(UpcomingEvent)
