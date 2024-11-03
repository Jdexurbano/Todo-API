from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','user','title',)

# Register your models here.

admin.site.register(Task,TaskAdmin)