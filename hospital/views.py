from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from hospital.utils import render_to_pdf
from decimal import Decimal




def About(request):
    return render(request, 'about.html')

def hospital_overview(request): 
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'hospital_overview.html')

def Index(request):
    if not request.user.is_staff:
        return redirect('login')
    
    d = Doctor.objects.count()
    p = Patient.objects.count()
    a = Appointment.objects.count()

    return render(request, 'index.html', {'d': d, 'p': p, 'a': a})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def Login(request):
    if request.user.is_authenticated:
        return redirect('hospital_overview') 

    error = "try again"

    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('hospital_overview')  
            else:
                error = "not_staff"
        else:
            error = "invalid_credentials"

    return render(request, 'login.html', {'error': error})


def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login')
    logout(request)
    return redirect('login')

def Contact(request):
    return render(request, 'contact.html')

def View_Doctor(request):
    if not request.user.is_staff:
        return redirect('login')

    doc = Doctor.objects.filter(is_active=True)  
    return render(request, 'view_doctor.html', {'doc': doc})

def View_Patient(request):
    if not request.user.is_staff:
        return redirect('login')

    patients = Patient.objects.filter(is_active=True)  
    return render(request, 'view_patient.html', {'patients': patients})

def Add_Doctor(request):
    if not request.user.is_staff:
        return redirect('login')

    error = ""

    if request.method == "POST":
        n = request.POST['name']
        m = request.POST['mobile']
        q = request.POST['qualification']
        d = request.POST['department']
        s = request.POST['special']


        if not n.lower().startswith("dr."):
            n = f"Dr. {n}"

        try:
            Doctor.objects.create(name=n, mobile=m, qualification=q, department=d, special=s)
            error = "no"
        except Exception as e:
            print(f"Error: {e}")
            error = "yes"

    return render(request, 'add_doctor.html', {'error': error})


def Add_Patient(request):
    if not request.user.is_staff:
        return redirect('login')

    error = ""
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        address = request.POST['address']
        issue = request.POST['issue']
        room_type = request.POST['room_type']
        room_number = request.POST['room_number']

        try:
            Patient.objects.create(
                name=name,
                age=age,
                gender=gender,
                mobile=mobile,
                address=address,
                issue=issue,
                room_type=room_type,
                room_number=room_number,
                is_active=True
            )
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_patient.html', locals())


def Add_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')

    doctors = Doctor.objects.filter(is_active=True)  
    patients = Patient.objects.filter(is_active=True)

    if request.method == "POST":
        doctor = Doctor.objects.get(id=request.POST['doctor'])
        patient = Patient.objects.get(id=request.POST['patient'])
        date = request.POST['date1']
        time = request.POST['time1']
        
        try:
            doctor.name = f"Dr. {doctor.name}" if not doctor.name.startswith("Dr.") else doctor.name
            Appointment.objects.create(doctor=doctor, patient=patient, date1=date, time1=time)
            return redirect('view_appointment')
        except Exception as e:
            print(f"Error: {e}")

    return render(request, 'add_appointment.html', {'doctors': doctors, 'patients': patients})

def View_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')

    appointments = Appointment.objects.all()
    return render(request, 'view_appointment.html', {'appointments': appointments})

def Delete_Appointment(request, aid):
    if not request.user.is_staff:
        return redirect('login')

    appointment = Appointment.objects.get(id=aid)
    appointment.delete()
    return redirect('view_appointment')

def Delete_Patient(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')

def Delete_Doctor(request, did):  
    if not request.user.is_staff:
        return redirect('login')
    
    doctor = Doctor.objects.get(id=did) 
    doctor.delete()
    return redirect('view_doctor')

def doctor_details(request):
    return render(request, 'doctors_details.html')

def feedback_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            Feedback.objects.create(name=name, email=email, message=message)
            messages.success(request, "Thank you for your feedback!")
            return redirect('feedback') 

    return render(request, 'feedback.html')

def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})

def view_nurse(request):
    if not request.user.is_staff:
        return redirect('login')
    nurses = Nurse.objects.all()
    return render(request, 'view_nurse.html', {'nurses': nurses})

def add_nurse(request):
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        name = request.POST['name']
        mobile = request.POST.get('mobile_number', None)
        shift = request.POST['shift']
        availability = request.POST['availability']
        Nurse.objects.create(
            name=name,
            mobile=mobile,
            shift=shift,
            availability=availability
        )
        return redirect('view_nurse')
    return render(request, 'add_nurse.html')

def view_staff(request):
    if not request.user.is_staff:
        return redirect('login')
    staffs = Staff.objects.all()
    return render(request, 'view_staff.html', {'staffs': staffs})

def add_staff(request):
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        name = request.POST['name']
        mobile = request.POST.get('mobile_number', None)
        occupation = request.POST['occupation']
        shift = request.POST['shift']
        availability = request.POST['availability']
        Staff.objects.create(
            name=name,
            mobile=mobile,
            occupation=occupation,
            shift=shift,
            availability=availability
        )
        return redirect('view_staff')
    return render(request, 'add_staff.html')

def delete_nurse(request, nurse_id):
    if not request.user.is_staff:
        return redirect('login')
    nurse = get_object_or_404(Nurse, id=nurse_id)
    nurse.delete()
    return redirect('view_nurse')

def delete_staff(request, staff_id):
    if not request.user.is_staff:
        return redirect('login')
    staff = get_object_or_404(Staff, id=staff_id)
    staff.delete()
    return redirect('view_staff')

def generate_bill(request, patient_id):
    patient = Patient.objects.get(id=patient_id)

    bill, created = Bill.objects.get_or_create(patient=patient)
    bill.medicine_charge = Decimal(request.POST.get("medicine_charge", "0") or "0")
    bill.save()

    return render(request, "generate_bills.html", {"bill": bill})

def view_bills(request):
    bills = Bill.objects.all()  # Fetch all bills
    return render(request, "view_bills.html", {"bills": bills})

def select_patient_for_bill(request):
    patients = Patient.objects.filter(is_active=True)  
    return render(request, "select_patient.html", {"patients": patients})

def bill_details(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, "bill_details.html", {"bill": bill})

def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id) 
    bill.delete()
    return redirect('view_bills')  

def bill_invoice(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    context = {'bill': bill}
    return render_to_pdf('bill_invoice.html', context)

def make_payment(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, 'make_payment.html', {'bill': bill})
