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
    list_display = ('email','username','organization','role','is_staff')
    list_filter = ('role','is_staff','is_superuser','is_active')
    search_fields = ('email','username')

    fieldsets = UserAdmin.fieldsets + (
        ('SecureVault Roles & Tenancy', {'fields':('organization', 'role')}),
    )

@admin.register(Wallet) 
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id','customUser','balance','created_at')
    search_fields = ('customUser',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','customUser','wallet','amount','state','created_at')
    list_filter = ('state',)
    search_fields = ('customUser',)
           