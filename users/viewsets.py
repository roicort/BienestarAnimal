from rest_framework import viewsets
from django.http import HttpResponse
from .models import User
from .serializers import UserSerializer, AdminUserSerializer
from .permissions import IsAuthenticatedAndSelfUserOrIsStaff

# Add your viewsets here


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminUserSerializer
        if self.request.user.is_authenticated:
            return UserSerializer
        return HttpResponse('Unauthorized', status=401)

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        if self.request.user.is_authenticated:
            return User.objects.filter(username=self.request.user.username)
        return HttpResponse('Unauthorized', status=401)

    permission_classes = [IsAuthenticatedAndSelfUserOrIsStaff]
    http_method_names = ['get', 'put', 'patch', 'head', 'options']
