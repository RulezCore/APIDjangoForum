from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
import sys

# Create your models here.
class Profile(models.Model):
    # Validators
    def validate_img_size(value):
        filesize = value.size
        
        if filesize > 2*1024*1024:
            raise ValidationError('Tamaño maximo de imagen de 2MB')
        else:
            return value
    
    # Campos de base de datos
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profilePic = models.ImageField(upload_to='profile_pics', validators=[validate_img_size], blank=True, null=True)

    def compressImage(self, profilePic):
        imageTemproary = Image.open(profilePic)
        outputIoStream = BytesIO()
        # imageTemproaryResized = imageTemproary.resize(500,500)
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        profilePic = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % profilePic.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        print("Imagen comprimida")
        return profilePic


    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return '#'


    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.profilePic = self.compressImage(self.profilePic)
        super(Profile, self).save(*args, **kwargs)

    
# Signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()