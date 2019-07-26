"""
Definition of urls for DjangoPolls.
"""

from datetime import datetime
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

urlpatterns = [
    path('', include(('app.urls', "app"), "appurls")),
    path('contact', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('seed/', views.seed, name='seed'),
    path('login/', 
        LoginView.as_view
        (
            template_name='app/login.html', 
            authentication_form=forms.BootstrapAuthenticationForm,
            extra_context =
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
         ),
        name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('image_upload', views.invoice_image_view, name = 'image_upload'), 
    path('success', views.success, name = 'success'), 
    path('invoice_images', views.display_invoice_images, name = 'invoice_images'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)