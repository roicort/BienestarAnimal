from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from .models import VinculacionAsociacion

#


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


class IsStaffOrCoordinadorAsociacionOrReadOnly(permissions.BasePermission):
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


class IsStaffOrVinculoAsociacion(permissions.BasePermission):
    def has_permission(self, request, view):
        # usuario_vinculado = request.user.vinculacionasociacion_set.filter(user=request.user)
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        usuario_vinculado = VinculacionAsociacion.objects.filter(asociacion=obj.id, user=request.user).exists()
        if request.user.is_staff or (request.user.is_authenticated and usuario_vinculado):
            return True
        else:
            return False
