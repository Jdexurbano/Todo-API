from django.contrib.auth.models import User
from core.models import Task
from rest_framework import serializers

#serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only = True,required = True)
    password2 = serializers.CharField(write_only = True,required = True)

    class Meta:
        model = User
        fields = ['username','password1','password2','email']

    def validate(self, attrs):
        #check if the password is match
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password":"passwords do not match"})
        return attrs
    
    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']


#serializer for user
class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','email','password']



#serializer for tasks
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','user','title','content','is_done','created_at','updated_at']
    
    def create(self, validated_data):
        user = self.context['user'] #get the user that pass through the context
        validated_data.pop('user',None) #remove the user if it exist in validated data
        task = Task.objects.create(user = user,**validated_data) #assign the pass user when creating task
        return task