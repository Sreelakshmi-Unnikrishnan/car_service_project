from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import logout as auth_logout

@api_view(['POST'])
def register(request): 
    if request.method == 'POST':
        user_serializer = RegisterSerializer(data=request.data)
        if user_serializer.is_valid():
            
            user = User.objects.create_user(user_serializer.data['username'], user_serializer.data['email'], user_serializer.data['password'])

            try:
                user = User.objects.get(username=user_serializer.data['username'])
            except:
                return Response({"Error": "Invalid credentials!"}, status=status.HTTP_403_FORBIDDEN) 
        
            token = Token.objects.create(user=user)
            data = {"Token": token.key}
            return Response(data, status=status.HTTP_200_OK)
        data = {'Error':'User already exist!'}
        return Response(data, status=status.HTTP_201_CREATED)
    
@api_view(['GET']) 
def logout(request):
    auth_logout(request)
    data = {'Success': 'Sucessfully logged out'}
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def home(request): 
    if request.method == 'GET':
        try:
            services = Service.objects.all()
            service_serializer = ServiceSerializer(services, many = True)
            return Response(service_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "Somthing went wrong!"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def listing(request,pk): 
    if request.method == 'GET':
        try:
            services = Service.objects.get(id=pk)
            service_serializer = ServiceSerializer(services)
            return Response(service_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "Somthing went wrong!"}, status=status.HTTP_403_FORBIDDEN)  

@api_view(['POST']) 
def add_service(request):   
    if request.method == 'POST':
        try:
            user = request.data['user']
        except KeyError:
            return Response({'Error': 'name not provided'}, status=status.HTTP_400_BAD_REQUEST) 
        
        try:
            address = request.data['address']
        except KeyError:
            return Response({'Error': 'address not provided'}, status=status.HTTP_400_BAD_REQUEST)  

        try:
            car_model = request.data['car_model']
        except KeyError:
            return Response({'Error': 'car_model not provided'}, status=status.HTTP_400_BAD_REQUEST) 
        
        try:
            number_plate_no = request.data['number_plate_no']
        except KeyError:
            return Response({'Error': 'number_plate_no not provided'}, status=status.HTTP_400_BAD_REQUEST) 
        
        try:
            service_name = request.data['service_name']
        except KeyError:
            return Response({'Error': 'servicename not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service_date = request.data['service_date']
        except KeyError:
            return Response({'Error': 'date not provided'}, status=status.HTTP_400_BAD_REQUEST)  


        try:
            user_qry = User.objects.get(username=user)
        except User.DoesNotExist:
            return Response({'Error': 'Invalid provided data of user'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service_qry = Service.objects.get(service_name=service_name)
        except Service.DoesNotExist:
            return Response({'Error': 'Invalid provided data of service'}, status=status.HTTP_400_BAD_REQUEST) 

        link = Buyer.objects.create(service_name=service_qry,user=user_qry,address=address,car_model=car_model,number_plate_no=number_plate_no,service_date=service_date)
        serializer = BuyerSerializer(link)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    return Response(serializer.error, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def service_issue_detail(request, token):
    if request.method == 'GET':
        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            token = None
            return Response({"Error": "Invalid token!"}, status=status.HTTP_400_BAD_REQUEST)

        service_issue = Buyer.objects.filter(user__id=token.user_id).order_by("-id") 
        serviceissued_serializer = BuyerSerializer(service_issue, many = True)
        return Response(serviceissued_serializer.data, status=status.HTTP_200_OK)