from django.db import models

class Setting(models.Model):
	name = models.CharField(max_length=100)
	value = models.CharField(max_length=500)

	def __str__(self):
		return self.name + ' : ' + self.value