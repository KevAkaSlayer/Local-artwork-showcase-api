from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Artist, Artwork
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.bio
        token['profile_pic'] = user.profile_pic.url

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Artist.objects.all())]
    )

    class Meta:
        model = Artist
        fields = ('username', 'email', 'password', 'password2', 'bio', 'profile_pic')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = Artist.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data['bio'],
            profile_pic=validated_data['profile_pic']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    artworks = ArtworkSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'