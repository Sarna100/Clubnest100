from django.contrib import admin
from django.urls import path, include
from ClubNest import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Home page
    path('clubnest/', include('ClubNest.urls')),  # ClubNest app URLs
    path('upload-gallery-image/', views.upload_gallery_image, name='upload_gallery_image'),
    path('get-gallery-images/', views.get_gallery_images, name='get_gallery_images'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
