# myapp/middleware.py

from datetime import datetime
from django.utils import timezone
from .models import UserActivity


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # start_time = timezone.localtime(timezone.now())
        response = self.get_response(request)
        session = request.session

        
        if request.method == 'GET' or 'POST':
            user = request.user
            if user.is_authenticated:
                emp_id = user.id
                path = request.path
                current_datetime = timezone.localtime(timezone.now())
                # duration = current_datetime - start_time

                # Calculate duration
                # duration = (current_datetime - request.timestamp).total_seconds()

                # Save user activity to database
                UserActivity.objects.create(
                    employee_id=emp_id,
                    path=path,
                    date=current_datetime,
                    time=current_datetime,
                    duration=session
                )

        return response
