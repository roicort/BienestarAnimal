from users.models import User
from rest_framework import authentication
import firebase_admin.auth as auth


#

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        token = request.headers.get('Authorization')
        print("token", token)
        if not token:
            return None

        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token["uid"]
            print("uid", uid)
        except:
            return None

        try:
            user = User.objects.get(username=uid)
            print("user", user)
            return user

        except Exception as e:
            print(e)
            return None