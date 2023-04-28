from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('',views.signin, name='login'),
    path('signin/',views.signin, name='login'),
    path('registeruser/',views.registeruser,name='registeruser'),
    path('updation/',views.updation, name='updation'),
    path('updation/newupdate/<int:id>',views.newupdate, name='newupdate'),
    path('updation/newupdate/createstatus/<int:id>',views.createstatus, name='createstatus'),
    path('addnewstatus/',views.addnewstatus, name='addnewstatus'),
    #Logout
    path('logout/',views.logout_view, name="logout"),
    # path('lossof/',views.Loss_of_pay,name='lossof'),

    #Alter Employee
    path('alteremployee/', views.alteremp, name='alteremployee'),
    path('addemp/', views.addemp, name='addemp'),
    path('alteremployee/inactive/<int:id>', views.inactive, name='inactive/'),
    path('alteremployee/updateppl/<int:id>', views.updateppl, name='updateppl'),
    path('updateemp/', views.updateemp, name="updateemp"),

    # Add Holiday
    path('addholiday/',views.addholiday, name='addholiday'),
    path('deleteholiday/',views.deleteholiday, name="deleteholiday"),
    path('deleteholiday/dlt/<int:id>',views.dlt, name="dlt"),
    path('holidayview/',views.holidayview, name='holidayview'),
    path('empholidayview/',views.empholidayview, name='empholidayview'),

    #Regularization
    path('regularization/',views.regularization, name='regularization'),
    path('employeerequest/', views.employeerequest, name='employeerequest'),
    path('employeerequest/approverequest/<int:id>',views.approverequest, name='approverequest'),
    path('employeerequest/rejectrequest/<int:id>',views.rejectrequest, name='rejectrequest'),
    path('requests/', views.requests, name='requests'),

    # path('base/',views.base, name='base'),

    #Hr Attendance View
    path('hremployeeattendance/', views.hrempattendance, name='hrempattendance'),
    path('empattendance/',views.attendance, name = 'attendance'),

    path('signinn/',views.signinn,name='sign_inn'),
    path('signoutt/',views.signoutt,name='sign_outt'),

    # path('a/',views.someleave,name='lpractise'),
    # path('aa/<int:pk>/',views.someleaverequest,name='llpractise'),
    path('aaa/',views.allleavereq,name='lllpractise'),

    # add leaves to emp and org

    path('addleave_emp/',views.admin_leave_access,name='addLeave_admin'),
    path('addlea_emp/',views.addleave_emp,name='addLeave_emp'),
    path('addleave_org/',views.addleave_org,name='addLeave_org'),
    path('deleteleave_emp/',views.deleteleave_emp,name='addLeave_emp'),
    path('deleteleave_org/',views.deleteleave_org,name='addLeave_org'),
    path('aleave/<int:pk>/',views.approveleave,name='approveleave'),
    path('aleavee/<int:pk>/',views.rejectleave,name='rejectleave'),
    path('applyleaves/',views.theleaves,name='applyleaves'),
    path('leavehistory/',views.leavehistory,name='leavehistory'),
     path('addleavetype/',views.addleavetype,name='addleavetype'),
    #add region

    path('addregion/',views.addregion, name='addregion'),

    #Download FIle
    path('downloadfile/',views.downloadfile,name="downloadfile"),
]

    # path('home/logout/',views.logout, name='logout'),
    # path('registeruser/register/',views.registeruser,name='register'),
    # path('addstatus/',views.addstatus, name='addstatus'),
    # path('updation/update/<int:id>',views.updatestatus, name='updatestatus'),
    # path('updation/update/updaterecord/<int:id>',views.updaterecord, name='updaterecord'),

    # path('statusupdate/<int:id>',views.statusupdate, name='statusupdate'),
    # path('updation/update/<int:id>'),

    # Latest One


