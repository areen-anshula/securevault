import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        MAKER = 'MAKER', 'Maker'
        CHECKER = 'CHECKER', 'Checker'
        AUDITOR = 'AUDITOR', 'Auditor'
        ADMIN = 'ADMIN', 'Admin'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default="")
    email = models.EmailField(unique=True)

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MAKER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    

class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.OneToOneField('Organization', on_delete=models.CASCADE, related_name='wallet', default=None)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='transactions')
    maker = models.ForeignKey('CustomUser', on_delete=models.PROTECT, related_name='made_transactions', default=None)
    checker = models.ForeignKey('CustomUser', on_delete=models.PROTECT, related_name='approved_transactions', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)    
    state = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)