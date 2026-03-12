from django.contrib import admin
from django import forms
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path, URLResolver
from django.utils.html import mark_safe # type: ignore

from courses.models import Category, Course, Lesson

from ckeditor_uploader.widgets import CKEditorUploadingWidget
class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonAdmin(admin.ModelAdmin):
    form = LessonForm  

# Register your models here.
class MyCourseAdmin(admin.ModelAdmin):
    list_display = ['id','subject','active','created_date']
    list_filter = ['id','subject','created_date']
    search_fields = ['subject']
    readonly_fields = ['image_view']

    def image_view(self,course):
        if course.image:
            return mark_safe(f'<image src={course.image.url} width="120" />')
        
class MyAdminSite(admin.AdminSite):
    site_header = 'Xin chào cậu'

    def get_urls(self): # type: ignore
        return [
            path('course-stats/',self.course_stats)
        ] + super().get_urls()

    def course_stats(self,request):
        stats = Course.objects.annotate(count=Count('lesson')).values('id','subject','count')
        count = Course.objects.filter(active=True).count()
        return TemplateResponse(request,'admin/stats.html',{
            'course_count': count,
            'course_stats': stats
        })
admin_site = MyAdminSite()

admin_site.register(Course, MyCourseAdmin)
admin_site.register(Category)
admin_site.register(Lesson,LessonAdmin)
