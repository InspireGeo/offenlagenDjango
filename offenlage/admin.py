from typing_extensions import _AnnotatedAlias
from django.contrib import admin

from .models import Offenlage

from leaflet.admin import LeafletGeoAdmin
from django.contrib.sessions.models import Session


@admin.register(Offenlage)
class OffenlageAdmin(LeafletGeoAdmin):
    search_fields=('title','stadt','owned_by_user',)
    list_display=['title','stadt','owned_by_user']
    list_filter=['stadt','owned_by_user']
    readonly_fields = ['owned_by_user','typ','planart','generic_id']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owned_by_user=request.user) 


    def save_model(self, request, obj, form, change):
        if change:
            obj.save() 
        else:
             
             obj.owner = request.user
             obj.last_modified_by = request.user
             obj.save() 
