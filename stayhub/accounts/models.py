from django.db import models



from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN','Admin'),
        ('VENDOR','Vendor'),
        ('CUSTOMER','Customer')
    )
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='CUSTOMER')
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} - {self.role}"
    
class Property(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ('HOTEL','Hotel'),
        ('PG','pg'),
        ('HOSTEL','Hostel')
    )
    status_type = (
        ('PENDING','Pending'),
        ("APPROVED",'Approved'),
        ('REJECTED','Rejected')
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    property_type = models.CharField(max_length= 20,choices=PROPERTY_TYPE_CHOICES,default='HOSTEL')
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=200)
    description = models.TextField()
    amenities = models.TextField(help_text="Comma separated values")
    status = models.CharField(max_length= 20,choices=status_type,default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    
class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.FileField(upload_to='property_images/')




class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('BED', 'Bed'), 
    ) 
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='rooms')
    room_type = models.CharField(max_length=20,choices=ROOM_TYPE_CHOICES)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    total_units = models.PositiveIntegerField()
    available_units = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.is_available = self.available_units > 0
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.property.name} - {self.room_type}"

class Booking(models.Model):

    BOOKING_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='bookings')
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='bookings')
    room = models.ForeignKey(Room,
    on_delete=models.CASCADE,
    related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    quantity = models.PositiveIntegerField()
    status = models.CharField( max_length=20, choices=BOOKING_STATUS_CHOICES,default='PENDING')
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user.username}"



class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('INITIATED', 'Initiated'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed')
    )
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,related_name = 'payments')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'payments')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default='INITIATED')
    provider = models.CharField(max_length=50,default='MOCK')
    provider_order_id = models.CharField(max_length=100,blank=True,null=True)
    provider_payment_id = models.CharField(max_length=100,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
