from apirest.urls import drf_router
from .viewsets import AnimalCategoriaViewSet, AnimalCaracteristicaViewSet, AdopcionViewSet, AnimalViewSet, ReportePerdidoViewSet, PostulacionAdopcionViewSet, MisPostulacionesAnimalViewSet, AnimalFavoritoViewSet, ReporteCiudadanoPerdidoViewSet

urlpatterns = []

drf_router.register(r'animales/padron', AnimalViewSet, basename='animales-animal')
drf_router.register(r'animales/adopciones', AdopcionViewSet, basename='animales-adopciones-animal')
drf_router.register(r'animales/reportes', ReportePerdidoViewSet, basename='animales-reporte-perdido')
drf_router.register(r'animales/reportes-ciudadanos', ReporteCiudadanoPerdidoViewSet, basename='animales-reporte-perdido')
drf_router.register(r'animales/postulacion-adopcion', PostulacionAdopcionViewSet, basename='animales-postulacion-animal')
drf_router.register(r'animales/mis-postulaciones', MisPostulacionesAnimalViewSet, basename='mis-postulacion-animal')
drf_router.register(r'animales/animal-favorito', AnimalFavoritoViewSet, basename='animales-animal-favorita')
drf_router.register(r'animales/animal-categoria', AnimalCategoriaViewSet, basename='animales-animal-categoria')
drf_router.register(r'animales/animal-inclusion', AnimalCaracteristicaViewSet, basename='animales-animal-inclusion')

urlpatterns += drf_router.urls
