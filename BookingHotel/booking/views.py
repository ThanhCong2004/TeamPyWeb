from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Hotel, User, Room, Booking, Payment, RoomPicture
from django.contrib import messages
from django.contrib.auth import logout
from .forms import SearchForm
from django.utils import timezone


def logout_view(request):
    logout(request)
    return redirect('home')


# Đăng nhập
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.user_id
            return redirect('home')
        except User.DoesNotExist:
            messages.error(request, "Sai thông tin đăng nhập")
    return render(request, 'login.html')


# Trang chủ - hiện tất cả khách sạn
def home(request):
    hotels = Hotel.objects.all()
    form = SearchForm(request.GET or None)

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword', '').strip().lower()
        city = form.cleaned_data.get('city', '').strip().lower()

        # Lọc theo tên khách sạn nếu có keyword
        if keyword:
            hotels = hotels.filter(name__icontains=keyword)

        # Lọc theo thành phố nếu có city
        if city:
            filtered_hotels = []
            for hotel in hotels:
                parts = hotel.address.split(',')
                if len(parts) > 1 and parts[-1].strip().lower() == city:
                    filtered_hotels.append(hotel)
            hotels = filtered_hotels

    return render(request, 'home.html', {
        'hotels': hotels,
        'form': form,
    })


#Các phòng trong khách sạn
def hotel_detail(request, hotel_id):
    hotel = Hotel.objects.get(hotel_id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)
    return render(request, 'hotel_detail.html', {'hotel': hotel,
        'rooms': rooms,  })


# Thông tin người dùng
def user_profile(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)
    return render(request, 'profile.html', {'user': user})

# Chi tiết phòng
def room_detail(request, room_id):
    room = Room.objects.get(room_id=room_id)
    pictures = RoomPicture.objects.filter(room=room)
    return render(request, 'room_detail.html', {'room': room, 'pictures': pictures})

# Đặt phòng
def book_room(request, room_id):
    if request.method == 'POST':
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        room = Room.objects.get(room_id=room_id)
        user = User.objects.get(user_id=request.session.get('user_id'))
        total = room.price_per_night * 2  # Ví dụ tính 2 ngày
        Booking.objects.create(user=user, room=room, check_in=check_in, check_out=check_out, total=total)
        return redirect('my_bookings')
    room = Room.objects.get(room_id=room_id)
    return render(request, 'book_room.html', {'room': room})

# Xem các phòng đã đặt
def my_bookings(request):
    user = User.objects.get(user_id=request.session.get('user_id'))
    bookings = Booking.objects.filter(user=user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

# Thanh toán
def make_payment(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)

    if request.method == 'POST':
        method = request.POST['payment_method']
        Payment.objects.create(
            booking=booking,
            payment_method=method,
            payment_date=timezone.now().date(),
            amount=booking.total
        )
        return redirect('my_bookings')

    return render(request, 'make_payment.html', {
        'booking': booking
    })
