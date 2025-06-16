
from django.contrib import admin
from django.urls import path
from hospital.views import *

urlpatterns = [
    path('',Index,name='home'),
    path('admin/', admin.site.urls),
    path('about/', About,name='about'),
    path('admin_login/', Login,name='login'),
    path('logout/', Logout_admin,name='logout'),
    path('contact/', Contact,name='contact'),
    path('view_doctor/', View_Doctor,name='view_doctor'),
    path('add_doctor/', Add_Doctor,name='add_doctor'),
    path('delete_doctor/<int:did>/', Delete_Doctor, name='delete_doctor'),
    path('add_patient/', Add_Patient, name='add_patient'),
    path('view_patient/', View_Patient, name='view_patient'),
    path('delete_patient/<int:pid>/', Delete_Patient, name='delete_patient'),
    path('add_appointment/', Add_Appointment, name='add_appointment'),
    path('view_appointment/', View_Appointment, name='view_appointment'),
    path('delete_appointment/<int:aid>/', Delete_Appointment, name='delete_appointment'),
    path('hospital_overview/', hospital_overview, name='hospital_overview'),
    path('doctor-details/', doctor_details, name='doctor_details'),
    path('feedback/', feedback_page, name='feedback'),
    path('feedback_list/', feedback_list, name='feedback_list'),
    path('view_nurse/', view_nurse, name='view_nurse'),
    path('add_nurse/', add_nurse, name='add_nurse'),
    path('view_staff/', view_staff, name='view_staff'),
    path('add_staff/', add_staff, name='add_staff'),
    path('delete_staff/<int:staff_id>/', delete_staff, name='delete_staff'),
    path('delete_nurse/<int:nurse_id>/', delete_nurse, name='delete_nurse'),
    path('bills/', view_bills, name='view_bills'),  
    path('generate_bill/<int:patient_id>/', generate_bill, name='generate_bill'),
    path('select_patient/', select_patient_for_bill, name='select_patient_for_bill'), 
    path('bill_details/<int:bill_id>/', bill_details, name='bill_details'),
    path('delete_bill/<int:bill_id>/', delete_bill, name='delete_bill'),
    path('bill_invoice/<int:bill_id>/', bill_invoice, name='bill_invoice'),
    path('make_payment/<int:bill_id>/', make_payment, name='make_payment'),

]

