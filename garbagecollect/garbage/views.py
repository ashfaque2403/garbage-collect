from datetime import datetime
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.urls import reverse
from django.views import View
from .models import Customer,Complaint,CompanyAdministrator,CustomUser, Driver,GarbageCollector,ReplyComplaint,PaymentReport,GarbageCollectedReport
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def AddComplaint(request):
    if request.method == "POST":
        # customer, created = Customer.objects.get_or_create(user=request.user)
        user=request.user
        name=request.POST.get('name')
        complaint=request.POST.get('subject')
        garbage_area=request.POST.get('area')
        date_str=request.POST.get('date')

        starting = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = datetime.now().date()

        if starting < today:
            messages.success(request, 'wrong Credentials')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        create=Complaint.objects.create(user=user,customer_name=name,complaint_text=complaint,garbage_collection_area=garbage_area,complaint_date=date_str)
        messages.success(request,'Thank you for valuable feedback')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    return render(request,'add_complaint.html')


@login_required
def RemoveAdmin(request):
    remove_admin=CompanyAdministrator.objects.all()
    
    context={
        'remove_admin':remove_admin,
    }
    return render(request, 'remove_admin.html',context)


@login_required
def delete_data(request, id):
    company_admin_instance = get_object_or_404(CompanyAdministrator, id=id)

    # Fetch the associated CustomUser instance
    user_instance = company_admin_instance.user

    # Perform the delete operation on both instances
    company_admin_instance.delete()
    user_instance.delete()

    return redirect('remove-admin')

@login_required
def DriverList(request):
    driver_list=Driver.objects.all()
    context={
        'driver_list':driver_list,
    }
    return render(request,'driver_list.html',context)


@login_required
def RemoveDriver(request,id):
    remove_driver=get_object_or_404(Driver,id=id)
    user_instance=remove_driver.user
    
    remove_driver.delete()
    user_instance.delete()
    
    return redirect('driver-list')


@login_required
def CollectorList(request):
    collector_list=GarbageCollector.objects.all()
    
    context={
        'collector_list':collector_list,
    }
    return render(request,'garbage_collector_list.html',context)


@login_required
def RemoveCollectorList(request,id):
    remove_driver=get_object_or_404(GarbageCollector,id=id)
    user_instance=remove_driver.user
    
    remove_driver.delete()
    user_instance.delete()
    
    return redirect('garbage-collector')


@login_required
def ViewComplaint(request):
    complaint=Complaint.objects.all()
    
    context={
        'complaint':complaint,
    }
    return render(request, 'view_complaint.html',context)


@login_required
def AddGarbageCollector(request):
    return render(request, 'garbage_collector.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect(index)




def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = CustomUser.objects.filter(username=username).first()

        if not user_obj:
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_authenticated = authenticate(request, username=username, password=password)

        if not user_authenticated:
            messages.warning(request, 'Invalid password')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        print(f"Authenticated User: {user_authenticated}")

        login(request, user_authenticated)
        return redirect('/')

    return render(request, 'login.html')



def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the provided email already exists
        user_exists = CustomUser.objects.filter(email=email).exists()

        if user_exists:
            messages.warning(request, 'User with this email already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Create a new CustomUser
        user = CustomUser.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        # Redirect to the login page
        return redirect('login')

    # If the request method is not POST, render the registration page
    return render(request, 'register.html')


@login_required
def CompleteCustomerProfile(request):
    
    if request.method == 'POST':
        user=request.user
        name=request.POST.get('name')
        email=request.POST.get('email')
        address=request.POST.get('address')
        garbage_collection_area=request.POST.get('area')
        
        customerprofile=Customer.objects.create(user=user,customer_name=name,email=email,address=address,garbage_collection_area=garbage_collection_area)
        return redirect('/')
    return render(request,'complete_customer_profile.html')    


@login_required
def adddriver(request):

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        # phone = request.POST.get('phone')
        # address = request.POST.get('address')
        garbage_collection_area = request.POST.get('garbage_collection_area')
        vehicle_name = request.POST.get('vehicle_name')
        password = request.POST.get('password')

        if CustomUser.objects.filter(username=name).exists():
            messages.warning(request, 'Already Exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            # Create a CustomUser instance
            user_ob = CustomUser.objects.create_user(username=name,email=email, password=password,is_driver=True)

            # Create a Driver instance associated with the CustomUser
            driver = Driver.objects.create(
                user=user_ob,
                driver_name=name,
                email=email,
                garbage_collection_area=garbage_collection_area,
                vehicle_name=vehicle_name,
                password=password
            )
            messages.success(request,'Success')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            

    return render(request, 'add_driver.html')


@login_required
def thanks(request):
    return render(request, 'thanks.html')



@login_required
def addgarbagecollector(request):
    if request.method == "POST":
        name=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        address=request.POST.get('address')
        garbage_collection_area=request.POST.get('area')
        
        if CustomUser.objects.filter(username=name).exists():
            messages.warning(request, 'Already Exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        else:
            user_obj=CustomUser.objects.create_user(username=name,email=email,password=password,is_garbagecollector=True)
            
            garbagecollector=GarbageCollector.objects.create(user=user_obj,collector_name=name,email=email,password=password,address=address,garbage_collection_area=garbage_collection_area)
            messages.success(request,'Success')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    return render(request, 'garbage_collector.html')


@login_required
def AddCompanyAdmin(request):
    if request.method == 'POST':
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        dob_str=request.POST.get('dob')
        district=request.POST.get('district')
        gender=request.POST.get('gender')
        p_address=request.POST.get('address')

        starting = datetime.strptime(dob_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        if starting >= today:
            messages.warning(request, 'Check your DOB')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if CustomUser.objects.filter(username=first_name).exists():
            messages.warning(request, 'Already Exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            user_obj = CustomUser.objects.create_user(username=first_name, email=email, is_companyadmin=True)
            user_obj.set_password(password)
            user_obj.save()

        # Create CompanyAdministrator
            admin_created = CompanyAdministrator.objects.create(
                user=user_obj,
                firstname=first_name,
                lastname=last_name,
                email=email,
                password=user_obj.password,  # Store the hashed password
                dob=dob_str,
                district=district,
                gender=gender,
                permanent_address=p_address
            )

            messages.success(request, 'Company Admin Created Successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        
    return render(request,'add_company_admin.html')


@login_required
def ViewReplyComplaint(request):
    reply_complaint = ReplyComplaint.objects.filter(user=request.user)
    context = {
        'reply_complaint': reply_complaint,
    }
    return render(request, 'view_reply_complaint.html', context)


@login_required
def reply_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == "POST":
        user = request.user
        name = request.POST.get('name')
        reply_text = request.POST.get('reply_complaint')
        reply_date_str = request.POST.get('reply_date')

        starting = datetime.strptime(reply_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()

        if starting < today:
            messages.warning(request, 'Wrong Credential')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        reply = ReplyComplaint.objects.create(original_complaint =complaint, user=user, name=name, reply_complaint=reply_text, reply_date=reply_date_str)
        return HttpResponseRedirect(reverse('view-reply-complaint'))  # Adjust the URL name accordingly

    return render(request, 'reply_complaint.html', {'complaint': complaint})

@login_required
def PaymentReportCreateView(request):
    if request.method == "POST":
        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        garbage_area = request.POST.get('area')
        amount = request.POST.get('amount')
        collector_name = request.POST.get('collector')

        name_check = Customer.objects.filter(customer_name=name).first()
        collector_check = GarbageCollector.objects.filter(collector_name=collector_name).first()

        if name_check and collector_check:
            payment = PaymentReport.objects.create(collector=collector_check, user=user, customer=name_check, email=email, garbage_collection_area=garbage_area, amount=amount)
            messages.success(request, 'Payment Success')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'User or Collector not found')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'payment_report_form.html')


@login_required
def CustomerDetails(request):
    view_customer=Customer.objects.all()
    
    context={
        'view_customer':view_customer
    }
    return render(request,'customer_details.html',context)


@login_required
def GarbageReport(request):
    if request.method == 'POST':
        user = request.user
        customer_name_report = request.POST.get('name')
        driver_name_report = request.POST.get('driver_name')
        collector_name_report = request.POST.get('collector_name')
        garbage_area = request.POST.get('area')
        date_str = request.POST.get('date')
        
        starting = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = datetime.now().date()

        if starting < today:
            messages.warning(request, 'Wrong Credential')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Check if the objects exist
        customer_name_report_check = Customer.objects.filter(customer_name=customer_name_report).first()
        driver_name_report_check = Driver.objects.filter(driver_name=driver_name_report).first()
        collector_name_report_check = GarbageCollector.objects.filter(collector_name=collector_name_report).first()
        
        if customer_name_report_check and driver_name_report_check and collector_name_report_check:
            # Create GarbageCollectedReport
            garbage_created = GarbageCollectedReport.objects.create(
                user=user,
                customer=customer_name_report_check,
                driver=driver_name_report_check,
                collector=collector_name_report_check,
                garbage_collection_area=garbage_area,
                date=date_str
            )
            messages.success(request, 'Garbage collecting completed')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            # Handle case when one or more objects are not found
            messages.error(request, 'Invalid Customer, Driver, or Collector')
    
    return render(request, 'garbage_report.html')


@login_required
def ViewPayment(request):
    view_payment=PaymentReport.objects.all()
    
    if request.user:
        view_payment_report = PaymentReport.objects.filter(user=request.user)
    
    
    context={
        'view_payment':view_payment,
        'view_payment_report':view_payment_report,
        
    }
    return render(request,'payment_view.html',context)


@login_required
def CustomerViewPayment(request):
    view_payment_report = PaymentReport.objects.filter(user=request.user)
    context={
       
        'view_payment_report':view_payment_report,
        
    }
    return render(request,'payment_view.html',context)



@login_required
def ViewGarbage(request):
    
    view_garbage=GarbageCollectedReport.objects.all()
    
    context={
        'view_garbage':view_garbage,
    }
    return render(request,'garbage_view.html',context)