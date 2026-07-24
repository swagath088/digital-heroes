from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Lead
from .serializers import LeadSerializer

# Public: Submit lead & Admin: Search/List leads
class LeadListCreateView(generics.ListCreateAPIView):
    serializer_class = LeadSerializer

    def get_queryset(self):
        queryset = Lead.objects.all().order_by('-created_at')
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(full_name__icontains=search_query) | 
                Q(email__icontains=search_query)
            )
        return queryset

# Admin: Update lead status
class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

# Real Django Superuser Login Endpoint
class AdminLoginView(APIView):
    def post(self, request):
        email_or_username = request.data.get('email')
        password = request.data.get('password')

        # Find user by email first, fallback to username
        user_obj = User.objects.filter(email=email_or_username).first()
        username = user_obj.username if user_obj else email_or_username

        user = authenticate(username=username, password=password)

        if user is not None and user.is_staff:
            return Response({"token": f"token-{user.id}"}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid admin email or password"}, status=status.HTTP_400_BAD_REQUEST)