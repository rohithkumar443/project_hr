# from django.dispatch import Signal
# from django.utils import timezone
# from .models import UserActivity

# user_accessed_page = Signal()

# # def save_log(sender, **kwargs):
# #     user = kwargs['user']
# #     path = kwargs['path']
# #     start_time = kwargs['start_time']
# #     endtime = timezone.now()
# #     duration = (endtime - start_time)
# #     data = UserActivity(employee_id = user, path = path,accessed_on = start_time, duration=duration)
# #     data.save()
