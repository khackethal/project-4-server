from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt


from .serializers import UserSerializer, UserProfileSerializer

User = get_user_model()

class RegisterView(APIView):

    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response(
                {'message: Registration Succesfull'},
                status=status.HTTP_201_CREATED
            )
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied({'detail': 'Unauthorized'})

        if not user_to_login.check_password(password):
            raise PermissionDenied({'detail': 'Unauthorized'})

        expiry_time = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            {'sub': user_to_login.id, 'exp':  int(expiry_time.strftime('%s'))},
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return Response(
            {'token': token, 'message': f'Welcome back {user_to_login.username}'}
        )


class ProfileView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, _request, pk):
        try :
            user = User.objects.get(pk=pk)
            serialized_user = UserSerializer(user)
            return Response(data=serialized_user.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise NotFound()


class EditProfileView(APIView):

    permission_classes = (IsAuthenticated, )

    def get_profile(self, pk):
        try :
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound()

    def put(self, request, pk):
        profile_to_update = self.get_profile(pk=pk)
        if profile_to_update.id != request.user.id:
            raise PermissionDenied()

        request.data['owner'] = request.user.id
        updated_profile = UserProfileSerializer(profile_to_update, data=request.data)
        if updated_profile.is_valid():
            updated_profile.save()
            return Response(updated_profile.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_profile.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        

  

