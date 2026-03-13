
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django.db.models import Count
from django.template.response import TemplateResponse
from courses.models import Category, Course, Lession

# Register your models here.
class MyCoursesAdmin(admin.ModelAdmin):
    list_display = ['id','subject','active','created_date']
    list_filter = ['id','subject','created_date']
    search_fields = ['subject']
    # Thêm trường tùy ý
    readonly_fields = ['image_view']

    def image_view(self,course):
        if course.image:
            return mark_safe(f'<img width="200" src="{course.image.url}"/>')
        return None

# 'widget = component'
class LessionForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False

    class Meta:
        model = Lession
        fields = '__all__'

class MyLessionAdmin(admin.ModelAdmin):
    form = LessionForm

class MyAdminSite(admin.AdminSite):
    site_header = 'Xin chào cu'

    def get_urls(self):
        return [
            path('course-stats/',self.count_stats)
        ] + super().get_urls()
    
    def count_stats(self, request):
        stats = Category.objects.annotate(count=Count('course')).values('id', 'name', 'count')
        return TemplateResponse(
            request,
            'admin/stats.html',
            {'stats': stats}
        )

admin_site = MyAdminSite(name="name ở đây")


admin_site.register(Category)
admin_site.register(Course,MyCoursesAdmin)
admin_site.register(Lession,MyCoursesAdmin)

