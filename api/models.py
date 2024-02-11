from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import random, string
import datetime

# Create your models here.

class User(models.Model):
    userid = models.CharField(max_length=10, unique=True, db_index=True, editable=False)
    username = models.CharField(max_length=50) 
    profile_photo = models.ImageField(upload_to="api/statics/userimages/", null=True)

    def generate_random_code():
        length = 10
        while(True):
            gen_code = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = length))
            if User.objects.filter(userid=gen_code).count() == 0:
                break
        return gen_code

    def save(self, *args, **kwargs):
        self.userid = self.generate_random_code()
        super().save(*args, **kwargs)



class Room(models.Model):
    room_code = models.CharField(max_length=6, unique=True, blank=False, db_index=True, editable=False)
    creator = models.OneToOneField(User,  on_delete=models.CASCADE)
    admins = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='admins')
    participants = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='participants')
    open_till = models.DateField(validators=[MinValueValidator(datetime.date.today), MaxValueValidator(datetime.timedelta(days=5))])
    votes_to_skip_or_pause = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)] ) #in percentage 
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def generate_random_code():
        length = 6
        while(True):
            gen_code = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = length))
            if Room.objects.filter(room_code=gen_code).count() == 0:
                break
        return gen_code

    def save(self, *args, **kwargs):
        self.room_code = self.generate_random_code()
        super().save(*args, **kwargs)


