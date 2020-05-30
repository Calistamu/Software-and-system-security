from django.contrib import admin

# Register your models here.
from .models import Student, Course, Score

class ScoreAdmin ( admin.ModelAdmin ):
    list_display = ('course', 'score', 'student')

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Score, ScoreAdmin)
