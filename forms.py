# from django import forms
# from .models import Leaves


# # class leaveform(forms.Form):
# #     Leave_date=forms.DateField()
# #     Reason=forms.CharField(max_length=300)
# #     Leave_type=forms.CharField()
# class dateinput(forms.DateInput):
#     input_type='date'


# class leaveform(forms.ModelForm):
#     class Meta:
#         model=Leaves
#         fields=["Leave_date","Leave_type","Reason"]
#         widgets={'Leave_date':dateinput}
#     Reason=forms.CharField(widget=forms.Textarea(attrs={'row':7}))

# class leaveform1(forms.ModelForm):
#     class Meta:
#         model=Leaves
#         fields=["Leave_date","Leave_type","Reason",'Is_approved']
#         widgets={'Leave_date':dateinput}
#     Reason=forms.CharField(widget=forms.Textarea(attrs={'row':7}))