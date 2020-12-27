from django.contrib import admin
from django.urls import path
from address import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('cor',views.co_ordinates,name='cor'),
    path('download',views.download,name='download')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
