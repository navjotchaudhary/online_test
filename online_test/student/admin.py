from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Student)
admin.site.register(TakenQuiz)
admin.site.register(StudentAnswer)

