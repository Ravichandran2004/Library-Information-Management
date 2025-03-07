from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import APIRequestLog
from .serializers import APIRequestLogSerializer
from .permissions import IsAdminOrReadOnly

class APIRequestLogViewSet(viewsets.ModelViewSet):
    queryset = APIRequestLog.objects.all()
    serializer_class = APIRequestLogSerializer
    permission_classes = [IsAdminOrReadOnly]  # Only admins can modify, others can view
