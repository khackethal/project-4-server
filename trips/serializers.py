from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Trip, Comment, UserTripList
User = get_user_model()

# UNPOPULATED
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'profile_image')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = '__all__'

class UserTripListSerializer(serializers.ModelSerializer):   
    class Meta:
        model = UserTripList
        fields = '__all__'



# POPULATED
class PopulatedCommentSerialzer(CommentSerializer):
    owner = UserSerializer()


class PopulatedTripSerializer(TripSerializer):
    owner = UserSerializer()
    comments = PopulatedCommentSerialzer(many=True)
    liked_by = UserSerializer(many=True)


class PopulatedUserTripListSerializer(UserTripListSerializer):
    owner = UserSerializer()
    trips = PopulatedTripSerializer(many=True)



class PopulatedUserSerializer(UserSerializer):
    trips = PopulatedTripSerializer(many=True)
    comments = PopulatedCommentSerialzer(many=True)
    trip_lists = PopulatedUserTripListSerializer(many=True)
