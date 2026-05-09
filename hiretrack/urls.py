from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

# 🔥 temporary homepage (for Render test)
def home(request):
    return HttpResponse("HireTrack is LIVE 🚀")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('jobs/', include('jobs.urls')),

    # 🔥 IMPORTANT: root page must not break
    path('', home),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)