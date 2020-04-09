from django.forms import ModelForm, ModelChoiceField, RadioSelect, CheckboxSelectMultiple
from .models import Student
from exam.models import Answer
from student.models import StudentAnswer

class StudentDetailsForm(ModelForm):
    class Meta:
        model = Student
        fields = ["interests","AdharNumber"]

        
class TakeQuizForm(ModelForm):
    answer = ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')

class StudentInterestsForm(ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': CheckboxSelectMultiple
        }
