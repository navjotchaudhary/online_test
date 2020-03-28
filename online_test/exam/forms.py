from django.forms import ModelForm, BaseInlineFormSet
from .models import Quiz, Question
from django.forms.utils import ValidationError
class QuizCreationForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['name','subject']


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('text', )

        

class BaseAnswerInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')

