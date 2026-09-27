from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.views.static import serve


def media(request, path):
    return serve(request, path, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Systalink CyberSécurité — Administration"
admin.site.site_title = "Systalink CyberSécurité"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "connexion/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("sensibilisation.urls")),
    # Vidéos locales : servies par Django, l'outil tourne sur le poste du formateur.
    re_path(r"^media/(?P<path>.*)$", media),
]
