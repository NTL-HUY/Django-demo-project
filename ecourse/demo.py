import os
import django
from django.db import connection, reset_queries

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecourse.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

django.setup()


# from pprint import pprint

# from django.db.models import QuerySet

# from courses.models import *
# reset_queries()

# # Course.objects.all()
# # c = Course.objects.filter(category__name__icontains='Programming')
# # print(Category.objects.all())
# # print(c)

# # c = Course.objects.filter(subject__icontains='python')
# c = Course.objects.order_by('-id')[:5]
# print(c)
# pprint(connection.queries)

