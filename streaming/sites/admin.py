from django.contrib import admin
from .models import *

admin.site.register(Site)
admin.site.register(SiteLike)
admin.site.register(SiteReport)
admin.site.register(SiteReportType)
