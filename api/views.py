from rest_framework import viewsets
from lims_app.models import APIRequestLog
from api.serializers import APIRequestLogSerializer
from lims_app.models import Reader, User, Book, BorrowRecord, APIRequestLog

class APIRequestLogViewSet(viewsets.ModelViewSet):
    queryset = APIRequestLog.objects.all()
    serializer_class = APIRequestLog





