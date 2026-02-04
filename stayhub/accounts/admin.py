from django.contrib import admin
from .models import User,Property,PropertyImage,Room,Booking,Payment


admin.site.register(User)
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'property_type', 'status', 'owner', 'city')
    list_filter = ('property_type', 'status', 'city')
    search_fields = ('name', 'city')

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'property')
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Payment)
