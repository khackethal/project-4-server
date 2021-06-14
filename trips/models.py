from django.db import models
# from django.db.models.fields import BooleanField

class Trip(models.Model):
    location_id = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=50)
    latitude = models.CharField(max_length=10, blank=True)
    longitude = models.CharField(max_length=10, blank=True)
    location_string = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    open_now_text = models.CharField(max_length=20, blank=True)
    image = models.CharField(max_length=250)

    liked_by = models.ManyToManyField(
        'jwt_auth.User',
        related_name='likes',
        blank=True
    )

    listed_by = models.ManyToManyField(
        'jwt_auth.User',
        related_name='lists',
        blank=True
    )

    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='created_trips',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} in {self.location_string}'


class Comment(models.Model):
    content = models.TextField(max_length=250)
    trip = models.ForeignKey(
      Trip,
      related_name='comments',
      on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
      'jwt_auth.User',
      related_name='comments',
      on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Comment {self.id} on {self.trip}'



class UserTripList(models.Model):
    list_name = models.CharField(max_length=50)
    is_public = models.BooleanField()
    trips = models.ManyToManyField(
      Trip,
      related_name='trips',
      blank=True
    )

    owner = models.ForeignKey(
    'jwt_auth.User',
    related_name='TripLists',
    on_delete=models.CASCADE
    )

    def __str__(self):
        return f'List {self.list_name} by {self.owner}'
  
