"""Facebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from fb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', views.FacebookLogin.as_view(), name="signin"),
    path('register/', views.UserRegistration.as_view(), name="register"),
    path("", views.FacebookHome.as_view(), name="home"),
    path("base/", views.FacebookBase.as_view(), name="base"),
    path("uploadpost/", views.FacebookUploadPostView.as_view(), name="uploadpost"),
    path('deletepost/<int:id>/', views.delete_post, name="delete"),
    path('likepost/<int:id>/', views.like_view, name="like"),
    path('profile/', views.profile_view, name="profile"),
    path('profilepost/', views.UserPostInProfile, name="profilepost"),
    path("profilepicture/", views.UserProfileDetailsView.as_view(), name="pro_pic"),



    
    path('shop/', views.ShoppingProductsListView.as_view(), name="shop"),
    path('addproducts/', views.UploadShoppingProductsView.as_view(), name="addproducts"),
    path("deleteproducts/<int:id>/", views.delete_shop_products, name="deleteShop"),


   


    # path("reels/", views.upload_videos, name="reels"),
    path("reels/", views.ShowUploadedVideosListView.as_view(), name="reels"),
    path("addreel/", views.UploadVideosView.as_view(), name="addreels"),
    # path("videos/", views.ShowUploadedVideos.as_view(), name="videos"),
    path("uploadvideos/", views.ShowUploadedVideosListView.as_view(), name="uploadvideos"),
    path('deletereel/<int:id>/', views.delete_reels, name="deletereel"),


    path('detailview/<int:id>/', views.productDeatlView, name="detailview"),
    # path("cart/<int:id>/", views.AddToCartModel.as_view(), name="cart"),

    path('buyproducts/<int:id>', views.BuyShoppingProducts, name="buy"),
    path('paymentmethod/', views.BuyProductUserDetailsForm.as_view(), name="payment"),




    path('signout/', views.LogoutSessionView, name="signout")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
