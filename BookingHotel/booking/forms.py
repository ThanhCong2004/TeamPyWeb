from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SearchForm(forms.Form):
    keyword = forms.CharField(
        label='Từ khóa (Tên khách sạn)',
        max_length=100,
        required=False
    )
    CITY_CHOICES = [
        ('', '--- Chọn thành phố ---'),
        ('Hà Nội', 'Hà Nội'),
        ('Đà Nẵng', 'Đà Nẵng'),
        ('TPHCM', 'TPHCM'),
    ]

    city = forms.ChoiceField(
        label='Lọc theo thành phố',
        choices=CITY_CHOICES,
        required=False
    )