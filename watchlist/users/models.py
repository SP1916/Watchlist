from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self, *args, **kwargs):
# Delete previous image of user
        try:                
            this = Profile.objects.get(id=self.id)
            if this.image != self.image and this.image != 'default.jpg':
                this.image.delete(save=False)
        except: pass

        super().save(*args, **kwargs)

# Resizing image
        if Profile.objects.get(id=self.id).image != 'default.jpg':
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

# this = previous original object of profile
# self = updated object
# save=False becz delete() calls save() function recursively

# NOTE: for unknown reasons
# super().save() must be below deleting previous pic block and above resize pic block 

