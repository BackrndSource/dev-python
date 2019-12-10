from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from main.models import Post


class LinkType(models.Model):
	value = models.CharField(max_length=200)

	def __str__(self):
		return self.value


class LinkLang(models.Model):
	value = models.CharField(max_length=200)

	def __str__(self):
		return self.value


class LinkSubtitle(models.Model):
	value = models.CharField(max_length=200)

	def __str__(self):
		return self.value


class LinkVideoQuality(models.Model):
	value = models.CharField(max_length=200)

	def __str__(self):
		return self.value


class LinkAudioQuality(models.Model):
	value = models.CharField(max_length=200)

	def __str__(self):
		return self.value


class Link(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	season = models.IntegerField(default=-1)
	episode = models.IntegerField(default=-1)
	type = models.ForeignKey(LinkType, on_delete=models.CASCADE)
	url = models.CharField(max_length=200)
	lang = models.ForeignKey(LinkLang, on_delete=models.CASCADE)
	subtitles = models.ForeignKey(LinkSubtitle, on_delete=models.CASCADE)
	video_quality = models.ForeignKey(LinkVideoQuality, on_delete=models.CASCADE)
	audio_quality = models.ForeignKey(LinkAudioQuality, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.url 

	def clean(self):
		if self.post.type == 0:
			self.season = -1
			self.episode = -1
		if self.post.type == 1 and (self.season < 0 or self.episode < 0):
			raise ValidationError('Specify a positive value for season and episode')


class LinkLike(models.Model):
	link = models.ForeignKey(Link, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.link.url + ' (' + self.user.username + ') [' + str(self.link.tmdb_id) + ']'


class LinkReportType(models.Model):
	description = models.CharField(max_length=200)

	def __str__(self):
		return self.description


class LinkReport(models.Model):
	link = models.ForeignKey(Link, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	#type = models.IntegerField(default=0, choices=REPORT_TYPE)
	type = models.ForeignKey(LinkReportType, on_delete=models.CASCADE)

	def __str__(self):
		return self.type + ' ' + self.link.url + ' (' + self.user.username + ')'

'''
REPORT_TYPE = (
	(1, 'Link not working (file deleted)'),
	(2, 'Link is false or scam'),
	(3, 'Link infected with virus'),
	(4, 'Too much publicity'),
)
'''