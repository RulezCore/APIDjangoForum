# Generated by Django 3.0.5 on 2020-04-05 13:38

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profilePic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics', validators=[users.models.Profile.validate_img_size]),
        ),
    ]
