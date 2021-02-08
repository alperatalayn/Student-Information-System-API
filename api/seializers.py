from rest_framework import serializers
from .models import Course,Class
from django.conf import settings
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CourseSerializer(serializers.ModelSerializer):
    instructor = CustomUserSerializer(many=False,required=False)
    students = CustomUserSerializer(many=True,required=False)
    class Meta:
        model = Course
        fields = "__all__"
    def create(self, validated_data,instructor):
        try:
            course = Course.objects.create(**validated_data,instructor=instructor)
            return course
        except:
            raise Exception("cannot create Course")
    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name', instance.name)
            instance.credit = validated_data.get('credit', instance.credit)        
            instance.save()
        except:
            raise Exception("cannot update Course") 
class ClassSerializer(serializers.ModelSerializer):
    students = CustomUserSerializer(many=True,required=False)
    class Meta:
        model = Class
        fields = "__all__"
    def create(self, validated_data):
        try:    
            course = Class.objects.create(**validated_data)
            return course
        except:
            raise Exception("cannot create class") 
    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name', instance.name)
            instance.save()
        except: 
            raise Exception("cannot update class")
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('user_name','password')
        extra_kwargs = {'password':{'write_only':True}}
    def create(self,validated_data):
        try:    
            password = validated_data.pop('password',None)
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance
        except:
            raise Exception("Error while creating user")
