from django import forms
from django.core.exceptions import ValidationError
from .models import BorrowRecord
# from .forms import BorrowRecordForm  


class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['user', 'book']

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        book = cleaned_data.get('book')

        # Check if this user has already borrowed the item
        if BorrowRecord.objects.filter(user=user, book=book, is_active=True).exists():
            raise ValidationError("Duplicate borrow record exists.")

        return cleaned_data




# from django import forms
# from .models import BorrowRecord

# class BorrowBookForm(forms.ModelForm):
#     class Meta:
#         model = BorrowRecord
#         fields = ['book', 'borrowed_by', 'return_date']
#         widgets = {
#             'return_date': forms.DateInput(attrs={'type': 'date'}),
#         }
# from django import forms
# from .models import BorrowRecord

# class BorrowBookForm(forms.ModelForm):
#     class Meta:
#         model = BorrowRecord
#         fields = ['book', 'user', 'return_date']  # Replace borrowed_by with user
