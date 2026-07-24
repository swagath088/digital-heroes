from django.urls import path
from .views import LeadListCreateView, LeadDetailView, AdminLoginView

urlpatterns = [
    path('leads/', LeadListCreateView.as_view(), name='lead-list-create'),
    path('leads/<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('auth/login/', AdminLoginView.as_view(), name='admin-login'),
]