from django.db import models
from django.contrib.auth.models import User

class Movies(models.Model):
    CATEGORY = (
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('Comedy', 'Comedy'),
        ('Crime', 'Crime'),
        ('Drama', 'Drama'),
        ('Fantasy', 'Fantasy'),
        ('Horror', 'Horror'),
        ('Mystery', 'Mystery'),
        ('Romance', 'Romance'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Thriller', 'Thriller')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    genre = models.CharField(max_length=50, choices=CATEGORY)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title