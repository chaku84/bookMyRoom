from django.db import models

# Create your models here.
class RoomInfo(models.Model):
	total_seats = models.IntegerField()
	location = models.CharField(max_length = 250)
	projector_status = models.BooleanField(default = True)
	