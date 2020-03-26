from django.forms import ModelForm
from .models import Student


class StudentDetailsForm(ModelForm):
    class Meta:
        model = Student
        fields = ["interests","AdharNumber"]

        
        