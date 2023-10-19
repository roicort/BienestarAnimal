from apirest.urls import drf_router
from .viewsets import AnimalCategoriaViewSet, AnimalInclusionViewSet, AdopcionViewSet, AnimalViewSet, ReportePerdidoViewSet, PostulacionAdopcionViewSet, MisPostulacionesAnimalViewSet, AnimalFavoritoViewSet

urlpatterns = []

drf_router.register(r'animales/padron', AnimalViewSet, basename='nimales-animal')
drf_router.register(r'animales/adopciones', AdopcionViewSet, basename='adopciones-animal')
drf_router.register(r'animales/reportes', ReportePerdidoViewSet, basename='empleos-reporte-perdido')
drf_router.register(r'animales/postulacion-adopcion', PostulacionAdopcionViewSet, basename='empleos-postulacion-animal')
drf_router.register(r'animales/mis-postulaciones', MisPostulacionesAnimalViewSet, basename='mis-postulacion-animal')
drf_router.register(r'animales/animal-favorito', AnimalFavoritoViewSet, basename='empleos-animal-favorita')
drf_router.register(r'animales/animal-categoria', AnimalCategoriaViewSet, basename='empleos-animal-categoria')
drf_router.register(r'animales/animal-inclusion', AnimalInclusionViewSet, basename='empleos-animal-inclusion')

urlpatterns += drf_router.urls
