from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Hotel, User, Room, Booking, Payment, RoomPicture, Picture
from django.contrib import messages
from django.contrib.auth import logout
from .forms import SearchForm
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator #Phân trang home
from django.db.models import Max



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

    paginator = Paginator(hotels, 5)  # 5 khách sạn mỗi trang
    page_number = request.GET.get('page')
    hotels = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'hotels': hotels,
        'form': form,
    })


#Các phòng trong khách sạn
def hotel_detail(request, hotel_id):
    hotel = Hotel.objects.get(hotel_id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)
    pictures = Picture.objects.filter(hotel=hotel)

    return render(request, 'hotel_detail.html',
                  {'hotel': hotel, 'rooms': rooms,  'pictures': pictures })


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
    room = Room.objects.get(room_id=room_id)

    if request.method == 'POST':
        # Lấy ngày từ form
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        # Kiểm tra đăng nhập
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        user = User.objects.get(user_id=user_id)

        # Chuyển thành object date
        try:
            check_i = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_o = datetime.strptime(check_out, "%Y-%m-%d").date()
        except ValueError:
            return render(request, 'book_room.html', {
                'room': room,
                'error': 'Vui lòng nhập đúng định dạng ngày.'
            })

        # Kiểm tra logic ngày
        nights = (check_o - check_i).days
        if nights <= 0:
            return render(request, 'book_room.html', {
                'room': room,
                'error': 'Ngày trả phải sau ngày nhận phòng.'
            })

        # Kiểm tra xem đã có người đặt trong khoảng ngày đó chưa
        overlap = Booking.objects.filter(
            room=room,
            check_in__lt=check_o,   # người khác check_in trước khi mình check_out
            check_out__gt=check_i   # người khác check_out sau khi mình check_in
        ).exists()

        if overlap:
            messages.error(request, "❌ Phòng này đã được đặt trong khoảng thời gian bạn chọn.")
            return redirect('room_detail', room_id=room.room_id)

        # Tính tổng tiền
        total = room.price_per_night * nights

        # Tự sinh booking_id
        max_id = Booking.objects.aggregate(Max('booking_id'))['booking_id__max'] or 0
        new_id = max_id + 1

        # Lưu booking mới
        Booking.objects.create(
            booking_id=new_id,
            user=user,
            room=room,
            check_in=check_i,
            check_out=check_o,
            total=total
        )

        messages.success(request, "🎉 Đặt phòng thành công!")
        return redirect('my_bookings')

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
