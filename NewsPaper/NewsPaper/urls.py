from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views

urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path("accounts/", include("allauth.urls")),
   path('news/', include('news.urls')),
   path('subscriptions/', include('subscription.urls'))
]

