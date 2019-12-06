from django.db import models
from django.contrib.auth.models import User

LINK_TYPE = (
	(0, 'Movie'),
	(1, 'Serie'),
)
LANGS = (
	('en', 'en-US'),
	('fr', 'fr-FR'),
	('es', 'es-ES'),
)
SUBTITLES = (
	('no', 'No'),
	('en', 'en-US'),
	('fr', 'fr-FR'),
	('es', 'es-ES'),
)
AUDIO_QUALITY = (
	('HQ', 'HQ'),
)
VIDEO_QUALITY = (
	('SC', 'Screener'),
	('HD', 'HDTV'),
	('H7', '720 HD'),
	('H1', '1080 HD'),
	('UH', 'ULTRA HD'),
	('4K', '4K'),
)
REPORT_TYPE = (
	(1, 'Link not working (file deleted)'),
	(2, 'Link is false or scam'),
	(3, 'Link infected with virus'),
	(4, 'Too much publicity'),
)
class Link(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	type = models.IntegerField(default=0, choices=LINK_TYPE)
	tmdb_id = models.IntegerField(default=0)
	season = models.IntegerField(default=0)
	episode = models.IntegerField(default=0)
	url = models.CharField(max_length=200)
	lang = models.CharField(max_length=2, choices=LANGS)
	subtitles = models.CharField(default='no', max_length=2, choices=SUBTITLES)
	audio_quality = models.CharField(default='HQ', max_length=2, choices=AUDIO_QUALITY)
	video_quality = models.CharField(default='HD', max_length=2, choices=VIDEO_QUALITY)

	def __str__(self):
		return self.url 


class LinkLike(models.Model):
	link = models.ForeignKey(Link, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.link.url + ' (' + self.user.username + ') [' + str(self.link.tmdb_id) + ']'


class LinkReport(models.Model):
	link = models.ForeignKey(Link, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	type=models.IntegerField(default=0, choices=REPORT_TYPE)

	def __str__(self):
		return self.type + ' ' + self.link.url + ' (' + self.user.username + ')'