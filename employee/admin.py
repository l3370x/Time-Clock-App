from employee.models import Emp
from django.contrib import admin

class EmpAdmin(admin.ModelAdmin):
  fieldsets = [
    ('User Info', {'fields': ['user']}),
    ('first name', {'fields': ['first_name']}),
    ('last name', {'fields': ['last_name']}),
    ('email', {'fields': ['email']}),
    ('phone', {'fields': ['phone']}),
    ('currently clocked in', {'fields': ['clockedin']}),
  ]
  readonly_fields = ('user',)

admin.site.register(Emp, EmpAdmin)