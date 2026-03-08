from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organization, CustomUser, Wallet, Transaction

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name','id','is_active','created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email','username','Organization','role','is_staff')
    list_filter = ('role','is_staff','is_superuser','is_active')
    search_fields = ('email','username')

    fieldsets = UserAdmin.fieldsets + (
        ('SecureVault Roles & Tenancy', {'fields':('Organization', 'role')}),
    )

@admin.register(Wallet) 
class WalletAdmin(admin.ModelAdmin):
    list_display = ('CustomUser_id','balance','created_at')
    search_fields = ('CustomUser_id__email',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','customuser','amount','status','created_at')
    list_filter = ('status',)
    search_fields = ('customuser__email',)
           