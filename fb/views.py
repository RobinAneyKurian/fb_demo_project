import imp
from django.shortcuts import render, redirect

from django.views import View

from django.contrib.auth import authenticate, login, logout

from fb.forms import UserRegistrationForm, UserLoginForm, UserProfileDetails, UploadShoppingProducts

from django.views.generic import CreateView, View, ListView, DetailView, DeleteView

from django.contrib.auth.models import User

from django.urls import reverse_lazy

from django.contrib import messages

from fb.forms import UserLoginForm,UserRegistrationForm, UpoloadPostForm, UserProfileForm, UploadShoppingProductsForm, UploadVideosForm, BuyProductUserDetailsForm

from fb.models import  UploadPhotoVideo, UploadVideosModel, BuyProductModel, UploadShoppingProducts, UserProfileDetails

from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache



def signin_required(fn):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request, *args, **kwargs)
    return wrapper


decs = [signin_required, never_cache]


class UserRegistration(View):
    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        return render(request, "fb_create_account.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect("signin")
        else:
            return render(request, "fb_create_account.html", {"form": form})

    

class FacebookLogin(View):

    def get(self, request, *args, **kwargs):
        form = UserLoginForm
        return render(request, "fb_login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usr_object = authenticate(request, username=username, password=password)
            if usr_object:
                login(request, usr_object)
                return redirect("home")
            else:
                messages.error(request, "Invalid Credentials")
                return render(request, "fb_login.html", {"form": form})


@method_decorator(decs, name="dispatch")
class FacebookHome(ListView):
    context_object_name="files"
    model=UploadPhotoVideo
    template_name="fb_home.html"
   

    def get_queryset(self):
        return UploadPhotoVideo.objects.all()


@method_decorator(decs, name="dispatch")
class FacebookBase(View):
    def get(self, request, *args, **kwargs):
        return render(request, "base.html")

@method_decorator(decs, name="dispatch")
class FacebookUploadPostView(CreateView, ListView):
    model = UploadPhotoVideo
    template_name = "fb_upload_post.html"
    form_class = UpoloadPostForm
    success_url = reverse_lazy("home")
    pk_url_kwarg = "id"
    context_object_name = "files"

    # def post_id(request, *args, **kwargs):
    #     id = kwargs.get("id")
    #     postid = UploadPhotoVideo.objects.get(id=id)
    #     return render(request, "fb_home.html", {"id": postid})

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


@signin_required
def delete_post(request, *args, **kwargs):
    id = kwargs.get("id")
    UploadPhotoVideo.objects.get(id=id).delete()
    return redirect("home")


@signin_required
def like_view(request, *args, **kwargs):
    ans_id = kwargs.get("id")
    ans = UploadPhotoVideo.objects.get(id=ans_id)
    ans.like.add(request.user)
    ans.save()
    return redirect("home")



# Profile 
@signin_required
def profile_view(request, *args, **kwargs):
    form = UploadPhotoVideo.objects.filter(user=request.user)
    return render(request ,'fb_profile.html', {"profilepost": form})



@method_decorator(decs, name="dispatch")
# class UserPostInProfile(ListView):
#     model = UserProfileDetails
#     template_name= "profile"
#     context_object_name = "profile"

def UserPostInProfile(request, *args, **kwargs):
    get_id = kwargs.get("id")
    get_user_details = UserProfileDetails.objects.get(id=get_id)
    return render(request, "fb_profile.html", {"profile": get_user_details})

   

    def get_queryset(self):
        return UserProfileDetails.objects.filter(user=self.request.user)





@method_decorator(decs, name="dispatch")
class UserProfileDetailsView(CreateView):
    model = UserProfileDetails
    form_class = UserProfileForm
    template_name = "fb_upload_profile_details.html"
    context_object_name = "form"
    success_url = reverse_lazy("profile")
    pk_url_kwarg = "id"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return UserProfileDetails().include(user=self.request.user)










# Shopping Section


@signin_required
def facebook_shopping(request, *args, **kwargs):
    # get_details = UploadShoppingProducts.objects.all()
    return render(request, "fb_shop.html")



@method_decorator(decs, name="dispatch")
class UploadShoppingProductsView(CreateView):
    template_name = "fb_upload_shopping_products.html"
    model = UploadShoppingProducts
    form_class = UploadShoppingProductsForm
    context_object_name = "products"
    success_url = reverse_lazy("shop")
    pk_url_kwarg = "id"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


@method_decorator(decs, name="dispatch")
class ShoppingProductsListView(ListView):
    model = UploadShoppingProducts
    template_name = "fb_shop.html"
    context_object_name = 'products'
    # success_url = reverse_lazy("shop")
   
    def get_queryset(self):
        return UploadShoppingProducts.objects.all()


def delete_shop_products(request, *args, **kwargs):
    get_id = kwargs.get("id")
    UploadShoppingProducts.objects.get(id=get_id).delete()
    return redirect("shop")



# Buy products from shopping page

def BuyShoppingProducts(request, *args ,**kwargs):
    get_id = kwargs.get("id")
    items = UploadShoppingProducts.objects.get(id=get_id)
    return render(request, "fb_shop_buy_products.html", {"buy": items})


class BuyProductUserDetailsForm(CreateView):
    template_name = "fb_shop_buy_products.html"
    form_class = BuyProductUserDetailsForm
    model = BuyProductModel
    context_object_name = "form"
    







# Reels Section

def upload_videos(request, *args, **kwargs):
    return render(request, "fb_reels.html")

class UploadVideosView(CreateView):
    template_name = "fb_reels.upload.html"
    form_class = UploadVideosForm
    model = UploadVideosModel
    success_url = reverse_lazy("reels")
    context_object_name = "form"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

class ShowUploadedVideosListView(ListView):
    template_name = "fb_reels.html"
    model = UploadVideosModel
    context_object_name = "videos"

    def get_queryset(self):
        return UploadVideosModel.objects.all()

def delete_reels(request, *args, **kwargs):
    get_id = kwargs.get("id")
    UploadVideosModel.objects.get(id=get_id).delete()
    return render(request, "fb_reels.html")


# Add to cart

def productDeatlView(request, *args ,**kwargs):
    get_id = kwargs.get("id")
    items = UploadShoppingProducts.objects.get(id=get_id)
    print(items)
    return render(request, "fb_product_detail_view.html", {"buy_products": items})





# Signout
   
decs
def LogoutSessionView(request, *args, **kwargs):
    logout(request)
    return redirect("signin")