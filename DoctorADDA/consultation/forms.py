from django import forms
from django.forms import ModelForm
from consultation.models import Patient,Doctor,Slot
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

class DoctorRegister(forms.Form):
    username=forms.CharField(max_length="20")
    first_name=forms.CharField(max_length="20")
    last_name=forms.CharField(max_length="20")
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    repassword=forms.CharField(widget=forms.PasswordInput)
    Day_Types=(
        ("Mon-Thu","MON-THU"),
        ("Mon-Fri","MON-FRI"),
        ("Mon-Sat","MON-SAT"),
        )
    Hour_Types=(
        ("10-12 & 5-7","10-12 AND 5-7"),
        ("10-12 & 6-9","10-12 AND 6-9"),
        ("10-12 & 5-8","10-12 AND 5-8"),
        )    
    availability=forms.ChoiceField(widget=RadioSelect, choices=Day_Types)
    consultation=forms.ChoiceField(widget=RadioSelect, choices=Hour_Types)
    speciality=forms.CharField(max_length="30")
    address=forms.CharField(max_length="100")
    def clean(self):
    	form_data = self.cleaned_data
    	if form_data['password'] != form_data['repassword']:
        	self._errors["password"] = "Password do not match"
        	del form_data['password']
    	return form_data		


class PatientRegister(forms.Form):
    username=forms.CharField(max_length="20")
    first_name=forms.CharField(max_length="20")
    last_name=forms.CharField(max_length="20")
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    repassword=forms.CharField(widget=forms.PasswordInput)
    contact=forms.IntegerField()
    def clean(self):
    	form_data = self.cleaned_data
    	if form_data['password'] != form_data['repassword']:
        	self._errors['password'] = "Password do not match"
        	del form_data['password']
    	return form_data		

class SlotBook(ModelForm):
    class Meta:
        model=Slot
        exclude=('user','doctor')


class LoginForm(forms.Form):
    username=forms.CharField(max_length="20")
    password=forms.CharField(widget=forms.PasswordInput)
    
    
class Voting(forms.Form):
	Voting_Types=(
				("voteup","voteup"),
				("votedown","votedown"),
				)
	vote=forms.ChoiceField(widget=forms.RadioSelect, choices=Voting_Types) 
	
	
class Failure(forms.Form):
	username=forms.CharField(max_length="20")
	
class ResetForm(forms.Form):
	username=forms.CharField(max_length="20")
	password=forms.CharField(widget=forms.PasswordInput)
	repassword=forms.CharField(widget=forms.PasswordInput)
	def clean(self):
		form_data = self.cleaned_data
		if form_data['password']!=form_data['repassword']:
			self._errors['password']="Password do not match"
			del form_data['password']
		return form_data	
	
class ChangePassword(forms.Form):
	password=forms.CharField(widget=forms.PasswordInput)






