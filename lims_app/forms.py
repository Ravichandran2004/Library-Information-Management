# from django import forms
# from .models import BorrowRecord

# class BorrowBookForm(forms.ModelForm):
#     class Meta:
#         model = BorrowRecord
#         fields = ['book', 'borrowed_by', 'return_date']
#         widgets = {
#             'return_date': forms.DateInput(attrs={'type': 'date'}),
#         }
from django import forms
from .models import BorrowRecord

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'user', 'return_date']  # Replace borrowed_by with user
