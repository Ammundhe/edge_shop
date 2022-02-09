from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from product.models import product, productCategory
from cart.models import Cart

class user_serializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            'id',
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password'
        ]
        extra_kwargs={
            'password':{'write_only':True}
            }

    def create(self, validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    def update(self, instance, validated_data):
        instance.username=validated_data.get('username', instance.username)
        instance.first_name=validated_data.get('first_name', instance.first_name)
        instance.last_name=validated_data.get('last_name', instance.last_name)
        instance.email=validated_data.get('email', instance.email)
        instance.set_password=validated_data.get('set_password', instance.set_password)
        instance.save()
        return instance
    
class productCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=productCategory
        fields=['name',]

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model=product
        fields=['product_category','name','decriptions','price','stock','cover_image','stock_status']
        depth=1

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['id','user', 'product', 'quantity']
    



