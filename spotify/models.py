from django.db import models

# Create your models here.

class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=50)
    access_token = models.CharField(max_length=50)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

    def __str__(self):
        print("user: ",self.user)
        print("created at: ", self.created_at)
        print("refresh token: ", self.refresh_token)
        print("access token: ", self.access_token)
        print("expires in: ", self.expires_in)
        print("token type: ", self.token_type )