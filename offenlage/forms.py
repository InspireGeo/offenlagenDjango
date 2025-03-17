from django import forms
from .models import Offenlage
from leaflet.forms.widgets import LeafletWidget
from django.contrib.gis.geos import GEOSGeometry


class OffenlageForm(forms.ModelForm):
    gml_file = forms.FileField(required=False, label="Upload GML file")

    class Meta:
        model = Offenlage
        exclude = ['generic_id', 'created', 'changed', 'deleted', 'active', 'owned_by_user']
        
        widgets = {
            'the_geom': LeafletWidget(attrs={
            'settings_overrides': {
                'DEFAULT_CENTER': (50.3563, 7.5886),
                'DEFAULT_ZOOM': 15,
                'SCALE': 'metric',
                'MIN_ZOOM': 3,
                'MAX_ZOOM': 18,
    
                'TILES': [
        # OpenStreetMap Base Layer
                    ('OpenStreetMap', 
                    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', 
                    {
                     'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                     
                    }),
                    ('Aerial Image',
         '//server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
         {'attribution': 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'}),  # noqa

       
        # WMS Layer (RLP WMS)
        # ('RLP WMS', 
        #  'https://geo4.service24.rlp.de/wms/rp_dop20.fcgi?REQUEST=GetCapabilities&VERSION=1.3.0&SERVICE=WMS',
        #  {
        #      'layers': 'wms_rp_dop20',
        #      'format': 'image/png',
        #      'transparent': True,
        #      'attribution': 'RLP Geoportal WMS',
        #      'maxZoom': 18,
        #      'minZoom': 3,
        #      'CRS': 'EPSG:3857',
        #  })
    ],
                'CRS': 'EPSG:3857',  # Harita CRS'sini belirleme
                'DRAW': {
                    'polyline': True,
                    'polygon': True,
                    'circle': True,
                    'rectangle': True,
                    'marker': True,
                    'circlemarker': False,
                },
                'EDIT': {
                    'featureGroup': True,
    },
                'OVERLAYS': [
                    ('RLP WMS Overlay', 
                     'https://geo4.service24.rlp.de/wms/rp_dop20.fcgi?', 
                        {
                            'layers': 'wms_rp_dop20',
                            'format': 'image/png',
                            'transparent': True,
                            'attribution': 'RLP Geoportal WMS',
                            'maxZoom': 18,
                            'minZoom': 3,
                            'CRS': 'EPSG:3857',
                        }),
                ],
            }
        }),
            
            'offenlage_beginn': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'offenlage_ende': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'offenlage_bekanntmachung': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'uvp_beginn': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'uvp_ende': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
    # def __init__(self, *args, **kwargs):
    #     super(OffenlageForm, self).__init__(*args, **kwargs)
        
    #     # UVP alanları
    #     self.uvp_fields = ['uvp_vorpruefung ','uvp','uvp_beginn', 'uvp_ende','uvp_kosten','uvp_url']
        
    #     # Diğer alanlar (UVP dışındaki tüm alanlar)
    #     self.non_uvp_fields = [field for field in self.fields if field not in self.uvp_fields]