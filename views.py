# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, HttpResponseRedirect
from .models import CustomUser
from django.views import View
from .models import *
from allauth import *
from django.contrib.auth import logout
import allauth
from allauth.account.views import get_adapter
from allauth.account.views import LogoutFunctionalityMixin
from django.db.models import Q, F

# from .signals import employee_activity_signal
from django.utils import timezone
from datetime import datetime, date
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import calendar
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Attendance
import calendar
from calendar import HTMLCalendar
from .forms import *
import openpyxl

# from allauth import socialaccount
from django.contrib import admin
from allauth.socialaccount.models import SocialAccount
from .models import EmailValidation

from decimal import *

# from allauth import


# from .models import Status
# Create your views here.


# def loginpage(request):
#     return render(request,'loginpage.html')
# def login(request):
#     if request.method=='POST':
#         # email = user.email
#         username = request.POST['username']
#         password = request.POST['password']
#         # email = request.POST['email']
# user = auth.authenticate(username=username,password=password)
# if user is not None:
#     auth.login(request,user)
#     return render(request,'Homepage/home.html',{'name':request.user.username})
#         else:
#             return HttpResponse("Invalid User!")
#     elif request.method=='GET':
#         return render(request, 'loginpage.html')

# def logout(request):
#     auth.logout(request)
#     return HttpResponse("Log out Successfull!")


# def registeruser(request):
#     return render(request,'registeruser/register.html')

# any_view = LogoutFunctionalityMixin()
# log_out = any_view.logout()


# def googlogout(request):
#     view = LogoutFunctionalityMixin.as_view()
#     return view(request)


@login_required
def signin(request):
    if EmailValidation.objects.filter(
        email=request.user.email, is_active=True
    ).exists():
        # user = request.user.email

        userrs = EmailValidation.objects.get(email=request.user.email)
        userr = userrs.id

        data = Regularization.objects.all()

        if data:
            for d in data:
                man = d.emp.manager
        queryreg = (
            "select * from app_Regularization where %s == %s and is_approved IS NULL"
        )
        try:
            regdata = Regularization.objects.raw(queryreg, [man, userr])
        except:
            regdata = Regularization.objects.all()
        tdate = date.today()
        reg = userrs.region.id

        query = "select * from app_AllHolidays WHERE date > %s and region_id = %s ORDER BY date limit 3"
        holidays = AllHolidays.objects.raw(query, [tdate, reg])
        null = "null"
        if Attendance.objects.filter(
            username=request.user.email, signout__isnull=True
        ).last() and (
            Attendance.objects.filter(
                username=request.user.email, signout__isnull=True
            ).last()
        ).date == (
            timezone.localtime(timezone.now()).date()
        ):
            null = "1"
        leaves = Leaves.objects.all().filter(Is_approved=None)
        leavess = leaves.select_related("Emp").filter(Emp__manager=userr)
        realcount = leavess.count()

        key = EmailValidation.objects.filter(email=request.user.email).values_list(
            "groups"
        )
        gr = [t[0] for t in key]

        user34 = CustomUser.objects.get(email=request.user.email)

        for i in gr:
            user34.groups.add(i)

        for i in range(1, 20):
            if i not in gr:
                user34.groups.remove(i)

        key = EmailValidation.objects.filter(email=request.user.email).values_list(
            "permissions"
        )
        perm = [t[0] for t in key]

        permuser = CustomUser.objects.get(email=request.user.email)
        for i in perm:
            permuser.user_permissions.add(i)

        for i in range(1, 20):
            if i not in perm:
                permuser.user_permissions.remove(i)

        le = leaves.count()
        EmailValidations = EmailValidation.objects.all()
        email = request.user.email
        user_email = EmailValidation.objects.filter(email=email).first()
        context = {
            "regdata": regdata,
            "holidays": holidays,
            "signin": null,
            "count": le,
            "leaves": list(leaves),
            "EmailValidations": EmailValidations,
            "user_email": user_email,
            "realcount": realcount,
        }

        userrs=EmailValidation.objects.filter(email=request.user.email).first()
        present_day = datetime.today()
        if present_day.day != 1:
            first_day = present_day.replace(day=1)
            empty_list = []
            if Leavebalance.objects.filter(leavetype__leavetype='Loss of pay').exists():
                while first_day <= present_day:

                    if first_day.weekday() == 5 or first_day.weekday() == 6:
                        first_day= first_day + timedelta(days=1)
                        continue

                    Holiidays = AllHolidays.objects.filter(date=first_day.date())
                    if len(Holiidays) != 0:
                        first_day=first_day + timedelta(days=1)
                        continue

                    Regularize = Regularization.objects.\
                    filter(date=F("todate")).\
                    filter(date = first_day.date())

                    if len(Regularize) != 0:
                        first_day=first_day + timedelta(days=1)
                        continue

                    Regularize2 = Regularization.objects.\
                    filter(Q(date=first_day.date()) & ~Q(todate=first_day.date()))

                    new_list = []
                    for eachday in Regularize2:
                    
                        while eachday.date <= eachday.todate:
                            new_list.append(eachday.date)
                            eachday.date=eachday.date + timedelta(days=1)

                    if first_day.date() in new_list:
                        first_day=first_day + timedelta(days=1)
                        continue

                    attend =\
                        Attendance.objects.select_related("emp")\
                        .filter(emp=userrs)\
                        .filter(date=first_day.date())
                

                    if len(attend) != 0:
                        first_day=first_day + timedelta(days=1)
                        continue

                    empty_list.append(first_day.date())
                    first_day=first_day + timedelta(days=1)

                u = Leavebalance.objects.filter(emp=userrs).filter(leavetype__leavetype="Loss of pay").first()
                
            
                if (u.leaves_taken + len(empty_list)) > u.leaves_taken:
                    u.leaves_taken = len(empty_list)
                    u.save()

        
        return render(request, "Homepage/home.html", context)

    else:
        logout(request)
        return render(request, "loginfailed.html")

def registeruser(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        cnfpassword = request.POST["cnfpassword"]

        if password == cnfpassword:
            if CustomUser.objects.filter(username=username).exists():
                return HttpResponse("Username Taken!")
            else:
                user = CustomUser.objects.create_user(
                    first_name=firstname,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email,
                )
                user.save()
                return HttpResponse("User Created Successfully!")
        else:
            return HttpResponse("Password Not Matching!")
    return render(request, "registeruser/register.html")
    # New One


def updation(request):
    alluser = CustomUser.objects.all()
    context = {
        "alluser": alluser,
    }
    return render(request, "recent/updation.html", context)


# def updateempp(request,id):
#     data = CustomUser.objects.get(id=id)
#     data.first_name == 'don1'
#     data.save()
#     return HttpResponse("Jamla bhau!")


def alteremp(request):
    data = EmailValidation.objects.all()
    context = {
        "data": data,
    }
    return render(request, "Admin/altemp.html", context)


def newupdate(request, id):
    empid = CustomUser.objects.get(id=id)
    alluser = CustomUser.objects.all()
    roles = Role.objects.all()
    context = {
        "alluser": alluser,
        "empid": empid,
        "roles": roles,
    }
    # messages.info(request, "Holiday Added!")
    return render(request, "recent/newupdate.html", context)


def createstatus(request, id):
    data = CustomUser.objects.get(id=id)
    x = request.POST["newstatus"]
    data.roles_id = x
    data.save()
    messages.info(request, "Updated!")
    return render(request, "recent/newupdate.html")


def updateppl(request, id):
    data = EmailValidation.objects.get(id=id)
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        gender = request.POST["gender"]
        jdate = request.POST["jdate"]
        region = request.POST["region"]
        manager = request.POST["manager"]
        econtact = request.POST["econtact"]
        bloodgroup = request.POST["bloodgroup"]
        username = request.POST["username"]
        dob = request.POST["dob"]
        address = request.POST["address"]
        designation = request.POST["designation"]
        hr = request.POST["hr"]
        eemail = request.POST["eemail"]
        role = request.POST["role"]
        active = request.POST.get("active")

        data.first_name = firstname
        data.last_name = lastname
        data.email = eemail
        data.contact = contact
        data.gender = gender
        data.date_joined = jdate
        data.username = username
        data.date_of_birth = dob
        data.address = address
        data.designation = designation
        data.hr = hr
        data.emergency_contact = econtact
        data.date_joined = jdate
        data.region_id = region
        data.blood_group = bloodgroup
        data.emergency_email = email
        data.is_active = active
        x = role

        if active == "on":
            data.is_active = True
        else:
            data.is_active = False
        data.save()
        if role == "1":
            g = Group.objects.get(name="Admin")
            data.groups.clear()
            data.groups.add(g)
        elif role == "2":
            g = Group.objects.get(name="HR")
            data.groups.clear()
            data.groups.add(g)
        elif role == "3":
            g = Group.objects.get(name="Manager")
            data.groups.clear()
            data.groups.add(g)
        elif role == "4":
            g = Group.objects.get(name="Employee")
            data.groups.clear()
            data.groups.add(g)
        data.save()
        messages.success(request, "Employee Updated Successfully")
        return redirect(alteremp)
        # return HttpResponse("Employee Updated Successfully!")
    regiondata = Region.objects.all()
    
    user = EmailValidation.objects.all()
    roless = Role.objects.all()
    Manager = EmailValidation.objects.filter(roles__role="Manager")
    HR = EmailValidation.objects.filter(roles__role="HR")
    groups = Group.objects.all()
    g = data.groups.all()
    p = data.permissions.all()
    context = {
        "regiondata": regiondata,
        "user": user,
        "roless": roless,
        "Manager": Manager,
        "HR": HR,
        "data": data,
        "groups": groups,
        "g": g,
        "p": p,
        "is_checked": True,
    }
    return render(request, "Admin/updateemp.html", context)


def addnewstatus(request):
    if request.method == "POST":
        x = request.POST["nstatus"]
        news = Role(role=x)
        news.save()
        return HttpResponse("Status Created Successfully")
    return render(request, "Admin/addnewstatus.html")


# Alter Employee


def addemp(request):
    user = request.user
    if request.method == "POST":
        # id = 23454
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        gender = request.POST["gender"]
        jdate = request.POST["jdate"]
        region = request.POST["region"]
        manager = request.POST["manager"]
        econtact = request.POST["econtact"]
        bloodgroup = request.POST["bloodgroup"]
        username = request.POST["username"]
        dob = request.POST["dob"]
        address = request.POST["address"]
        designation = request.POST["designation"]
        hr = request.POST["hr"]
        eemail = request.POST["eemail"]
        role = request.POST["role"]
        activ = request.POST["active"]
        permission = request.POST.getlist("permission")
    
        if activ == "on":
            active = True
        else:
            activ = False
        if EmailValidation.objects.filter(username=username, email=email).exists():
            messages.info(request, "Username/Email Taken.")
            return redirect(addemp)
        else:
            data = EmailValidation(
                first_name=firstname,
                last_name=lastname,
                email=email,
                contact=contact,
                region_id=region,
                manager=manager,
                blood_group=bloodgroup,
                emergency_contact=econtact,
                date_joined=jdate,
                username=username,
                date_of_birth=dob,
                address=address,
                designation=designation,
                hr=hr,
                emergency_email=eemail,
                is_active=active,
                roles_id=role,
            )
            data.save()
            ppp = []
            print("above is permission")
            for per in permission:
                pr = Permission.objects.get(codename=per)
                ppp.append(pr)
                print(ppp)
            data.permissions.set(ppp)
            if role == "1":
                g = Group.objects.get(name="Admin")
                data.groups.add(g)
            elif role == "2":
                g = Group.objects.get(name="HR")
                data.groups.add(g)
            elif role == "3":
                g = Group.objects.get(name="Manager")
                data.groups.add(g)
            elif role == "4":
                g = Group.objects.get(name="Employee")
                data.groups.add(g)

            keys = EmailValidation.objects.filter(email=request.user.email).values_list(
                "groups"
            )
            gr = [t[0] for t in keys]  # we will get

            user34 = CustomUser.objects.get(email=request.user.email)

            for x in gr:
                user34.groups.add(x)

            for i in range(1, 20):
                if i not in gr:
                    user34.groups.remove(i)
            messages.success(request, "Employee Created Successfully")
            return redirect(addemp)
    regiondata = Region.objects.all()
    print(regiondata)
    # user = CustomUser.objects.all()
    roless = Role.objects.all()
    Manager = EmailValidation.objects.filter(roles__role="Manager")
    HR = EmailValidation.objects.filter(roles__role="HR")
    groups = Group.objects.all()
    context = {
        "regiondata": regiondata,
        "user": user,
        "roless": roless,
        "Manager": Manager,
        "HR": HR,
        "groups": groups,
        "is_checked": True,
        # 'groups_permissions':groups_permissions,
    }
    return render(request, "Admin/addemp.html", context)


def inactive(request, id):
    data = CustomUser.objects.get(id=id)
    if data.is_active:
        data.is_active = False
    elif data.is_active == False:
        data.is_active = True
    data.save()
    messages.info(request, "Employee Status Changed!")
    return redirect(alteremp)
    # return HttpResponse("Employee Activation Status is Changed.")


# Add Holiday


def addholiday(request):
    if request.method == "POST":
        region = request.POST["region"]
        date = request.POST["date"]
        year = request.POST["year"]
        occasion = request.POST["occasion"]
        updated_by = request.user.id
        updated_on = timezone.localtime(timezone.now())
        data = AllHolidays(
            region_id=region,
            date=date,
            year=year,
            occasion=occasion,
            updated_by=updated_by,
            updated_on=updated_on,
        )
        data.save()
        messages.info(request, "Holiday Added!")
        # return HttpResponse("Holiday Added")
    regiondata = Region.objects.all()

    context = {
        "regiondata": regiondata,
    }
    return render(request, "Admin/addholiday.html", context)


def holidayview(request):
    data = AllHolidays.objects.all()
    context = {
        "data": data,
    }
    return render(request, "Admin/holidayview.html", context)


def regularization(request):
    if request.method == "POST":
        emp = request.user.email
        user_email = EmailValidation.objects.filter(email=emp).first()
        date = request.POST["date"]
        todate = request.POST["todate"]
        reason = request.POST["reason"]
        updated_by = request.user.id
        updated_on = timezone.localtime(timezone.now())
        applied_on = timezone.localtime(timezone.now())
        data = Regularization(
            emp_id=user_email.id,
            date=date,
            todate=todate,
            reason=reason,
            updated_by=updated_by,
            updated_on=updated_on,
            applied_on=applied_on,
        )
        data.save()
        messages.info(request, "Regularization Applied!")
        return redirect(regularization)
    else:
        data = Regularization.objects.all()
        context = {
            "data": data,
        }
        return render(request, "Attendance_Regularization/regularization.html", context)


# Employee Request


def employeerequest(request):
    user = request.user.email
    user_email = EmailValidation.objects.filter(email=user).first()
    user = user_email.id
    data = Regularization.objects.all()
    if data:
        for d in data:
            man = d.emp.manager
    queryreg = "select * from app_Regularization where %s == %s and is_approved IS NULL"
    leaves = Leaves.objects.all()
    specificleaves = Leaves.objects.all().filter(Is_approved=None)
    le = specificleaves.count()
    try:
        regdata = Regularization.objects.raw(queryreg, [man, user])
    except:
        regdata = Regularization.objects.all()

    email = request.user.email
    user_email = EmailValidation.objects.filter(email=email).first()
    types = Leavetype.objects.all()
    context = {
        "regdata": regdata,
        "leaves": leaves,
        "specific": le,
        "user_email": user_email,
        "types": types,
    }
    return render(request, "Manager/emprequest.html", context)


def approverequest(request, id):
    data = Regularization.objects.get(id=id)
    data.is_approved = True
    data.approved_by = request.user.id
    data.approved_on = timezone.localtime(timezone.now())
    data.updated_on = timezone.localtime(timezone.now())
    data.updated_by = request.user.id
    data.save()
    messages.info(request, "Approved")
    # send_mail(
    #     'Regularization Status',
    #     'Regualarization Request Approved',
    #     'csea539samyakbendre@gmail.com',
    #     ['samyak.bendre@amnetdigital.com'],
    #     fail_silently=False,
    # )
    return redirect(employeerequest)


def rejectrequest(request, id):
    data = Regularization.objects.get(id=id)
    data.is_approved = False
    data.updated_on = timezone.localtime(timezone.now())
    data.updated_by = request.user.id
    data.save()
    messages.info(request, "Rejected")
    return redirect(employeerequest)


def requests(request):
    user = request.user.id
    email = EmailValidation.objects.filter(email=request.user.email).first()
    user = email.id
    data = Regularization.objects.all()
    if data:
        for d in data:
            emp = d.emp_id

    queryreg = "select * from app_Regularization where %s == %s order by date"
    try:
        regdata = Regularization.objects.raw(queryreg, [emp, user])
        print(regdata)
    except:
        regdata = Regularization.objects.all()
    context = {
        "regdata": regdata,
        "email": email,
    }
    return render(request, "Attendance_Regularization/requests.html", context)


# Emp Holiday View


def empholidayview(request):
    tdate = date.today()
    data = EmailValidation.objects.get(email=request.user.email)
    reg = data.region.id
    query = (
        "select * from app_AllHolidays WHERE date > %s and region_id = %s ORDER BY date"
    )
    holidays = AllHolidays.objects.raw(query, [tdate, reg])
    context = {
        "holidays": holidays,
    }
    return render(request, "Holidays/holidays.html", context)


# Logout


def logout_view(request):
    logout(request)
    return redirect("/accounts/google/login/")


def hrempattendance(request):
    import calendar
    if request.method == "POST":
        email=str(request.POST['email'])
        month=int(request.POST['month'])
        year=int(request.POST['year'])
        data = EmailValidation.objects.all()

        cal = calendar.monthcalendar(int(year), int(month))  # Get calendar object for specified month and year 
        # Create list of weekend dates
        weekend_dates = []
        for week in cal:
            sat = week[calendar.SATURDAY]
            sun = week[calendar.SUNDAY]
            if sat != 0:
                weekend_dates.append(int(sat))
            if sun != 0:
                weekend_dates.append(int(sun))

        attend_dates = Attendance.objects.filter(username = email,date__year=year,date__month=month).values_list('date').distinct()
        holiday_list = AllHolidays.objects.filter(date__year=year,date__month=month).values_list('date')

      
        regularize234= Regularization.objects.filter(emp__email = email, date__year=year,date__month=month,is_approved=True).values_list('date','todate')
        
        two_months_list1= ((Leaves.objects.filter(Emp__email = email, Leave_date__year=year, Leave_date__month =month-1,Is_approved=True)) and (Leaves.objects.filter(Emp__email = email, To_date__year=year, To_date__month=month,Is_approved=True))).values_list('Leave_date','To_date')
        
        two_months_list2= ((Leaves.objects.filter(Emp__email = email, Leave_date__year=year, Leave_date__month =month,Is_approved=True)) and (Leaves.objects.filter(Emp__email = email, To_date__year=year, To_date__month=month+1,Is_approved=True))).values_list('Leave_date','To_date')
        
        thi_month_leave= ((Leaves.objects.filter(Emp__email = email, Leave_date__year=year, Leave_date__month =month,Is_approved=True)) and (Leaves.objects.filter(Emp__email = email, To_date__year=year, To_date__month=month,Is_approved=True))).values_list('Leave_date','To_date')


       
        fleave_list = [t[0] for t in thi_month_leave ]
        tleave_list = [t[1] for t in thi_month_leave]

        one1=[t[0] for t in two_months_list1]
        one2=[t[1] for t in two_months_list1]

        two1=[t[0] for t in two_months_list2]
        two2=[t[1] for t in two_months_list2]

        attend_list = [t[0].day for t in attend_dates]
        holiday_list = [t[0].day for t in holiday_list]

     

        regularize1=[t[0] for t in regularize234 ]
        regularize2=[t[1] for t in regularize234 ]
       

        regularize=[]
        if len(regularize1)>0:
            for i in range(len(regularize1)):
                if regularize1[i].month==regularize2[i].month:
                    if regularize1[i].day==regularize2[i].day:
                        regularize.append(regularize1[i].day)
            
                    elif(regularize1[i].day != regularize2[i].day):
                        x=regularize1[i].day
                        y=regularize2[i].day
                        z=y-x
                        
                        

                        for i in range(x,x+z+1):
                            regularize.append(i)
        

        leave=[]

        if len(fleave_list)>0:
            for i in range(len(fleave_list)):
                if fleave_list[i].month==tleave_list[i].month:
                    if fleave_list[i].day==tleave_list[i].day:
                        leave.append(fleave_list[i].day)
            
                    if(fleave_list[i].day != tleave_list[i].day):
                        x=fleave_list[i].day
                        y=tleave_list[i].day
                        z=y-x
                        

                        for i in range(x,x+z):
                            leave.append(i)
       
        dummy_dates = []
        for i in range(len(one1)):
            if one1[i].month != one2[i].month:
                    start_dt =one1[i]
                    end_dt = one2[i]

            
                
                    while start_dt <= end_dt:  
                        dummy_dates.append(start_dt)
                        start_dt +=  timedelta(days=1)
         
        for i in range(len(two1)):
            if two1[i].month != two2[i].month:
                    start_dt =two1[i]
                    end_dt = two2[i]

                
                    while start_dt <= end_dt:  
                        dummy_dates.append(start_dt)
                        start_dt +=  timedelta(days=1)
        
        for i in range(len(dummy_dates)):
            if dummy_dates[i].month==month:
                leave.append(dummy_dates[i].day)  

        
        
        
        # casual_leave=[]
        # for i in range(len(from_c_list)):
        #     if from_c_list[i]==to_c_list[i]:
        #         casual_leave.append(from_c_list[i])
            
        #     elif(from_c_list[i]!=to_c_list[i]):
        #         x=from_c_list[i]
        #         y=to_c_list[i]
        #         z=y-x+1
               
        #         for i in range(x,x+z):
        #             casual_leave.append(i)
      

        # paternity_leave=[]
        # for i in range(len(from_p_list)):
        #     if from_p_list[i]==to_p_list[i]:
        #         casual_leave=[].append(from_p_list[i])
            
        #     elif(from_p_list[i]!=to_p_list[i]):
        #         x=from_p_list[i]
        #         y=to_p_list[i]
        #         z=y-x
               
        #         for i in range(x,x+z+1):
        #             paternity_leave=[].append(i)
        


       
        count=0
        for i in range(len(leave)):
            count=count+1


        
        present=0
        print(regularize)

        for i in attend_list:
            if i != None :
                if int(i) not in holiday_list  and int(i) not in leave and  int(i) not in weekend_dates:
                    present=present+1
        for i in regularize:
            if i != None :
                if int(i) not in holiday_list  and int(i) not in leave and int(i) not in weekend_dates:
                    present=present+1

        x=int(month)
        mon=calendar.month_name[x]

        data = EmailValidation.objects.all()
        context={"present":present,"ccount":count,"month":mon,"year":year,"email":email,"c_list":leave ,"data":data}
        return render(request,"HR/attendanceinfo.html",context)
    else:
        data = EmailValidation.objects.all()
        context = {
            'data':data,
        }
        return render(request,"HR/attendanceinfo2.html",context)
    



from django.utils.html import conditional_escape as escape
now=datetime.now()


def Convert(string):
    li = list(string.split(","))
    return li

from datetime import date, timedelta

def attendance(request,year=now.year,month=now.month):
    now=datetime.now()
    year=now.year
    month=now.month
       

    if request.method=="POST":
        value1=request.POST["a"]
        
        str1 = value1
        x=Convert(str1)
        value=int(x[0])
        month=int(x[1])
        year=int(x[2])

        if value==1:
            if month < 12:
                month=month+1
            elif month ==12:
                month=1
                year=year+1
        if value==0:
            if month > 1:
                month=month-1
            elif month ==1:
                month=12
                year=year-1
    
    now=datetime.now()
    startmonth=2
    startyear=2023
    total=2025
    email=request.user.email
    region = request.user.region_id
   

    if(int(year) >= int(startyear) and int(year)+int(month)>=int(total)):
        holiday_list = AllHolidays.objects.filter(region = region,date__year=year,date__month=month).values_list('date')
        usertime = Attendance.objects.filter(username = email,date__year=year,date__month=month).values_list('date').distinct()

        thi_month_leave= ((Leaves.objects.filter(Emp__email = email, Leave_date__year=year, Leave_date__month =month,Is_approved=True)) and (Leaves.objects.filter(Emp__email = email, To_date__year=year, To_date__month=month,Is_approved=True))).values_list("Leave_date","To_date")


        regularize = Regularization.objects.filter(emp__email = email, date__year=year,date__month=month,is_approved=True).values_list('date','todate').distinct()
 
        two_months_list1= ((Leaves.objects.filter(Emp__email = email, Leave_date__year=year, Leave_date__month =month-1,Is_approved=True)) and (Leaves.objects.filter(Emp__email = email, To_date__year=year, To_date__month=month,Is_approved=True))).values_list("Leave_date","To_date")
        
        two_months_list2= ((Leaves.objects.filter(Emp__email = email, Leave_date__year=year, Leave_date__month =month,Is_approved=True)) and (Leaves.objects.filter(Emp__email = email, To_date__year=year, To_date__month=month+1,Is_approved=True))).values_list("Leave_date","To_date")
        
        
       
        fleave_list = [t[0] for t in thi_month_leave ]
        tleave_list = [t[1] for t in thi_month_leave]

        my_new_list = [t[0].day for t in usertime]
        my_holiday_list = [t[0].day for t in holiday_list]

        regularize1=[t[0] for t in regularize ]
        regularize2=[t[1] for t in regularize ]

        print(regularize1)
        print(regularize2)

       

        one1=[t[0] for t in two_months_list1]
        one2=[t[1] for t in two_months_list1]

        two1=[t[0] for t in two_months_list2]
        two2=[t[1] for t in two_months_list2]
        
       
        regularize=[]
        if len(regularize1)>0:
            for i in range(len(regularize1)):
                if regularize1[i].month==regularize2[i].month:
                    if regularize1[i].day==regularize2[i].day:
                        regularize.append(regularize1[i].day)
            
                    elif(regularize1[i].day != regularize2[i].day):
                        x=regularize1[i].day
                        y=regularize2[i].day
                        z=y-x
                        
                        

                        for i in range(x,x+z+1):
                            regularize.append(i)
        print(regularize)
        leave=[]

        if len(fleave_list)>0:
            for i in range(len(fleave_list)):
                if fleave_list[i].month==tleave_list[i].month:
                    if fleave_list[i].day==tleave_list[i].day:
                        leave.append(fleave_list[i].day)
            
                    if(fleave_list[i].day != tleave_list[i].day):
                        x=fleave_list[i].day
                        y=tleave_list[i].day
                        z=y-x
                        

                        for i in range(x,x+z+1):
                            leave.append(i)
       
        dummy_dates = []
        for i in range(len(one1)):
            if one1[i].month != one2[i].month:
                    start_dt =one1[i]
                    end_dt = one2[i]
                
                    while start_dt <= end_dt:  
                        dummy_dates.append(start_dt)
                       
                        start_dt += timedelta(days=1)
        for i in range(len(two1)):
            if two1[i].month != two2[i].month:
                    start_dt =two1[i]
                    end_dt = two2[i]
                
                    while start_dt <= end_dt:  
                        dummy_dates.append(start_dt)
                   
                        start_dt += timedelta(days=1)
        
        for i in range(len(dummy_dates)):
            if dummy_dates[i].month==month:
                leave.append(dummy_dates[i].day)   
        
        
    
        calendar = CustomHTMLCalendar(my_new_list,my_holiday_list,month,year,leave,regularize) #passing values to customehtmlcalender class
        calendar_html = calendar.formatmonth(year,month)   # displaying the data that we got from above line
        return render(request,'Attendance_Regularization/attendance.html',{"cal":calendar_html , "user":my_new_list,"year":year,"month":month})
    else:

        messages.success(request, "Since Amnet portal started from Feb- 2023, Data before that is not available")
        return render(request,'Attendance_Regularization/attendance.html',{"year":year,"month":month})





class CustomHTMLCalendar(HTMLCalendar):
    def __init__(
        self, my_new_list, my_holiday_list, month, year, leave_list, regularize
    ):
        super().__init__(firstweekday=0)
        self.attendance_list = my_new_list
        self.holiday_list = my_holiday_list
        self.month = int(month)
        self.year = int(year)
        self.leave = leave_list
        self.regularize = regularize

    def formatday(self, day, weekday):
        now = datetime.now()

        if day != 0:
            cssclass = self.cssclasses[weekday]

            if day in self.attendance_list or day in self.regularize:
                cssclass += " special-day"  # add custom CSS class to highlight the day
            elif now.month == self.month and now.year == self.year:
                if day < now.day:
                    cssclass += " absent"
            elif now.year > self.year:
                cssclass += " absent"
            elif now.year == self.year and now.month > self.month:
                cssclass += " absent"
            if day in self.leave:
                cssclass += " leave"

            if day in self.holiday_list:
                cssclass += " holiday"

            return f'<td class="{cssclass}">{escape(str(day))}</td>'
        return '<td class="noday">&nbsp;</td>'


def signinn(request):
    # try:
    user = request.user.email
    today = date.today()
    attend = Attendance.objects.all()
    attend = Attendance(
        username=user,
        date=today,
        signin=timezone.localtime(timezone.now()),
        day=today.day,
    )
    attend.save()
    messages.success(request, "Signed in")
    # return render(request,'Homepage/home.html',{"signin":1})
    return redirect(signin)


# except:
#     return render(request,"logout_sessoin_out.html")


def signoutt(request):
    try:
        username = request.user.email
        today = date.today()
        attend = Attendance.objects.filter(username=username).last()
        attend.signout = timezone.localtime(timezone.now())
        attend.save()
        messages.success(request, "Signed out")
        # return render(request,'Homepage/home.html',{"signin":null})
        return redirect(signin)
    except:
        return render(request, "logout_sessoin_out.html")


# def someleave(request):
#     form = leaveform()
#     if request.method == "POST":
#         form = leaveform(request.POST)
#         if form.is_valid():
#             form.save()
#             data = Leaves.objects.last()
#             data.Emp_id = request.user.id
#             data.save()
#             messages.success(request, "Leave is applied")
#             return redirect(someleave)
#     context = {"forms": form}
#     return render(request, "practise/form.html", context)


# def someleaverequest(request, pk):
#     data = Leaves.objects.get(id=pk)
#     forms = leaveform1(instance=data)
#     if request.method == "POST":
#         forms = leaveform1(request.POST, instance=data)
#         if forms.is_valid():
#             if data.Leave_type == "Casual":
#                 data.casual_leaves_left = data.casual_leaves_left - 1
#                 # messages.success(request,"Leave is approved")
#             else:
#                 data.paternity_leaves_left = data.paternity_leaves_left - 1
#                 # messages.success(request,"Leave is rejected")
#             forms.save()

#             return redirect(employeerequest)
#     context = {"forms": forms}
#     return render(request, "practise/form1.html", context)


def allleavereq(request):
    datas = Leaves.objects.all()
    context = {"datas": datas}
    return render(request, "practise/form2.html", context)


def admin_leave_access(request):
    search1 = EmailValidation.objects.all()
    types=Leavetype.objects.all()
    data={"search":search1,"types":types}
    
              
    return render(request, "Admin/modifyleave.html",data)


def addleave_emp(request):
    if request.method == "POST":
        email = request.POST["email"]
        leave=request.POST["Leave_type"]
        num = request.POST["number"]
        leave_balance_email=Leavebalance.objects.all()
       
        for i in leave_balance_email:
            if str(i.emp.email) == str(email) and str(i.leavetype) == str(leave):
                i.alloated= i.alloated +int(num)
                i.balance= i.balance +int(num)
                i.save()
               
                    
        # data = EmailValidation.objects.get(email=email)
        # data.Leaves = data.Leaves + int(num)
        # print(data.Leaves)
        # data.save()
        messages.success(request, "Leaves are added")
        search1 = EmailValidation.objects.all()
        types=Leavetype.objects.all()
        data={"search":search1,"types":types}
        return render(request, "Admin/modifyleave.html",data)
        # return HttpResponse("<h1>leave of an employee updated sucessfuly</h1>")
    else:
        return render(request, "Admin/modifyleave.html")


def addleave_org(request):
    if request.method == "POST":

        leave=request.POST["Leave_type"]
        num = request.POST["number"]
        leave_balance_email=Leavebalance.objects.all()
       
        for i in leave_balance_email:
            if str(i.leavetype) == str(leave):
                i.alloated= i.alloated +int(num)
                i.balance= i.balance +int(num)
                i.save()
               

        
        # data.Leaves=data.Leaves+int(num)
        # data.save()
        messages.success(request, "Leaves are added for whole oraganization")
        search1 = EmailValidation.objects.all()
        types=Leavetype.objects.all()
        data={"search":search1,"types":types}
        return render(request, "Admin/modifyleave.html",data)
        # return HttpResponse("<h1>leave of organisaiton updated sucessfuly</h1>")
    else:
        return render(request, "Admin/modifyleave.html")


# DELETING LEAVES
def deleteleave_emp(request):
    if request.method == "POST":
        email = request.POST["email"]
        leave=request.POST["Leave_type"]
        num = request.POST["number"]
        leave_balance_email=Leavebalance.objects.all()
       
        for i in leave_balance_email:
            if str(i.emp.email) == str(email) and str(i.leavetype) == str(leave):
                if i.alloated >= int(num) and i.alloated !=0 and i.balance >= int(num) and i.balance !=0 :
                    i.alloated= i.alloated -int(num)
                    i.save()
                    i.balance= i.balance - int(num)
                    i.save()
                else:
                    i.alloated= 0
                    i.balance= 0
                    i.save()
                    
        messages.success(request, "Leaves are deleted")
        search1 = EmailValidation.objects.all()
        types=Leavetype.objects.all()
        data={"search":search1,"types":types}
        return render(request, "Admin/modifyleave.html",data)
        # return HttpResponse("<h1>leave of an employee updated sucessfuly</h1>")
    else:
        return render(request, "Admin/modifyleave.html")


def deleteleave_org(request):
    if request.method == "POST":
        leave=request.POST["Leave_type"]
        num = request.POST["number"]
        leave_balance_email=Leavebalance.objects.all()
       
        for i in leave_balance_email:
            if str(i.leavetype) == str(leave):
                if i.alloated >= int(num) and i.balance >= int(num)  :
                    i.alloated= i.alloated -int(num)
                    i.balance= i.balance - int(num)
                    i.save()
                else:
                    i.alloated= 0
                    i.balance= 0
                    i.save()
        messages.success(request, "Leaves are deleted for whole organization")
        search1 = EmailValidation.objects.all()
        types=Leavetype.objects.all()
        data={"search":search1,"types":types}
        return render(request, "Admin/modifyleave.html",data)
        # return HttpResponse("<h1>leave of organisaiton updated sucessfuly</h1>")
    else:
        return render(request, "Admin/modifyleave.html")

def approveleave(request, pk):
    leave = Leaves.objects.get(id=pk)
    leave.Is_approved = True
    us = EmailValidation.objects.get(id=leave.Emp.id)
    types = Leavetype.objects.all()

    if leave.Leave_date == leave.To_date:
        if (leave.F_session_1 == True and leave.F_session_2 == False) and (
            leave.T_session_1 == False and leave.T_session_2 == True
        ):
            Total_leaves_applied = 1.0
            for ltypes in types:
                if ltypes.id == int(leave.Leave_type):
                    user = us.leavebalances.filter(leavetype__id=ltypes.id).first()
                    user.balance = user.balance - Decimal(Total_leaves_applied)
                    user.leaves_taken = user.leaves_taken + Decimal(
                        Total_leaves_applied
                    )
                    leave.approved_by = request.user
                    leave.approved_on = datetime.now()
                    user.save()
                    # us.save()

        elif (
            (leave.F_session_1 == True and leave.F_session_2 == False)
            and (leave.T_session_1 == True and leave.T_session_2 == False)
        ) or (
            (leave.F_session_1 == False and leave.F_session_2 == True)
            and (leave.T_session_1 == False and leave.T_session_2 == True)
        ):
            Total_leaves_applied = 0.5
            for ltypes in types:
                if ltypes.id == int(leave.Leave_type):
                    user = us.leavebalances.filter(leavetype__id=ltypes.id).first()
                    user.balance = user.balance - Decimal(Total_leaves_applied)
                    user.leaves_taken = user.leaves_taken + Decimal(
                        Total_leaves_applied
                    )
                    leave.approved_by = request.user
                    leave.approved_on = datetime.now()
                    user.save()
                    # us.save()

        else:
            Total_leaves_applied = 1.0
            for ltypes in types:
                if ltypes.id == int(leave.Leave_type):
                    user = us.leavebalances.filter(leavetype__id=ltypes.id).first()
                    user.balance = user.balance - Decimal(Total_leaves_applied)
                    user.leaves_taken = user.leaves_taken + Decimal(
                        Total_leaves_applied
                    )
                    leave.approved_by = request.user
                    leave.approved_on = datetime.now()
                    user.save()
                    # us.save()
    else:
        tdelta = leave.To_date - leave.Leave_date
        
        if leave.Leave_type == 'paternity':
                paternityleavetaken=Leavebalance.objects.filter(emp=us).filter(leavetype__leavetype='paternity').first()
                paternityleavetaken.times_applied = paternityleavetaken.times_applied + 1
                paternityleavetaken.save()
        

        if (leave.F_session_1 == True and leave.F_session_2 == False) and (
            leave.T_session_1 == False and leave.T_session_2 == True
        ):
            Total_leaves_applied = tdelta.days + 1

            for ltypes in types:
                if ltypes.leavetype == leave.Leave_type:
                    user = us.leavebalances.filter(leavetype__id=ltypes.id).first()
                    user.balance = user.balance - Decimal(Total_leaves_applied)
                    user.leaves_taken = user.leaves_taken + Decimal(
                        Total_leaves_applied
                    )
                    leave.approved_by = request.user
                    leave.approved_on = datetime.now()
                    user.save()
                    # us.save()
        elif (
            (leave.F_session_1 == True and leave.F_session_2 == False)
            and (leave.T_session_1 == True and leave.T_session_2 == False)
        ) or (
            (leave.F_session_1 == False and leave.F_session_2 == True)
            and (leave.T_session_1 == False and leave.T_session_2 == True)
        ):
            Total_leaves_applied = tdelta.days + 0.5
            for ltypes in types:
                if ltypes.id == int(leave.Leave_type):
                    user = us.leavebalances.filter(leavetype__id=ltypes.id).first()
                    user.balance = user.balance - Decimal(Total_leaves_applied)
                    user.leaves_taken = user.leaves_taken + Decimal(
                        Total_leaves_applied
                    )
                    leave.approved_by = request.user
                    leave.approved_on = datetime.now()
                    user.save()
                    # us.save()
        else:
            Total_leaves_applied = tdelta.days + 1
            for ltypes in types:
                if ltypes.id == int(leave.Leave_type):
                    user = us.leavebalances.filter(leavetype__id=ltypes.id).first()
                    user.balance = user.balance - Decimal(Total_leaves_applied)
                    user.leaves_taken = user.leaves_taken + Decimal(
                        Total_leaves_applied
                    )
                    leave.approved_by = request.user
                    leave.approved_on = datetime.now()
                    user.save()
                    # us.save()
    leave.save()

    return redirect(employeerequest)


def rejectleave(request, pk):
    leave = Leaves.objects.get(id=pk)
    leave.Is_approved = False
    leave.save()
    return redirect(employeerequest)


def downloadfile(request):
    content1 = request.POST.get("content1")
    content2 = request.POST.get("content2")
    content3 = request.POST.get("content3")
    content4 = request.POST.get("content4")
    content5 = request.POST.get("content5")
    content6 = request.POST.get("content6")
    
    # Create a new Excel workbook
    workbook = openpyxl.Workbook()
    # Get the active worksheet
    worksheet = workbook.active

    worksheet["A1"] = content1
    worksheet["A2"] = content2
    worksheet["A3"] = content3
    worksheet["A4"] = content4
    worksheet["A5"] = content5
    worksheet["A6"] = content6
   

    # Setting the content type and filename of the response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="content.xlsx"'
    # Save the workbook to the response
    workbook.save(response)
    return response


def addregion(request):
    if request.method == "POST":
        x = request.POST["region"]
        data = Region(country=x)
        data.save()
        messages.success(request, "Region Added Successfully.")
        return redirect(addregion)
    return render(request, "Admin/addregion.html")


def updateemp(request):
    if request.method == "POST":
        x = request.POST["email"]
        data = EmailValidation.objects.get(email=x)
        data
    email = CustomUser.objects.all()
    context = {
        "email": email,
    }
    return render(request, "Admin/updateemp.html", context)


def deleteholiday(request):
    holidays = AllHolidays.objects.all()
    context = {
        "holidays": holidays,
    }
    return render(request, "Admin/deleteholiday.html", context)


def dlt(request, id):
    hol = AllHolidays.objects.get(id=id)
    hol.delete()
    messages.success(request, "Holiday Deleted Successfully.")
    return redirect(deleteholiday)


def theleaves(request):
    email = request.user.email

    if EmailValidation.objects.filter(email=email).exists():
        user_email = EmailValidation.objects.filter(email=email).first()

        if request.method == "POST":
            Leaves_type = request.POST["Leave_type"]

            Leave_date = request.POST["From Date"]

            if request.POST["F_session"] == "session_1":
                F_session_1 = True
                F_session_2 = False
            else:
                F_session_1 = False
                F_session_2 = True

            To_date = request.POST["To Date"]

            if request.POST["T_session"] == "session_2":
                T_session_1 = False
                T_session_2 = True
            else:
                T_session_1 = True
                T_session_2 = False

            Reason = request.POST["Reason"]

            FMyear, FMmonth, FMday = Leave_date.split("-")
            F_date = datetime(int(FMyear), int(FMmonth), int(FMday))
            from_date = F_date

            TMyear, TMmonth, TMday = To_date.split("-")
            T_date = datetime(int(TMyear), int(TMmonth), int(TMday))
            to_date = T_date
            if (F_date.weekday() == int(5) or F_date.weekday() == int(6)) or (
                T_date.weekday() == int(5) or T_date.weekday() == int(6)
            ):
                messages.warning(
                    request,
                    "Leave cannot be applied,your applied leave falls on weekend   ",
                )
                return redirect(theleaves)

            else:
                dates = []
                while F_date <= T_date:
                    dates.append(F_date)
                    F_date += timedelta(days=1)

                weeknumbers = []
                for date in dates:
                    num = date.weekday()
                    weeknumbers.append(num)

                if (int(5) in weeknumbers) or (int(6) in weeknumbers):
                    messages.warning(
                        request, "Leave cannot be applied,weekend fall  between leaves"
                    )
                    return redirect(theleaves)

            Holiday = AllHolidays.objects.filter(Q(date=Leave_date) | Q(date=To_date))

            if len(Holiday) != 0:
                messages.warning(
                    request,
                    "Leave cannot be applied,your applied leave falls on a Holiday ",
                )
                return redirect(theleaves)

            Holidayss = []
            while F_date <= T_date:
                Holidays = AllHolidays.objects.filter(Q(date=F_date))
                if Holidays is not None:
                    Holidayss.append("Holidays falls on your leave")
                    break
                F_date += timedelta(days=1)

            if len(Holidayss) != 0:
                messages.warning(
                    request,
                    "Leave cannot be applied,your applied leave falls on a Holiday ",
                )
                return redirect(theleaves)

            types = Leavetype.objects.all()
            for ltypes in types:
                if ltypes.leavetype == Leaves_type:
                    user = user_email.leavebalances.filter(
                        leavetype__id=ltypes.id
                    ).first()

            if Leaves_type != "Loss of pay":
                if user.balance <= Decimal(0.5):
                    messages.warning(
                        request, "Leave cannot be applied,you have low balance"
                    )
                    return redirect(theleaves)

            if Leave_date == To_date:
                if Leaves_type == "paternity":
                    messages.warning(
                        request, "You can't apply a single day paternity leave"
                    )
                    return redirect(theleaves)
                else:
                    if (F_session_1 == True and F_session_2 == False) and (
                        T_session_1 == False and T_session_2 == True
                    ):
                        Total_days_applying_for = Decimal(1.0)

                    elif (
                        (F_session_1 == True and F_session_2 == False)
                        and (T_session_1 == True and T_session_2 == False)
                    ) or (
                        (F_session_1 == False and F_session_2 == True)
                        and (T_session_1 == False and T_session_2 == True)
                    ):
                        Total_days_applying_for = Decimal(0.5)

                    else:
                        Total_days_applying_for = Decimal(1.0)

            else:
                tdelta = to_date - from_date

                number_of_days = tdelta.days
                
                if (F_session_1 == True and F_session_2 == False) and (
                    T_session_1 == False and T_session_2 == True
                ):
                    Total_days_applying_for = Decimal(number_of_days) + Decimal(1.0)

                    for ltypes in types:
                        if Leaves_type== ltypes.leavetype:
                            user = user_email.leavebalances.filter(
                                leavetype__id=ltypes.id
                            ).first()

                            if Total_days_applying_for > user.balance:
                                messages.warning(
                                    request, "You don't have that many leaves"
                                )
                                return redirect(theleaves)

                elif (
                    (F_session_1 == True and F_session_2 == False)
                    and (T_session_1 == True and T_session_2 == False)
                ) or (
                    (F_session_1 == False and F_session_2 == True)
                    and (T_session_1 == False and T_session_2 == True)
                ):
                    Total_days_applying_for = Decimal(number_of_days) + Decimal(0.5)
                    for ltypes in types:
                        if Leaves_type == ltypes.leavetype:
                            user = user_email.leavebalances.filter(
                                leavetype__id=ltypes.id
                            ).first()

                    if Total_days_applying_for > user.balance:
                        messages.warning(request, "You don't have that many leaves")
                        return redirect(theleaves)

                else:
                    Total_days_applying_for = Decimal(number_of_days) + Decimal(1)
                    for ltypes in types:
                        if Leaves_type == ltypes.leavetype:
                            user = user_email.leavebalances.filter(
                                leavetype__id=ltypes.id
                            ).first()

                    if Total_days_applying_for > user.balance:
                        messages.warning(request, "You don't have that many leaves")
                        return redirect(theleaves)
                    
            if Leaves_type == 'paternity':
                
                paternityleavetaken=Leavebalance.objects.filter(emp=user_email).filter(leavetype__leavetype='paternity').first()
                
                if paternityleavetaken.times_applied > 2:

                    messages.warning(request, "You can't apply for paternity leaves more than twice")
                    return redirect(theleaves)

            

            leave = Leaves.objects.create(
                Emp=user_email,
                Leave_type=Leaves_type,
                Leave_date=Leave_date,
                To_date=To_date,
                Reason=Reason,
                F_session_1=F_session_1,
                F_session_2=F_session_2,
                T_session_1=T_session_1,
                T_session_2=T_session_2,
                Total_days_applying_for=Total_days_applying_for,
            )

            leave.save()
            messages.warning(request, "Leave is successfully applied")
            return redirect(theleaves)

        else:
            user_email = EmailValidation.objects.filter(email=email).first()
            allleavetypes = Leavetype.objects.all()
            context = {"user": user_email, "leavetypes": allleavetypes}
            return render(request, "practise/new.html", context)


def leavehistory(request):
    leave = Leaves.objects.all()
    email = request.user.email
    user_email = EmailValidation.objects.filter(email=email).first()
    types = Leavetype.objects.all()
    context = {"leaves": leave, "user": user_email, "types": types}


    return render(request, "Leave/leavehistory.html", context)


def addleavetype(request):
    if request.method == "POST":
        leavetype = Leavetype()
        leavetype.leavetype = request.POST["Add_Leave_type"]
        leavetype.save()

        email_list = list(EmailValidation.objects.all())
        print(email_list)
        for email in email_list:
            leavebalance = Leavebalance()
            leavebalance.emp = email
            leavebalance.leavetype = Leavetype.objects.last()
            leavebalance.alloated = request.POST["Balance"]
            leavebalance.balance = request.POST["Balance"]
            leavebalance.leaves_taken = 0
            leavebalance.save()
        messages.warning(request, "Leavetype is successfully added ")
        return redirect(addleavetype)

    else:
        return render(request, "Admin/addleavetype.html")


