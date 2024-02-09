from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from account.utils import Util
# from authenticate.utils import Util
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True},
        }
#validate password and confirm password
    def validate(self,attrs):
     password=attrs.get('password')
     password2=attrs.get('password2')
     if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
     return attrs
    def create(self, validated_data):
     return User.objects.create_user(**validated_data)
 
class UserLoginSerializer(serializers.ModelSerializer):
     email=serializers.EmailField(max_length=255)
     class Meta:
         model=User
         fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name']
class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2=serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields=['password','password2']
    
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and confirm password does't match")
        user.set_password(password)
        user.save()
        return attrs
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
        
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
           user=User.objects.get(email=email)
           uid = urlsafe_base64_encode(force_bytes(user.id))
           print('Encode UID', uid)
           token=PasswordResetTokenGenerator().make_token(user)
           print('Password Reset Token',token)
           link='http://localhost:3000/api/user/reset/'+uid+'/'+token
           print('Password Reset link', link)
           #Send email
           body='Click following link to reset your password' + link
           data={
               'subject':'Reset your Password',
               'body': body,
               'to_email':user.email
               
           }
           Util.send_email(data)
           return attrs
           
        else:
            raise ValidationErr('You are not a registered user')

class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2=serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields=['password','password2']
    
    def validate(self,attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password != password2:
             raise serializers.ValidationError("password and confirm password does't match")
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
             raise ValidationError('Token is not valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is not valid or Expired')
            
    