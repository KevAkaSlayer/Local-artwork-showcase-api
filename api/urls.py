from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('artwork-list/',views.ArtworkList.as_view(),name='artwork-list'),
    path('artwork-detail/<str:pk>/',views.ArtworkDetail,name='artwork-detail'),
    path('artwork/',views.Artworks,name='artwork'),
    path('create-artwork/',views.createArtwork.as_view(),name='create-artwork'),
    path('update-artwork/',views.updateArtwork.as_view(),name='update-artwork'),
    path('delete-artwork/',views.deleteArtwork.as_view(),name='delete-artwork'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('token/',views.MyTokenObtainPairView.as_view(),name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/',views.Profile.as_view(),name='profile'),
    path('update-profile/',views.updateProfile.as_view(),name='update-profile'),
    path('login/',views.loginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
]
