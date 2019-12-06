from django.db import models
from django.contrib.auth.models import User
import unidecode
import re

SITE_TYPE = (
	(0, 'Both'),
	(1, 'Movies'),
	(2, 'Series'),
)
BASE_TYPE = (
	(0, '+'),
	(1, '-'),
)
LANGS = (
	('en', 'en-US'),
	('fr', 'fr-FR'),
	('es', 'es-ES'),
)
REPORT_TYPE = (
	(1, 'Site Offline'),
	(2, 'Site is false or scam'),
	(3, 'Site is redirecting to a new site'),
	(4, 'Dificult to find links inside the site. Need instructions'),
	(5, 'Domain is changed, but still working. Example: site.com to site.link'),
	(6, 'Site infected with virus'),
	(7, 'Too much publicity'),
)
# s = Site(name='VoirStreaming.fr', base_url='https://voirstreaming.com/search/%s')
# s.save()
class Site(models.Model):
	
	type=models.IntegerField(default=0, choices=SITE_TYPE)
	name=models.CharField(max_length=200)
	base_url=models.CharField(max_length=200)
	base_type=models.IntegerField(default=0, choices=BASE_TYPE)
	lang=models.CharField(default='en', max_length=2, choices=LANGS)
	description=models.CharField(default='', max_length=200)

	def __str__(self):
		return self.name

	@property
	def likes(self):
		return SiteLike.objects.filter(site=self)

	@property
	def reports(self):
		return SiteReport.objects.filter(site=self)

	def get_search_url(self, term):
		return self.base_url % re.sub('[^A-z0-9\s]','',unidecode.unidecode(term)).lower().replace('  ', ' ').replace(' ', self.get_base_type_display())


class SiteLike(models.Model):
	site = models.ForeignKey(Site, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	tmdb_id = models.IntegerField(default=0)

	def __str__(self):
		return self.site.name + ' (' + self.user.username + ') [' + str(self.tmdb_id) + ']'


class SiteReport(models.Model):
	
	site = models.ForeignKey(Site, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	tmdb_id = models.IntegerField(default=0)
	type=models.IntegerField(default=0, choices=REPORT_TYPE)

	def __str__(self):
		return self.type + ' ' + self.site.name + ' (' + self.user.username + ') [' + str(self.tmdb_id) + ']'