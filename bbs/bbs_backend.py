from django.contrib.auth.hashers import make_password, check_password
from .models import MyUser

class UsernamePasswordAuth:

    def authenticate(self, request, username, password):
        print("UsernamePasswordAuth.authenticate")
        try:
            user = MyUser.objects.get(username=username)
            print(user.check_password(password))
            if user.check_password(password):
                return user
        except MyUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        print("UsernamePasswordAuth.get_user")
        try:
            user = MyUser.objects.get(pk=user_id)
            return user
        except MyUser.DoesNotExist:
            return None

