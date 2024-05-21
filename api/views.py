from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Artist, Artwork
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer, ArtworkSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = Artist.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Profile(request):
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)

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
    public_works = Artwork.objects.filter(is_public=True).order_by('-updated')[:10]
    user_works = request.user.artworks.all().order_by('-updated')[:10]
    artworks = public_works | user_works
    serializer = ArtworkSerializer(artworks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ArtworkList(request):
    artworks = Artwork.objects.all().order_by('-updated')
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

