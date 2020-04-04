from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profilePic = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.user.username
    


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titulo")
    description = models.CharField(max_length=200, verbose_name="Descripcion")
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.title
    

class Topic(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titulo")
    description = models.TextField(verbose_name="Descripcion")
    fixed = models.BooleanField(default=False, verbose_name="Fijado")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if(self.user.groups.filter(name='Moderador') or self.user.is_staff):
            self.fixed = self.fixed
        else:
            self.fixed = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Tema"
        verbose_name_plural = "Temas"

    def __str__(self):
        return self.title
    
class ResponseTopic(models.Model):
    myResponse = models.TextField(verbose_name="Respuesta")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"

    def __str__(self):
        return self.topic
    


class ResponseToResponse(models.Model):
    parentResponse = models.ForeignKey(ResponseTopic, on_delete=models.CASCADE)
    textResponse = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)


# Signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()