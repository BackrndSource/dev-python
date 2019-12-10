from django.db import models

class Setting(models.Model):
	name = models.CharField(max_length=100)
	value = models.CharField(max_length=500)

	def __str__(self):
		return self.name + ' : ' + self.value
	

class Post(models.Model):
	POST_TYPE = (
		(0, 'Movie'),
		(1, 'Serie'),
	)
	type = models.IntegerField(default=0, choices=POST_TYPE)
	tmdb_id = models.IntegerField(default=0)

	def __str__(self):
		return str(self.tmdb_id)
