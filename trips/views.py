from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Trip, Comment, UserTripList
from .serializers import CommentSerializer, TripSerializer, UserTripListSerializer, PopulatedTripSerializer, PopulatedUserTripListSerializer, UpdatedUserTripListSeralizer


## TRIP VIEW ALL

class TripListView(APIView):

    def get(self, _request):
        trips = Trip.objects.all()
        serialized_trips = PopulatedTripSerializer(trips, many=True)
        return Response(serialized_trips.data, status=status.HTTP_200_OK)


# POST NEW TRIP
    def post(self, request):
        request.data['owner'] = request.user.id
        new_trip = TripSerializer(data=request.data)
        if new_trip.is_valid():
            new_trip.save()
            return Response(new_trip.data, status=status.HTTP_201_CREATED)
        return Response(new_trip.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# TRIP DETAIL VIEW and methods
class TripDetailView(APIView):

    permission_classes = (IsAuthenticated, )
#FIND MATCH
    def get_trip(self, pk):
        try:
            return Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            raise NotFound()
# SHOW ONE
    def get(self, _request, pk):
        trip = self.get_trip(pk=pk)
        serialized_trip = PopulatedTripSerializer(trip)
        return Response(serialized_trip.data, status=status.HTTP_200_OK)

# UPDATE TRIP
    def put(self, request, pk):
        trip_to_update = self.get_trip(pk=pk)
        if trip_to_update.owner != request.user:
            raise PermissionDenied()
        request.data['owner'] = request.user.id
        updated_trip = TripSerializer(trip_to_update, data=request.data)
        if updated_trip.is_valid():
            updated_trip.save()
            return Response(updated_trip.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_trip.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

# DELETE TRIP
    def delete(self, request, pk):
        trip_to_delete = self.get_trip(pk=pk)
        if trip_to_delete.owner != request.user:
            raise PermissionDenied()
        trip_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# TRIP LIKE VIEW
class TripLikeView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        try:
            trip_to_like = Trip.objects.get(pk=pk)
            if request.user in trip_to_like.liked_by.all():
                trip_to_like.liked_by.remove(request.user.id)
            else:
                trip_to_like.liked_by.add(request.user.id)
            trip_to_like.save()
            serialized_trip = PopulatedTripSerializer(trip_to_like)
            return Response(serialized_trip.data, status=status.HTTP_202_ACCEPTED)
        except Trip.DoesNotExist:
            raise NotFound()


## COMMENT POST
class CommentListView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, trip_pk):
        request.data['trip'] = trip_pk
        request.data['owner'] = request.user.id
        serialized_comment = CommentSerializer(data=request.data)
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
        return Response(serialized_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


## COMMENT DELETE
class CommentDetailView(APIView):

    def delete(self, request, _trip_pk, comment_pk):
        try:
            comment_to_delete = Comment.objects.get(pk=comment_pk)
            if comment_to_delete.owner != request.user:
                raise PermissionDenied()
            comment_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise NotFound()


## VIEW ALL TRIP LISTS

class UserTripListView(APIView):
    
    permission_classes = (IsAuthenticated, )

    def get(self, _request):
        lists = UserTripList.objects.all()
        serialized_trips = PopulatedUserTripListSerializer(lists, many=True)
        return Response(serialized_trips.data, status=status.HTTP_200_OK)
    
## POST A NEW LIST
    def post(self, request):
        request.data['owner'] = request.user.id
        new_list = UserTripListSerializer(data=request.data)
        if new_list.is_valid():
            new_list.save()
            return Response(new_list.data, status=status.HTTP_201_CREATED)
        return Response(new_list.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


## VIEW A SINGLE LIST and METHODS
class UserTripListDetailView(APIView):

    permission_classes = (IsAuthenticated, )
#FIND MATCH
    def get_list(self, pk):
        try:
            return UserTripList.objects.get(pk=pk)
        except UserTripList.DoesNotExist:
            raise NotFound()
# SHOW ONE
    def get(self, _request, pk):
        user_list = self.get_list(pk=pk)
        serialized_list = PopulatedUserTripListSerializer(user_list)
        return Response(serialized_list.data, status=status.HTTP_200_OK)

# DELETE LIST
    def delete(self, request, pk):
        list_to_delete = self.get_list(pk=pk)
        if list_to_delete.owner != request.user:
            raise PermissionDenied()
        list_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


## RENAME LIST OR CHANGE PRIVACY SETTINGS 
    def put(self, request, pk):
        list_to_update = self.get_list(pk=pk)
        if list_to_update.owner != request.user:
            raise PermissionDenied()
        request.data['owner'] = request.user.id
        updated_list = UpdatedUserTripListSeralizer(list_to_update, data=request.data)
        if updated_list.is_valid():
            updated_list.save()
            return Response(updated_list.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_list.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)





# # ADD A TRIP TO A LIST/ TOGGLE TO REMOVE A TRIP FROM A LIST
class TripAddListView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, trip_pk, list_pk):
        try:
            trip_to_list = Trip.objects.get(pk=trip_pk)
            user_list = UserTripList.objects.get(pk=list_pk)

            if trip_to_list in user_list.trips.all():
                trip_to_list.listed_by.remove(request.user.id)
                user_list.trips.remove(trip_to_list.id)
                serialized_list = PopulatedUserTripListSerializer(user_list)
                return Response(serialized_list.data, status=status.HTTP_202_ACCEPTED)
            else:
                trip_to_list.listed_by.add(request.user.id)
                user_list.trips.add(trip_to_list.id)
                trip_to_list.save()
                user_list.save()
                serialized_list = PopulatedUserTripListSerializer(user_list)
                return Response(serialized_list.data, status=status.HTTP_202_ACCEPTED)
        except Trip.DoesNotExist:
            raise NotFound()
