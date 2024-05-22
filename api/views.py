from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Artist, Artwork
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer, ArtworkSerializer, LoginSerializer, logoutSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from django.http import JsonResponse


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(APIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                 email = serializer.validated_data['email']
                 user = Artist.objects.filter( email= email).exists()
                 if user :return Response("User with this email already exist",status=status.HTTP_406_NOT_ACCEPTABLE)
                 user = serializer.save()
                 user.save()
                 return Response({"status":1})
            except Exception as e:
                return Response("User with this email already exist",status=status.HTTP_406_NOT_ACCEPTABLE)
                 
        return Response(serializer.errors)




class loginView(APIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username = username,password = password)
            if not user or user == None:return Response({'error' : "Invalid Credential"})
            Refresh=RefreshToken.for_user(user)
            login(request,user)
            return Response({ "access" :str( Refresh.access_token), 'refresh':str( Refresh),'user_id' : user.id,"status":1 ,'username':username,},status=status.HTTP_200_OK)
        
        return Response(serializer.errors)

class LogoutView(APIView):
    serializer_class = logoutSerializer
    def post(self, request):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            refresh_token  = serializer.validated_data['refresh_token']
            try:
                logout(request)
                RefreshToken(refresh_token).blacklist()
                return Response("successfully logged out",status=status.HTTP_200_OK)
            except Exception as e:
                    return Response("something went wrong",status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)

class Profile(APIView): 
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user=request.user
        profile_picture_url = request.build_absolute_uri(user.profile_pic.url) if user.profile_pic else None
        return JsonResponse({"email":user.email,'user_id' : user.id,"status":1 ,'username':user.username,'bio':user.bio,'profile_pic':profile_picture_url,},status=status.HTTP_200_OK) 
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Artworks(request):
    public_works = Artwork.objects.filter(is_public=True)
    user_works = request.user.artworks.all()
    artworks = public_works | user_works
    serializer = ArtworkSerializer(artworks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ArtworkList(request):
    artworks = Artwork.objects.all()
    serializer = ArtworkSerializer(artworks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ArtworkDetail(request, pk):
    artworks = Artwork.objects.get(id=pk)
    serializer = ArtworkSerializer(artworks, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createArtwork(request):
    data = request.data
    Artwork = Artwork.objects.create(
        body=data['body']
    )
    serializer = ArtworkSerializer(Artwork, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateArtwork(request, pk):
    data = request.data
    Artwork = Artwork.objects.get(id=pk)
    serializer = ArtworkSerializer(instance=Artwork, data=data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def deleteArtwork(request, pk):
    Artwork = Artwork.objects.get(id=pk)
    Artwork.delete()
    return Response('Artwork was deleted!')

