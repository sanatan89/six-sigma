from django.conf.urls import url,patterns
from consultation import views

urlpatterns=patterns('',
        (r'^$',views.index),
        (r'^register_doc/',views.register_doctor),
        (r'^register_patient/',views.register_patient),
        (r'^login/',views.log_user),
        (r'^doctor/',views.doctor_details),
        (r'logout/',views.logout_user),
        (r'view/(?P<u_id>\d+)/',views.show_details),
        (r'bookslot/(?P<d_id>\d+)/',views.slot_book),
        (r'thanks/',views.vote_user),
        (r'^user/',views.user_details),
        (r'^description/(?P<c_id>\d+)/',views.user_description),
        )

