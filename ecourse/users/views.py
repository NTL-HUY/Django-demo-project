from urllib.parse import urlencode

from django.shortcuts import redirect, render
from ecourse import settings
import requests
from django.views import View

from django.contrib.auth import login, get_user_model

# Create your views here.
class UserView(View):
    @staticmethod
    def login(request):
        return render(request, 'login.html')

    @staticmethod
    def google_login(request):
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"

        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
        }

        url = f"{base_url}?{urlencode(params)}"
        return redirect(url)
    


    @staticmethod
    def google_callback(request):
        code = request.GET.get("code")

        token_url = "https://oauth2.googleapis.com/token"

        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        # đổi code -> access token
        token_response = requests.post(token_url, data=data)
        token_json = token_response.json()

        access_token = token_json.get("access_token")

        # lấy thông tin user
        userinfo_response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        userinfo = userinfo_response.json()

        email = userinfo["email"]
        name = userinfo["name"]
        User = get_user_model()
        # tạo user nếu chưa có
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                "email": email,
                "first_name": name,
            }
        )

        login(request, user)

        return redirect("/") 