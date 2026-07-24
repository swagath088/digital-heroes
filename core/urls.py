from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Health check view to keep Render service awake
def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/', include('leads.urls')),
]