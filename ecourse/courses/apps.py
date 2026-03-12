from django.apps import AppConfig


# Dùng để load thêm thông tin gì đó thì định nghĩa ở đây
class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
