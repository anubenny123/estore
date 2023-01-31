from django.shortcuts import render,redirect
# from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View, CreateView,TemplateView,FormView,DetailView,ListView
from customer import forms
from django.contrib.auth import authenticate,login,logout
from owner.models import Products,Carts,Orders


# Create your views here.
# def home(request):
#     return HttpResponse("hello world")

class RegistrationView(CreateView):
    form_class = forms.RegistrationForm
    template_name = "Registration.html"
    success_url = reverse_lazy("login")

class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                if request.user.is_superuser:
                    return redirect("dashboard")
                else:
                    return redirect("home")
            else:
                return render("login.html",{"form":form})

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        all_products=Products.objects.all()
        context["products"]=all_products
        return context


class ProductDetailView(DetailView):
    template_name = "product-detail.html"
    model=Products
    context_object_name ="product"
    pk_url_kwarg = "id"


class AddToCartView(FormView):
    template_name = "addto-cart.html"
    form_class = forms.CartForm

    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        product=Products.objects.get(id=id)
        return render(request,self.template_name,{"form":forms.CartForm(),"product":product})

    def post(self, request, *args, **kwargs):
        id=kwargs.get("id")
        product=Products.objects.get(id=id)
        qty=request.POST.get("qty")
        user=request.user
        Carts.objects.create(product=product,user=user,qty=qty)
        return redirect("home")


class MyCartView(ListView):
    model = Carts
    template_name = "cart-list.html"
    context_object_name = "carts"


    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user).exclude(status="cancelled").order_by("-created_date")

class CartRemoveView(ListView):
    template_name = "cart-list.html"
    form_class=forms.CartForm
    context_object_name = "carts"

    def get_queryset(self):
        id=self.kwargs.get("id")
        cart=Carts.objects.get(id=id)
        cart.status="cancelled"
        cart.delete()
        return Carts.objects.filter(user=self.request.user).exclude(status="cancelled").order_by("-created_date")



class PlaceOrderView(FormView):
    template_name = "place-order.html"
    form_class = forms.OrderForm


    def post(self, request, *args, **kwargs):
        cart_id = kwargs.get("c_id")
        product_id = kwargs.get("p_id")
        cart = Carts.objects.get(id=cart_id)
        product = Products.objects.get(id=product_id)
        user = request.user
        delivered_address= request.POST.get("delivered_address")
        Orders.objects.create(product=product, user=user, delivered_address=delivered_address)
        cart.status = "order-placed"
        cart.save()
        return redirect("home")


class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")











