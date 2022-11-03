from django.http import HttpResponse
from django.shortcuts import render,redirect,HttpResponseRedirect
from myapp.models import Categary,Product,Customer,Order
from django.contrib.auth.hashers import make_password,check_password
from django.views import View



class Index(View):
    def post(self,request):
        product=request.POST.get('product')
        cart=request.session.get('cart')
        remove=request.POST.get('remove')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1


                else:
                    cart[product] = quantity + 1





            else:
                cart[product] = 1

        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] =cart
        # print('cart',request.session['cart'])
        return redirect('homepage')


    def get(self,request):
        cart=request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        categary = Categary.objects.all()
        product = Product.objects.all()
        categaryID = request.GET.get('categary')

        if categaryID:
            product = Product.objects.filter(categary=categaryID)
        else:
            product = Product.objects.all()

        data = {
            'categary': categary,
            'product': product,
            'categaryID': categaryID,
        }
        # print('you are :',request.session.get('email'))
        return render(request, 'index.html', data)




def signup(request):
    if request.method=="GET":
       return render(request,'signup.html')

    else:
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        password=request.POST.get('password')

        values={
            'first_name':first_name,
            'last_name':last_name,
            'phone':phone,
            'email':email,
            'password':password
        }


        #-------Validation------------------
        error_message=None
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)

        if (not first_name):
            error_message="First Name is Required"
        elif len(first_name) < 4:
            error_message="len of First Name must be 4 or long"

        if (not last_name):
            error_message="Last Name is Required"
        elif len(last_name) < 4:
            error_message="len of Last Name must be 4 or long"

        if (not phone):
            error_message="Phone is Required"
        elif len(phone) < 4:
            error_message="len of Phone must be 4 or long"

        if (not email):
            error_message="Email Address is Required"
        elif len(email) < 4:
            error_message="len of Email Address must be 4 or long"
        #------Email Validation---------
        elif customer.isExists():
            error_message='Email Address is Already registered....'
        if (not password):
            error_message="Password is Required"
        elif len(password) < 4:
            error_message="len of Password must be 4 or long"




        #-------Form Save---------------
        if not error_message:

            customer.password=make_password(customer.password)
            customer.register()
            return redirect('login')
        else:
            data={
                'error':error_message,
                'values':values

            }


            return render (request,'signup.html',data)

class login(View):
    return_url=None
    def get(self,request):
          login.return_url = request.GET.get('return_url')
          return render(request,'login.html')


    def post(self, request):
           email=request.POST.get('email')
           password=request.POST.get('password')

           customer=Customer.get_customer_by_email(email)

           error_message=None
           if customer:
               flag = check_password(password,customer.password)
               if flag:
                  request.session['customer']=customer.id
                  if login.return_url:
                      return HttpResponseRedirect(login.return_url)
                  else:
                      login.return_url = None
                      return redirect('homepage')
               else:
                  error_message = 'Email or Password Invalid'
           else:
               error_message='Email or Password Invalid'
        # print(email,password)
               return render(request,'login.html',{'error':error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self,request):
        ids=list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)

        print(products)
        return render(request,'cart.html',{'products':products})


class CheckOut(View):
    def post (self,request):
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        customer=request.session.get('customer')
        cart=request.session.get('cart')
        products=Product.get_products_by_id(list(cart.keys()))
        # print(address,phone,customer,cart,products)

        for product in products:
            order=Order(customer=Customer(id=customer),
                        product=product,
                        price=product.price,
                        address=address,
                        phone=phone,
                        quantity=cart.get(str(product.id))
                        )
            order.save()
            request.session['cart']={}
            # print(order.placeOrder());

        return redirect('cart')

class OrderView(View):
    def get(self,request):
        customer=request.session.get('customer')
        orders=Order.get_orders_by_customer(customer)
        return render(request,'orders.html',{'orders':orders})



































