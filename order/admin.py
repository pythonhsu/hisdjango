from django.contrib import admin
from order.models import UserInfo,Product,OrderDetail,Member

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Product)
admin.site.register(OrderDetail)
admin.site.register(Member)
