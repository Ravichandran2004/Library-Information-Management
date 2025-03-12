from django import forms
from django.core.exceptions import ValidationError
from .models import BorrowRecord
from django.contrib.auth.models import User
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
class StaffRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        # Mark user as staff
        user.is_staff = True
        user.set_password(self.cleaned_data['password'])  # Hash password
        if commit:
            user.save()
        return user



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