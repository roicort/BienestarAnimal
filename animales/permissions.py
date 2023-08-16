from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from asociaciones.models import VinculacionAsociacion

#
class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_staff
        )


class IsStaffOrCoordinadorEmpresaOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user
        )

    def has_object_permission(self, request, view, obj):
        try:
            obj = obj.asociacion
        except Exception:
            pass
        es_coordinador = VinculacionAsociacion.objects.filter(asociacion=obj, user=request.user, user_rol='coordinador').exists()
        if request.user.is_authenticated and request.user.is_staff:
            return True
        elif request.user.is_authenticated and es_coordinador:
            return True
        elif request.user and request.method in SAFE_METHODS:
            return True
        else:
            return False


class IsStaffOrVinculacionAsociacionOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user
        )

    def has_object_permission(self, request, view, obj):
        try:
            obj = obj.asociacion
        except Exception:
            pass
        tiene_vinculo = VinculacionAsociacion.objects.filter(asociacion=obj, user=request.user).exists()
        if request.user.is_authenticated and request.user.is_staff:
            print("es staff")
            return True
        elif request.user.is_authenticated and tiene_vinculo:
            print("tiene vinculo")
            return True
        elif request.user and request.method in SAFE_METHODS:
            print("safe methods")
            return True
        else:
            print("false")
            return False
