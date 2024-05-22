from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('artwork-list/',views.ArtworkList,name='artwork-list'),
    path('artwork-detail/<str:pk>/',views.ArtworkDetail,name='artwork-detail'),
    path('artwork/',views.Artworks,name='artwork'), #individual user's artworks
    path('create-artwork/',views.createArtwork,name='create-artwork'),
    path('update-artwork/<str:pk>/',views.updateArtwork,name='update-artwork'),
    path('delete-artwork/<str:pk>/',views.deleteArtwork,name='delete-artwork'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('token/',views.MyTokenObtainPairView.as_view(),name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/',views.Profile.as_view(),name='profile'),
    path('update-profile/',views.updateProfile,name='update-profile'),
    path('login/',views.loginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
]
