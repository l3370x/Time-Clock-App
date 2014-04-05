from django.db import models
from employee.models import *
from datetime import datetime
# Create your models here.
class TimeReg(models.Model):
  emp = models.ForeignKey(Emp, editable = False)
  isclockin = models.BooleanField(default=False)
  creation = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField()
  timestamp = models.DateTimeField()
  
  def save(self):
    self.modified = datetime.now()
    super(TimeReg, self).save()
