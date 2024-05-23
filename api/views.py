from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Artist, Artwork
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer, ArtworkSerializer, LoginSerializer, logoutSerializer,ProfileUpdateSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser


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
                 return Response({"status":1},status=status.HTTP_201_CREATED)
                 print(serializer.validated_data)
                 print(status.HTTP_201_CREATED)
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

class ArtworkList(APIView):
     def get(self, request):
          id = request.GET.get('id')
          if id:
              id=int(id)
              artwork = Artwork.objects.filter(id=id).exists()
              if artwork:
                   artwork = Artwork.objects.filter(id=id).values()
                   return Response({'artwork': artwork})
              else :return Response({'error': "Artwork not found"})

          artworks = Artwork.objects.filter().values()
          return Response({'artworks': artworks})
     
class updateProfile(APIView): 
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileUpdateSerializer
    parser_classes = (MultiPartParser, FormParser)
    def post(self,request):
        serializer  = self.serializer_class(data=request.data)
        if  serializer.is_valid():
             user=request.user
             email = serializer.validated_data['email']
             name = serializer.validated_data['name']
             bio = serializer.validated_data['bio']
             try:
                if(name):user.name=name
                user.save()
             except Exception as e:pass
             try:
                if bio:user.bio=bio
                user.save()
             except Exception as e:pass
             try:
                if email:
                    if email==user.email:pass
                    else:
                        if not Artist.objects.filter(email=email).exists():
                                user.email=email
                                user.save()
             except Exception as e:pass
             return Response({"status":1},status=status.HTTP_200_OK)
        else:return Response(serializer.errors)
             







@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Artworks(request):
    public_works = Artwork.objects.filter(is_public=True)
    user_works = request.user.artworks.all()
    artworks = public_works | user_works
    serializer = ArtworkSerializer(artworks, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def ArtworkDetail(request, pk):
    artworks = Artwork.objects.get(id=pk)
    serializer = ArtworkSerializer(artworks, many=False)
    return Response(serializer.data)

class createArtwork(APIView):
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ArtworkSerializer
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status":1})
            except Exception as e:
                 return Response("Error ",status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors)


class updateArtwork(APIView):
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ArtworkSerializer
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
          try:
             id = request.GET.get('id')
             if id:
                 id=int(id)
                 if Artworks.objects.filter(id=id).exists():
                         artwork = Artworks.objects.get(id=id)
                         if artwork.user == request.user:
                              serializer = self.serializer_class(data=request.data)
                              if serializer.is_valid():
                                   title  = serializer.validated_data['title']       
                                   description  = serializer.validated_data['description']         
                                   artwork.title=title
                                   artwork.description=description
                                   artwork.save()
                                   return Response({"status":1})
                              return Response(serializer.errors)
                    
          except Exception as e:return Response("Error",status=status.HTTP_406_NOT_ACCEPTABLE)
          return Response("Error",status=status.HTTP_406_NOT_ACCEPTABLE)




class deleteArtwork(APIView):
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
          id = request.GET.get('id')
          if id:
            id=int(id)
            if Artworks.objects.filter(id=id).exists():
                artwork = Artworks.objects.get(id=id)
                if artwork.user == request.user:
                    artwork.delete()
                    return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
                        
