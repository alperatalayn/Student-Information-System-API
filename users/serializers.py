from rest_framework import serializers 
from .models import CustomUser
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (['first_name','id'])
        extra_kwargs = {'password': {'write_only': True},'id':{'read_only':True}}

    def create(self, validated_data):
        try:     
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance
        except:
            raise Exception("Error while creating user")