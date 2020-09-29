from django.contrib import admin
from zencheck.models import PulseCheck, News, Tweets, WellBeing

# Register your models here.
admin.site.register(PulseCheck)
admin.site.register(News)
admin.site.register(Tweets)
admin.site.register(WellBeing)
