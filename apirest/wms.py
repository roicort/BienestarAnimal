from wms import maps, layers, views

from animales.models import ReportePerdido

# Subclass the WmsVectorLayer class and point it to a spatial model.
# Use WmsRasterLayer for rasters
class MyWmsLayer(layers.WmsVectorLayer):
    model = ReportePerdido

# Subclass the WmsMap class and add the layer to it
class MyWmsMap(maps.WmsMap):
    layer_classes = [ MyWmsLayer ]

# Subclass the WmsView to create a view for the map
class MyWmsView(views.WmsView):
    map_class = MyWmsMap