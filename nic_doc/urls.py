from django.contrib import admin
from django.urls import path
from doc_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('division-selection/', views.division_selection, name='division-selection'),
    path('generate/', views.generate_documents, name='generate_documents'),
    path('login/', views.login, name='login'),
    path('verify/', views.verify_user, name='verify_user'),
   

    # path('download/', views.download_file, name='download_file'),
    # path('', views.generate_document, name='generate_document'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)