from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.http import Http404
from app.models import User
from app.serializers import UserSerializer

class UserListAPIView(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'count': users.count()
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An error occurred while fetching users.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'User created successfully.',
                    'data': UserSerializer(user).data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Validation failed.',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except IntegrityError as e:
            if 'email' in str(e):
                return Response({
                    'status': 'error',
                    'message': 'User with this email already exists.',
                    'errors': {'email': ['This email is already registered.']}
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Database integrity error.',
                    'details': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An error occurred while creating the user.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailAPIView(APIView):
    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except (User.DoesNotExist, ValueError):
            return None

    def get(self, request, user_id):
        try:
            user = self.get_object(user_id)
            if not user:
                return Response({
                    'status': 'error',
                    'message': 'User not found.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserSerializer(user)
            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An error occurred while fetching the user.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, user_id):
        try:
            user = self.get_object(user_id)
            if not user:
                return Response({
                    'status': 'error',
                    'message': 'User not found.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'User updated successfully.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Validation failed.',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except IntegrityError as e:
            if 'email' in str(e):
                return Response({
                    'status': 'error',
                    'message': 'User with this email already exists.',
                    'errors': {'email': ['This email is already registered.']}
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Database integrity error.',
                    'details': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An error occurred while updating the user.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, user_id):
        try:
            user = self.get_object(user_id)
            if not user:
                return Response({
                    'status': 'error',
                    'message': 'User not found.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            user.delete()
            return Response({
                'status': 'success',
                'message': 'User deleted successfully.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An error occurred while deleting the user.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

