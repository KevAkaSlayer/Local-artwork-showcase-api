from django.contrib import admin
from .models import Artist, Artwork
# Register your models here.

class ArtistAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio', 'profile_pic']
    
    def first_name(self, obj):
        return obj.first_name
    def last_name(self, obj):
        return obj.last_name
    

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Artwork)

