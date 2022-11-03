from django.contrib import admin
from.models import Categary,Product,Customer,Order

# Register your models here.

class AdminCategary(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Categary,AdminCategary)


class AdminProduct(admin.ModelAdmin):
    list_display = ('name','price','description','image','categary')

admin.site.register(Product,AdminProduct)


class AdminCustomer(admin.ModelAdmin):
    list_display = ('first_name','last_name','phone','email','password')

admin.site.register(Customer,AdminCustomer)


class AdminOrder(admin.ModelAdmin):
    list_display = ('product','customer','quantity','price','address','phone','date','status')

admin.site.register(Order,AdminOrder)