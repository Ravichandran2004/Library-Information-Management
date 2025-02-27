from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Reader, Book, BorrowRecord

class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowRecordSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    fee = serializers.SerializerMethodField()

    class Meta:
        model = BorrowRecord
        fields = '__all__'

    def get_fee(self, obj):
        return obj.calculate_fee()  # Include calculated fee in response
