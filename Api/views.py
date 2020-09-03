from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate


# Create your views here.

@api_view(['POST'])
def LoginView(request):
    if request.method == 'POST':
        print(request.data)
        if request.data is not None:
            username = User.objects.filter(username=request.data["username"])
            if username.count() > 0:
                user = authenticate(username=request.data["username"], password=request.data["password"])
                if user is not None:
                    if user.is_active and user.is_staff:
                        print("Superuser Valid user and exist")
                        serializer = LoginSerializer(data=request.data)
                        if serializer.is_valid():
                            return Response({'message': 'successfully login', 'is_admin': 'true'},
                                            status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    elif user.is_active and not user.is_staff:
                        print("Valid user but not a Staff user")
                        serializer = LoginSerializer(data=request.data)
                        if serializer.is_valid():
                            return Response({'message': 'successfully login', 'is_admin': 'false'},
                                            status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    print("Invalid Password")
                    serializer = LoginSerializer(data=request.data)
                    if serializer.is_valid():
                        return Response({'message': 'Invalid Password'}, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("Wrong Username Provided")
                serializer = LoginSerializer(data=request.data)
                if serializer.is_valid():
                    return Response({'message': 'Invalid Username'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        print("Null Data")
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)