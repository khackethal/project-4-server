from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Trip, Comment, UserTripList
from .serializers import UserSerializer, CommentSerializer, TripSerializer, UserTripListSerializer, PopulatedCommentSerialzer, PopulatedTripSerializer, PopulatedUserTripListSerializer, PopulatedUserSerializer


## TRIP VIEW ALL

class TripListView(APIView):

    permission_classes = (IsAuthenticated, )

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
            trip_to_favorite = Trip.objects.get(pk=pk)
            if request.user in trip_to_favorite.favorited_by.all():
                trip_to_favorite.favorited_by.remove(request.user.id)
            else:
                trip_to_favorite.favorited_by.add(request.user.id)
            trip_to_favorite.save()
            serialized_dinosaur = PopulatedTripSerializer(trip_to_favorite)
            return Response(serialized_dinosaur.data, status=status.HTTP_202_ACCEPTED)
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


## CREATE NEW TRIP LIST