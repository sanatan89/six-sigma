from django.conf.urls import url,patterns
from consultation import views

urlpatterns=patterns('',
        (r'^$',views.index),
        (r'^register_doc/',views.register_doctor),
        (r'^register_patient/',views.register_patient),
        (r'^login/',views.log_user),
        (r'^doctor/',views.doctor_details),
        (r'logout/',views.logout_user),
        (r'^admin/',views.admin_details),
        (r'view/(?P<u_id>\d+)/',views.show_details),
        (r'bookslot/(?P<d_id>\d+)/',views.slot_book),
        (r'thanks/',views.vote_user),
        (r'^user/',views.user_details),
        (r'alldoctor/',views.all_doctor),
        (r'allpatient/',views.all_patient),
        (r'^small/(?P<s_id>\d+)/',views.single_detail),
        (r'^delete/(?P<g_id>\d+)/',views.delete_user),
        (r'^forgotpassword/',views.login_failure),
        (r'^reset/',views.reset_password),
        (r'^change/',views.change_password),
        (r'^description/(?P<c_id>\d+)/',views.user_description),
        )

