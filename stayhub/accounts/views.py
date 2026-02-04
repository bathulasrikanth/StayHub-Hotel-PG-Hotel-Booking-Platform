from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status,permissions
from .serializers import RegisterSerializers,PropertySerializer,RoomSerializer,BookingSerializer,MyBookingSerializer,VendorBookingViewSerializer
from .models import Property,Room,Booking,Payment
from .permissions import IsVendor,IsCustomer
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Sum
from django.db import transaction

class RegisterAPIView(APIView):
    def post(self,request):
        serializer = RegisterSerializers(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message" : "user register successfull"},
                status = status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    

class VendorPropertyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,IsVendor]

    def get(self,request):
        properties = Property.objects.filter(owner = request.user)
        serializer = PropertySerializer(properties,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PropertySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(owner = request.user)
            return Response(
                {"message" : "Property submitted for approval"},
                status = status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
    

class PublicPropertyListAPIView(APIView):
    def get(self, request):
        properties = Property.objects.filter(status='APPROVED')
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)

class VendorRoomAPIView(APIView):
    permission_classes = [IsAuthenticated,IsVendor]
    def post(self,request):
        property_id = request.data.get('property')

        try:
            property_obj = Property.objects.get(
                id = property_id,
                owner = request.user
            )
        except Property.DoesNotExist:
            return Response(
                {
                    "error" : "Invalid property"
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = RoomSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(property = property_obj)
            return Response(
                {'message' : 'Room added SuccessFully'},
                status = status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        rooms = Room.objects.filter(propery_owner = request.user)
        serializer = RoomSerializer(rooms,many = True)
        return Response(serializer.data)


class PublicRoomListAPIView(APIView):
    def get(self, request, property_id):
        rooms = Room.objects.filter(
            property__id=property_id,
            property__status='APPROVED',
            is_available=True
        )
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class BookingAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    @transaction.atomic
    def post(self, request):
        serializer = BookingSerializer(data=request.data)

        # 1️ Validate input
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        room = serializer.validated_data['room']
        quantity = serializer.validated_data['quantity']
        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']

        # 2️ Property must be approved
        if room.property.status != 'APPROVED':
            return Response(
                {"error": "Property is not approved for booking"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3️ Check availability
        if room.available_units < quantity:
            return Response(
                {"error": "Not enough rooms/beds available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4️ Lock availability
        room.available_units -= quantity
        room.save()

        # 5️ Calculate price (simple version)
        total_price = room.price * quantity

        # 6️ Create booking
        booking = Booking.objects.create(
            user=request.user,
            property=room.property,
            room=room,
            quantity=quantity,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            status='CONFIRMED'
        )

        return Response(
            {
                "message": f"Booking confirmed successfully - {booking.user}",
                "booking_id": booking.id,
                "total_price": booking.total_price
            },
            status=status.HTTP_201_CREATED
        )


class CancellationBookingAPIView(APIView):
    permission_classes = [IsAuthenticated,IsCustomer]

    @transaction.atomic
    def put(self,request,booking_id):
        try:
            booking = Booking.objects.select_for_update().get(
                id = booking_id,
                user = request.user
            )
        except Booking.DoesNotExist:
            return Response(
                {"error" : "Booking not Found"},
                status = status.HTTP_404_NOT_FOUND
            )
        if booking.status != "CONFIRMED":
            return Response(
                {"error" : "Only confirmed Bookings can be cancelled"},
                status  = status.HTTP_400_BAD_REQUEST
            )
        room = booking.room

        room.available_units += booking.quantity
        room.save()

        booking.status = "CANCCELLED"
        booking.save()

        return Response(
            {"message" : "Booking Cancelled Successfully"},
            status  = status.HTTP_200_OK
        )
    
    
class ViewBookingAPIView(APIView):
    permission_classes = [IsAuthenticated,IsCustomer]
    def get(self,request):
        bookings = Booking.objects.filter(
            user = request.user,
        ).order_by('-created_at')
        serializer = MyBookingSerializer(bookings,many = True)
        return Response(serializer.data)

        
class VendorBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated,IsVendor]
    def get(self,request):
        bookings = Booking.objects.filter(
            property__owner = request.user
        ).order_by('-created_at')
        serializer = VendorBookingViewSerializer(bookings,many = True)
        return Response(serializer.data)
    
class vendorDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated,IsVendor]

    def get(self,request):

        vendor = request.user
        total_properties = Property.objects.filter(owner=vendor).count()

        total_rooms = Room.objects.filter(
            property__owner=vendor
        ).count()

        total_bookings = Booking.objects.filter(
            property__owner=vendor
        ).count()

        active_bookings = Booking.objects.filter(
            property__owner=vendor,
            status='CONFIRMED'
        ).count()

        cancelled_bookings = Booking.objects.filter(
            property__owner=vendor,
            status='CANCELLED'
        ).count()

        total_revenue = Booking.objects.filter(
            property__owner=vendor,
            status='CONFIRMED'
        ).aggregate(
            revenue=Sum('total_price')
        )['revenue'] or 0
        return Response({
            "total_properties": total_properties,
            "total_rooms": total_rooms,
            "total_bookings": total_bookings,
            "active_bookings": active_bookings,
            "cancelled_bookings": cancelled_bookings,
            "total_revenue": total_revenue
        })
    

class CreatePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated,IsCustomer]

    @transaction.atomic
    def post(self,request):
        booking_id = request.data.get('booking_id')
        if not booking_id:
            return Response(
                {"error" : "booking_id is required"},
                status = status.HTTP_400_BAD_Request
            )
        try:
            booking = Booking.objects.select_for_update().get(
                id = booking_id,
                user = request.user
            )
        except Booking.DoesNotExist:
            return Response(
                {"error" : "Booking Not Found"},
                status = status.HTTP_404_NOT_FOUND
            )
        if booking.status != 'CONFIRMED':
            return Response(
                {'error' : 'Payment allowed only for Confirmed'},
                status = status.HTTP_404_NOT_FOUND
            )
        if Payment.objects.filter(
            booking = booking,
            status = 'INITIATED').exists():
            return Response(
                {'error' : 'Payment already initiated'},
                status = status.HTTP_400_BAD_REQUEST
            )
        payment = Payment.objects.create(
            booking = booking,
            user = request.user,
            amount = booking.total_price,
            status = 'INITIATED',
            provider = 'MOCK'
        )
        return Response(
            {
                "message": "Payment initiated",
                "payment_id": payment.id,
                "amount": payment.amount,
                "provider": payment.provider
            },
            status=status.HTTP_201_CREATED 
        )
class paymentSuccessAPIView(APIView):
    permission_classes = [IsAuthenticated,IsCustomer]

    @transaction.atomic
    def post(self,request):
        payment_id = request.data.get('payment_id')
        provider_payment_id = request.data.get('provider_payment_id')

        if not payment_id or not provider_payment_id:
            return Response(
                {"error": "Payment id and provider_payment_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            payment = Payment.objects.select_for_update().get(
                id=payment_id,
                user=request.user
            )
        except Payment.DoesNotExist:
            return Response(
              {  "error" : "Payment Not Found"},
              status = status.HTTP_404_NOT_FOUND
            )
        if payment.status != 'INITIATED':
            return Response(
                {"error": "Payment already processed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking = payment.booking

        payment.status = 'SUCCESS'
        payment.provider_payment_id = provider_payment_id
        payment.save()

        booking.status = 'COMPLETED'
        booking.save()

        return Response(
            {
                "message": "Payment successful and booking completed",
                "booking_id": booking.id,
                "payment_id": payment.id
            },
            status=status.HTTP_200_OK
        )
    
class PaymentFailureAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    @transaction.atomic
    def post(self, request):
        payment_id = request.data.get('payment_id')
        reason = request.data.get('reason', 'Payment failed')

        if not payment_id:
            return Response(
                {"error": "payment_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment = Payment.objects.select_for_update().get(
                id=payment_id,
                user=request.user
            )
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if payment.status != 'INITIATED':
            return Response(
                {"error": "Payment already processed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.status = 'FAILED'
        payment.save()

        return Response(
            {
                "message": "Payment marked as failed",
                "payment_id": payment.id,
                "retry_allowed": True,
                "reason": reason
            },
            status=status.HTTP_200_OK
        )