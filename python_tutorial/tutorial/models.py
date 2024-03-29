from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class RoomInfo(models.Model):
	name = models.CharField(max_length = 250, default = None)
	total_seats = models.IntegerField()
	location = models.CharField(max_length = 250)
	projector_status = models.BooleanField(default = True)
	comm_status = models.BooleanField(default = True)
	def __str__(self):
		return self.name

class Bookings(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
	room_name = models.ForeignKey(RoomInfo, on_delete = models.CASCADE)
	start_time = models.DateTimeField(auto_now = False, auto_now_add = False)
	end_time = models.DateTimeField(auto_now = False, auto_now_add = False)
