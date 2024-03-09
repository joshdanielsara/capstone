from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', projects, name='projects'),  
    path('edit_form/', edit_form, name='edit_form'),  
    path('create_entry/', create_entry, name='create_entry'),  
    path('update_entry/<str:entry_key>/', update_entry, name='update_entry'),
    path('delete_entry/<str:entry_key>/', delete_entry, name='delete_entry'),
    path('create_ldf/', create_ldf, name='create_ldf'),
    path('update_ldf_entry/<str:entry_key>/', update_ldf_entry, name='update_ldf_entry'),
    path('delete_ldf_entry/<str:entry_key>/', delete_ldf_entry, name='delete_ldf_entry'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
