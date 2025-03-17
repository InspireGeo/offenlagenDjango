from django.db import models
from django.db.models.base import Model

from statistics import mode
import os, uuid
from django.contrib.gis.db import models
from django.contrib.gis.forms.widgets import OSMWidget
from django.urls import reverse
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
import json


# Create your models here.
class GenericMetadata(models.Model):
    generic_id = models.UUIDField(default = uuid.uuid4)
    created = models.DateTimeField(null=True)
    changed = models.DateTimeField(null=True)
    deleted = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)
    owned_by_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True
    
class Offenlage(GenericMetadata):

    id = models.AutoField(primary_key=True)
    #uuid = models.CharField(max_length=300, null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    title = models.CharField(max_length=300, null=True, blank=True)

    #createdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    #changedate = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    #lastchanged = models.DateTimeField(auto_now=True, null=True, blank=True)

    offenlage_url = models.CharField(max_length=300, null=True, blank=True)
    #owner = models.CharField(max_length=300, null=True, blank=True)
    #owner = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)
    #owner = models.OneToOneField(settings.AUTH_USER_MODEL, default=1,on_delete=models.CASCADE)
    gkz = models.CharField(max_length=300, null=True, blank=True)
    stadt = models.CharField(max_length=300, null=True, blank=True)
    planart  = models.IntegerField( null=True, blank=True)
    rechtsstand  = models.IntegerField(null=True, blank=True)
    offenlage_beginn = models.DateField('offenlage begin',max_length=300, null=True, blank=True)
    offenlage_ende = models.DateField('offenlage ende',max_length=300, null=True, blank=True)
    kontakt = models.CharField(max_length=2048, null=True, blank=True)
    notiz = models.CharField(max_length=2048, null=True, blank=True)
    public = models.BooleanField(default=True, null=True, blank=True)
    the_geom= models.MultiPolygonField(srid=4326,null=True,blank=True)
    #the_geom2= models.GEOSGeometry(the_geom)
    #the_geom_geojson= models.TextField( null=True, blank=True) 
    TYP_PLANART = [("BPLAN", (
    ("BPlan_10000", "einfacher BPlan"),
    ("BPlan_10001", "qualifizierter BPlan"),
    ("BPlan_2000'", "BPlanNachParag13"),
    ("BPlan_3000", "vorhabenbezogener BPlan"),
    ("BPlan_4000", "Innenbereichssatzung"),
    ("BPlan_40000", "Klarstellungssatzung"),
    ("BPlan_40001", "Entwicklungssatzung"),
    ("BPlan_40002", "Ergaenzungssatzung"),
    ("BPlan_5000", "AussenbereichsSatzung"),
    ("BPlan_6000", "BPlan_Innenentwicklung"),
    ("BPlan_7000", "OertlicheBauvorschrift"),
    ("BPlan_9999", "Sonstiges"),)),

    ("FPLAN", (
     ("FPlan_10000", "FPlan"),
     ("FPlan_2000", "GemeinsamerFPlan"),
     ("FPlan_3000'", "RegFPlan"),
     ("FPlan_4000", "FPlanRegPlan"),
     ("FPlan_5000", "FPlanNachParag13"),)
     ), ]

    typ_planart = models.CharField(max_length=300,
                               choices=TYP_PLANART,
                               default="einfacher BPlan")
    #typ_planart = models.CharField(max_length=300, null=True, blank=True)
    typ = models.CharField(max_length=30, null=True, blank=True)
    offenlage_bekanntmachung = models.DateField('Offenlage bekanntmachung',max_length=300, null=True, blank=True)
    uvp_vorpruefung = models.BooleanField(default=True, null=True, blank=True)
    uvp = models.BooleanField(default=True, null=True, blank=True)
    uvp_beginn = models.DateField('uvp begin',max_length=300, null=True, blank=True)
    uvp_ende = models.DateField('uvp ende',max_length=300, null=True, blank=True)
    uvp_kosten = models.FloatField(null=True, blank=True)
    uvp_url = models.CharField(max_length=2048, null=True, blank=True)
   
   
    def __str__(self):
        return  self.name
    
   
    
  