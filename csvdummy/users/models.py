from django.db import models

class Users(models.Model):
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=20)

	def __str__(self):
		return self.username
	
	class Meta:
		verbose_name = 'User'
		verbose_name_plural = 'Users'