from rest_framework import serializers
from .models import Organization, CustomUser, Transaction, Wallet

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'organization', 'role', 'password']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):

        password = validated_data.pop('password', None)

        user = super().create(validated_data)

        if password:
            user.set_password(password)
            user.save()
            
        return user
    
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'organization', 'balance', 'created_at']

        read_only_fields = ['id','balance', 'created_at']    

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'maker', 'checker', 'amount', 'state', 'created_at'] 

        read_only_fields = ['id', 'maker', 'state', 'created_at']       