from django.shortcuts import render

# Create your views here.

from gisserver.features import FeatureType, ServiceDescription
from gisserver.geometries import CRS, WGS84
from gisserver.views import WFSView
from .models import ReportePerdido

RD_NEW = CRS.from_srid(28992)

class ReportePerdidosWFSView(WFSView):
    """An simple view that uses the WFSView against our test model."""

    xml_namespace = "http://example.org/gisserver"

    # The service metadata
    service_description = ServiceDescription(
        title="Reportes de Animales Perdidos",
        abstract="Unittesting",
        keywords=["sdhis, animales, perdidos"],
        provider_name="SIGA",
        provider_site="https://www.monterrey.gob.mx/siga",
        contact_person="Coodinación de Ciencia de Datos",
    )

    # Each Django model is listed here as a feature.
    feature_types = [
        FeatureType(
            ReportePerdido.objects.all(),
            fields="__all__",
            other_crs=[RD_NEW]
        ),
    ]