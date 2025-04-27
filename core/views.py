from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

from .models import UserProfile, Store
from .utils import throw_unauthenticated
from .constants import USER_TYPES

@api_view()
def profile(request):
    res = throw_unauthenticated(request)
    if res: return res
    profile = UserProfile.objects.get(user=request.user)
    return Response({
        "type": profile.type, 
        "address": profile.shipping_address,
    })

@api_view()
def store_info(request):
    res = throw_unauthenticated(request)
    if res: return res
    profile = UserProfile.objects.get(user=request.user)
    if profile.type != "vendor":
        return Response({
            "error": "You must be a vendor",
        })
    try:
        store = Store.objects.get(vendor=request.user)
    except Store.DoesNotExist:
        return Response({
            "error": "Store info hasn't been created yet",
        })
    return Response({
        "name": store.name,
        "phone": store.phone,
        "address": store.address,
        "category": store.categroy,
    })

@api_view(http_method_names=['PATCH'])
def set_store_info(request):
    res = throw_unauthenticated(request)
    if res: return res
    profile = UserProfile.objects.get(user=request.user)
    if profile.type != "vendor":
        return Response({
            "error": "You must be a vendor",
        })
    try:
        store = Store.objects.get(vendor=request.user)
    except Store.DoesNotExist:
        store = Store(vendor=request.user)
    if "name" in request.data:
        store.name = request.data["name"]
    if "phone" in request.data:
        store.phone = request.data["phone"]
    if "address" in request.data:
        store.address = request.data["address"]
    if "category" in request.data:
        store.categroy = request.data["category"]
    store.save()
    return Response({
        "message": "success"
    })

@api_view(http_method_names=['PUT'])
def set_type(request):
    res = throw_unauthenticated(request)
    if res: return res
    try:
        if request.data["type"] == "none" or request.data["type"] not in [x[0] for x in USER_TYPES]:
            return Response({
                "error": "Invalid type",
            })
        profile = UserProfile.objects.get(user=request.user)
        if profile.type != "none":
            return Response({
                "error": "You cannot set type multiple times.",
            })
        profile.type = request.data["type"]
        profile.save()
        return Response({
            "message": "success",
        })
    except:
        return Response({
            "error": "Invalid request",
        })

@api_view(http_method_names=['PUT'])
def set_shipping_address(request):
    res = throw_unauthenticated(request)
    if res: return res
    if "address" not in request.data:
        return Response({
            "error": "No address was provided",
        })
    profile = UserProfile.objects.get(user=request.user)
    profile.shipping_address = request.data["address"]
    profile.save()

    return Response({
        "message": "success",
    })

def demo_login(request):
    return render(request, "core/demo.html")

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter