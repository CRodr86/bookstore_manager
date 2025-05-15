"""
URL configuration for bookstore_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import views as auth_views
from books.api.views import PurchaseBookAPIView

urlpatterns = [
    # Authentication URLs
    path('accounts/user/', 
        lambda req: JsonResponse({'username': req.user.username}) 
                    if req.user.is_authenticated 
                    else HttpResponse(status=401)),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # API URLs
    path('api/', include('books.api.urls', namespace='books_api')),
    
    # Endpoint for purchasing books
    path('book/buy/<int:pk>/', PurchaseBookAPIView.as_view(), name='book-buy-api'),
    
    # Another app URLs
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('books/', include('books.urls', namespace='books')),
]
