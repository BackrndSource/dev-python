from django.contrib import admin
from .models import *

admin.site.register(Link)
admin.site.register(LinkType)
admin.site.register(LinkLang)
admin.site.register(LinkSubtitle)
admin.site.register(LinkVideoQuality)
admin.site.register(LinkAudioQuality)
admin.site.register(LinkLike)
admin.site.register(LinkReport)
admin.site.register(LinkReportType)