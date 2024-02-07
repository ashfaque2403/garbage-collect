from django.contrib import admin
from .models import CompanyAdministrator,Customer,Complaint,Driver,CustomUser,GarbageCollector,ReplyComplaint,PaymentReport,GarbageCollectedReport
# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'is_driver', 'is_garbagecollector', 'is_companyadmin')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_driver', 'is_garbagecollector', 'is_companyadmin'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_driver', 'is_garbagecollector', 'is_companyadmin')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(CompanyAdministrator)
admin.site.register(Customer)
admin.site.register(Complaint)

class Garbage(admin.ModelAdmin):
    exclude=('payment_text',)
admin.site.register(GarbageCollector,Garbage)
admin.site.register(Driver)
admin.site.register(ReplyComplaint)
admin.site.register(PaymentReport)
admin.site.register(GarbageCollectedReport)