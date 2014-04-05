from django.db import models
from django import forms
from django.contrib.auth.models import User
from localflavor.us.forms import USPhoneNumberField
# Create your models here.
class Emp(models.Model):
  def __unicode__(self):
    return self.first_name
  def name(self):
      return self.first_name + ' ' + self.last_name
  user = models.ForeignKey(User, editable = False)
  first_name = models.CharField(max_length = 50)
  last_name = models.CharField(max_length = 50)
  phone = models.CharField(max_length=20)
  clockedin = models.BooleanField(default = False)
  email = models.EmailField()

class EmpForm(forms.ModelForm):
  class Meta:
    model = Emp
    
class UserForm(forms.Form):
  username = forms.CharField(max_length = 100)
  first_name = forms.CharField(max_length = 50)
  last_name = forms.CharField(max_length = 50)
  email = forms.EmailField(max_length = 100)
  phone = USPhoneNumberField()
  password = forms.CharField(widget = forms.PasswordInput(render_value = False), max_length = 100)
  confirm = forms.CharField(widget = forms.PasswordInput(render_value = False), max_length = 100)
    
class StudentChangePasswordForm(forms.Form):
    password = forms.CharField(widget = forms.PasswordInput(render_value = True), max_length = 100)