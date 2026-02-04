from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterAPIView,VendorPropertyAPIView,PublicPropertyListAPIView,VendorRoomAPIView,PublicRoomListAPIView,BookingAPIView,CancellationBookingAPIView,ViewBookingAPIView,VendorBookingsAPIView,vendorDashboardAPIView,CreatePaymentAPIView,paymentSuccessAPIView,PaymentFailureAPIView
urlpatterns = [
    path("register/",RegisterAPIView.as_view()),
    path("login/",TokenObtainPairView.as_view()),
    path("vendor/properties/",VendorPropertyAPIView.as_view()),
    path("properties/",PublicPropertyListAPIView.as_view()),
    path('vendor/rooms/',VendorRoomAPIView.as_view()),
    path('properties/<int:property_id>/rooms/',PublicRoomListAPIView.as_view()),
    path('room/booking/',BookingAPIView.as_view()),
    path("bookings/<int:booking_id>/cancel/",CancellationBookingAPIView.as_view()),
    path('bookings/my/',ViewBookingAPIView.as_view()),
    path('vendor/bookings/',VendorBookingsAPIView.as_view()),
    path('vendor/dashboard/',vendorDashboardAPIView.as_view()),
    path('create/payment/',CreatePaymentAPIView.as_view()),
    path('payment/success/',paymentSuccessAPIView.as_view()),
    path('payment/success/',PaymentFailureAPIView.as_view())
]



