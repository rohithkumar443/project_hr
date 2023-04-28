from django.contrib import admin
from .models import CustomUser,EmailValidation,AllHolidays,Region,Regularization,UserActivity,Attendance,Leaves,Role,Leavebalance,Leavetype
# Register your models here.


# admin.site.register(Leaves,LeavesAdmin)

class LeavesAdmin(admin.ModelAdmin):
    list_display=['Emp','Reason','Leave_date','To_date','Total_days_applying_for']
    list_editable=['Total_days_applying_for']
    ordering=['Leave_date']
    list_select_related=['Emp']
    
    # def Total_leaves_taken(self,Leaves):
    #     return Leaves.Emp.Leaves_taken


class LeaveBalanceadmin(admin.ModelAdmin):
    list_display=['emp','leavetype','balance','leaves_taken']
    list_editable=['balance','leaves_taken']
    list_select_related=['emp','leavetype']
admin.site.register(Leavebalance,LeaveBalanceadmin)
admin.site.register(CustomUser)
admin.site.register(EmailValidation)
admin.site.register(AllHolidays)
admin.site.register(Region)
admin.site.register(Regularization)
admin.site.register(UserActivity)
admin.site.register(Attendance)
admin.site.register(Leaves,LeavesAdmin)
admin.site.register(Role)
admin.site.register(Leavetype)


