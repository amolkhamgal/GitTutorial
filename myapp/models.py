from django.db import models
import datetime

# Create your models here.

class Categary(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Product(models.Model):
    categary=models.ForeignKey(Categary,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    price=models.IntegerField(default=0)
    description=models.CharField(max_length=200)
    image=models.ImageField(upload_to='upload/images')

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)


class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.IntegerField()
    email=models.EmailField()
    password=models.CharField(max_length=500)


    def register(self):
        self.save()

    @staticmethod

    def get_customer_by_email(email):
        try:
          return Customer.objects.get(email=email)
        except:
            return False



    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True

        return False

class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=100,default="",blank=True)
    phone = models.CharField(max_length=50,default="",blank=True)
    date = models.DateTimeField(default=datetime.datetime.now)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()


    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order .objects.filter(customer = customer_id).order_by('-date')


