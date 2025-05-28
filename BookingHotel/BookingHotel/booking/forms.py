from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SearchForm(forms.Form):
    keyword = forms.CharField(label='Từ khóa (tên khách sạn / loại phòng)', max_length=100, required=False)
    max_occupancy = forms.IntegerField(label='Số người tối đa', required=False, min_value=1)
    status = forms.ChoiceField(
        label='Trạng thái phòng',
        choices=[('', '---'), ('Còn trống', 'Còn trống'), ('Đã đặt', 'Đã đặt')],
        required=False
    )