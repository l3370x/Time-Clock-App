from timeregistry.models import TimeReg
from django.contrib import admin

class TimeAdmin(admin.ModelAdmin):
  readonly_fields = ('emp','creation','modified')

admin.site.register(TimeReg, TimeAdmin)