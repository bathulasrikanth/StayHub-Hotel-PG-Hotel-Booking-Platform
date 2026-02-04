from rest_framework import serializers

from .models import User,Property,Room,Booking

class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ("username","email","password","role")

    def create(self,validated_data):
        user = User.objects.create_user(
        username = validated_data['username'],
        email = validated_data['email'],
        password = validated_data["password"],
        role = validated_data.get('role','CUSTOMER')
        )
        return user
    

class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    status = serializers.ReadOnlyField()
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id',
            'name',
            'property_type',
            'address',
            'city',
            'description',
            'amenities',
            'status',
            'owner',
            'is_available',
            'created_at'
        ]

    def get_is_available(self, obj):
        # Property is available if at least one room is available
        return obj.rooms.filter(is_available=True).exists()


class RoomSerializer(serializers.ModelSerializer):
    is_available = serializers.ReadOnlyField()
    class Meta:
        model = Room
        fields = [
            'id','property','room_type','price','total_units','available_units','is_available','created_at'
        ]

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = [
            'room',
            'quantity',
            'check_in',
            'check_out'
        ]
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        return value
    def validate(self, data):
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date"
            )
        return data


class MyBookingSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source = "property.name",read_only = True)
    room_type = serializers.CharField(source = "room.room_type",read_only = True)
    class Meta:
        model = Booking
        fields = [
            'id',
            'property_name',
            'room_type',
            'check_in',
            'check_out',
            'quantity',
            'status',
            'total_price',
            'created_at'
        ]

class VendorBookingViewSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source = 'user.username',read_only = True)
    property_name = serializers.CharField(source = 'property.name',read_only = True)
    room_type = serializers.CharField(source = 'room.room_type',read_only = True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'customer',
            'property_name',
            'room_type',
            'check_in',
            'check_out',
            'quantity',
            'status',
            'total_price',
            'created_at'

        ]