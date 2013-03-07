# Create your views here.
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from consultation.forms import DoctorRegister,PatientRegister,SlotBook,LoginForm,Voting,Failure,ResetForm,ChangePassword
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from consultation.models import Doctor,Patient,Slot,UserProfile,Vote
from django.db.models import Avg
from django.core.mail import send_mail



#***********************************************          *************************************************************
#**********************************************For common*************************************************************# 
#**********************************************          **************************************************************



def index(request): #For home page
    return render_to_response('home.html',locals())


def log_user(request): #For user login 
    if request.method=="POST":
        form=LoginForm(request.POST)
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_staff:
            	return HttpResponseRedirect('/doctoradda/admin/')
            else:
            	request_user=UserProfile.objects.get(profile=user)           
            	if request_user.user_type=="doctor":
                	return render_to_response('app/doctor_data.html',locals())
            
                else:
            		return HttpResponseRedirect('/doctoradda/doctor/')
        else:
            state="Username AND/OR Password is incorrect"
            login_form=form
            extra="Forgot Password"
            return render_to_response('app/login.html',locals())
    else:
        form=LoginForm()
        state="Already Registered Please"
        return render_to_response('app/login.html',locals())

	
def logout_user(request): #For user Logout
    logout(request)
    return render_to_response('home.html',locals())



def login_failure(request):
	if request.method=="POST":
		form=Failure(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			print username
			user=User.objects.get(username=username)
			print user
			if user is not None:
				link="http://127.0.0.1:8000/doctoradda/reset/"
				send_mail("RESET PASSWORD",link,"sanatan.nayak90@gmail.com",[user.email])
				return HttpResponseRedirect('/doctoradda/login/')
			else:
				return render_to_response('home.html',locals())
		else:
			reg_form=form
			return render_to_response('app/password.html',locals())
	else:
		form=Failure()
		state="Please enter Username"
		return render_to_response('app/password.html',locals())
			



def reset_password(request):
	if request.method=="POST":
		form=ResetForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			user=User.objects.get(username=username)
			print user
			user.set_password(str(form.cleaned_data['password']))
			user.save()
			return HttpResponseRedirect('/doctoradda/login/')
		else:
			reg_form=form
			return render_to_response('app/password.html',locals())
	else:
		form=ResetForm()
		state="Please enter your new password"
		return render_to_response('app/password.html',locals())
		

def change_password(request):
	if request.method=="POST":
		form=ChangePassword(request.POST)
		if form.is_valid():
			register_user=User.objects.get(username=request.user.username)
			register_user.set_password(str(form.cleaned_data['password']))
			register_user.save()
			return HttpResponseRedirect('/doctoradda/login/')
		else:
			state="please enter a new password"
			return render_to_response('app/reset.html',locals())
	else:
		form=ChangePassword()
		state="Enter a New Password"
		return render_to_response('app/reset.html',locals())





##################################################               #################################################
##################################################For Doctor User#################################################
##################################################               #################################################



def register_doctor(request): # for doctor Registration
    if request.method=="POST":
        form=DoctorRegister(request.POST)
        if form.is_valid():
            user=User.objects.create(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    #password=form.cleaned_data['password'],
                    )
            user.set_password(str(form.cleaned_data['password']))
            user.save()
            doctor=Doctor.objects.create(
                    user=user,
                    speciality=form.cleaned_data['speciality'],
                    availability=form.cleaned_data['availability'],
                    consult_hour=form.cleaned_data['consultation'],
                    address=form.cleaned_data['address'],
                    )
            doctor.save()
            current_user=UserProfile.objects.create(
                    profile=user,
                    user_type="doctor",
                    )
            current_user.save()
            send_mail('Registration-Acknowledgement','Thanks Doctor for Registration','sanatan.nayak90@gmail.com',[user.email])
            return HttpResponseRedirect('/doctoradda/login/')
        else:
            state="Please fill the form correctly"
            reg_form=form
            return render_to_response('app/register.html',locals())
    else:
        state="Doctor fill the form to register"
        form=DoctorRegister()
        return render_to_response('app/register.html',locals())


def user_details(request):
    doc_obj=Doctor.objects.get(user=request.user)
    form=Slot.objects.filter(doctor = doc_obj)
    return render_to_response('app/user.html',locals())



def user_description(request,c_id):
    patient=Patient.objects.get(user=User.objects.get(id=c_id))
    return render_to_response('app/userdesc.html',locals())



#################################################           #########################################################
#################################################For Patient#########################################################
#################################################           #########################################################




def register_patient(request): # For patient registration
    if request.method=="POST":
        form=PatientRegister(request.POST)
        if form.is_valid():
            user=User.objects.create(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    #password=form.cleaned_data['password'],
                    )
            user.set_password(str(form.cleaned_data['password']))
            user.save()
            patient=Patient.objects.create(
                    user=user,
                    contact_no=form.cleaned_data['contact'],
                    )
            patient.save()
            current_user=UserProfile.objects.create(
                    profile=user,
                    user_type="patient",
                    )
            current_user.save()
            send_mail('Registration-Acknowledgement','Thanks for Registration','sanatan.nayak90@gmail.com',[patient.user.email])
            return HttpResponseRedirect('/doctoradda/login/')
        else:
            reg_form=form
            return render_to_response('app/register.html',locals())
    else:
        state="Patient fill the form to Register"
        form=PatientRegister()
        return render_to_response('app/register.html',locals())



def slot_book(request, d_id): #For booking a slot
    if request.method=="POST":
        book_form=SlotBook(request.POST)
        if book_form.is_valid():
            slot=Slot.objects.create(
                    user=request.user,
                    doctor=Doctor.objects.get(id=d_id),
                    day=book_form.cleaned_data['day'],
                    hour=book_form.cleaned_data['hour'],
                    )
            slot.save()
            return HttpResponseRedirect('/doctoradda/thanks/')
        else:
            form=book_form
            return render_to_response('app/slotbook.html',locals())
    else:
        form=SlotBook()
        return render_to_response('app/slotbook.html',locals())




def doctor_details(request): #For All Doctor Details
    form=Doctor.objects.all()
    return render_to_response('app/doctor.html',locals())


def show_details(request,u_id): # For 
    form=Doctor.objects.get(id=u_id)
    print form.availability
    return render_to_response('app/doctor_details.html',locals())



def vote_user(request):
	if request.method=="POST":
		form=Voting(request.POST)
		if form.is_valid():
			form.vote=form.cleaned_data['vote']
			if form.vote=="voteup":
				register_vote=Vote.objects.create(
						user=request.user,
						)
				register_vote.vote=register_vote.vote + 1
				register_vote.save()
			else:
				register_vote=Vote.objects.create(
						user=request.user,
						)
				register_vote.vote=register_vote.vote 
				register_vote.save()
			
			rating=Vote.objects.all().aggregate(Avg('vote'))
			return render_to_response('app/thanks.html',locals())
		else:
			rform=form
			return render_to_response('app/vote.html',locals())
	else:
		form=Voting()
		return render_to_response('app/vote.html',locals())




def thanks(request):
    return render_to_response('app/doctor.html',locals())



#########################################################         ###########################################################
#########################################################For Admin###########################################################
#########################################################         ###########################################################



def admin_details(request):
	return render_to_response('home1.html',locals())


def all_doctor(request):
	form=Doctor.objects.all()
	return render_to_response('home1.html',locals())


def all_patient(request):
	form=Patient.objects.all()
	return render_to_response('home1.html',locals())
	
	
def single_detail(request,s_id):
	form=User.objects.get(id = s_id)
	return render_to_response('app/single.html',locals())
	
def delete_user(request,g_id):
	print "sanatan"
	User.objects.get(id=g_id).delete()
	return render_to_response('home1.html',locals())
	


