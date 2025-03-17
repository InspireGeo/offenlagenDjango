from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
import os
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone

import offenlage
from .forms import OffenlageForm
from django.contrib import messages
from .models import Offenlage

import fiona
from shapely.geometry import shape 
from django.contrib.gis.geos import GEOSGeometry
import tempfile
import xml.etree.ElementTree as ET
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .tables import OffenlageTable  # Tabloyu ekleyin
from .OffenlageSearchForm import OffenlageSearchForm
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db import models
from django.db.models import Q


# Ana sayfa
def index(request):
    return render(request, "index.html")  # index.html sayfasını render ediyoruz

def about(request):
    return render(request, "about.html")  # about.html sayfasını render ediyoruz


@login_required(login_url="user:login")
def offenlagedashboard(request):
    form = OffenlageSearchForm(request.GET or None)

    # Kullanıcının yarattığı Offenlagen nesnelerini alıyoruz
    offenlagen = Offenlage.objects.filter(owned_by_user=request.user)

    # Eğer form geçerliyse ve arama terimi varsa
    if form.is_valid():
        search_term = form.cleaned_data.get('search')
        if search_term:
            # Hem title hem de stadt alanında arama yap
            offenlagen = offenlagen.filter(
                Q(title__icontains=search_term) | Q(stadt__icontains=search_term)
            )

    today = timezone.now().date()

    # Üç ayrı liste oluştur: aktif, upcoming ve pasif
    active_offenlagen = []
    upcoming_offenlagen = []
    inactive_offenlagen = []

    for offenlage in offenlagen:
        if offenlage.offenlage_beginn and offenlage.offenlage_beginn > today:
            upcoming_offenlagen.append(offenlage)
        elif offenlage.offenlage_ende and offenlage.offenlage_ende < today:
            inactive_offenlagen.append(offenlage)
        elif offenlage.offenlage_beginn and offenlage.offenlage_beginn <= today and (offenlage.offenlage_ende is None or offenlage.offenlage_ende >= today):
            active_offenlagen.append(offenlage)
        else:
            inactive_offenlagen.append(offenlage)

    # Tüm Offenlagen'ları sıralı bir şekilde birleştiriyoruz: Aktif, Upcoming, Pasif
    sorted_offenlagen = active_offenlagen + upcoming_offenlagen + inactive_offenlagen

    # Django-Tables2 tablosunu oluştur
    table = OffenlageTable(sorted_offenlagen)  # Tablonun verilerini geçiyoruz

    # Pagination
    page = request.GET.get('page')

    # Sayfanın geçerli bir tam sayı olup olmadığını kontrol et
    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1  # Varsayılan olarak 1. sayfayı ayarla

    table.paginate(page=page, per_page=10)  # Sayfa başına 10 kayıt

    context = {
        "table": table,  # Tabloyu bağlayın
        "form": form,
    }

    return render(request, "offenlagedashboard.html", context)


@login_required(login_url="user:login")
def addoffenlage(request):
    if request.method == 'POST':
        form = OffenlageForm(request.POST, request.FILES)
        if form.is_valid():
            offenlage = form.save(commit=False)
            offenlage.owned_by_user = request.user
            offenlage.created = timezone.now()
            offenlage.changed = timezone.now()
            # GML-Datei prüfen
            gml_file = request.FILES.get('gml_file')
            if gml_file:
                try:
                    # GML dosyasını işleme al
                    with fiona.BytesCollection(gml_file.read()) as src:
                        for feature in src:
                            geom = feature['geometry']  
                            shapely_geom = shape(geom)
                            wkt_geom = shapely_geom.wkt
                            geos_geom = GEOSGeometry(wkt_geom)
                            offenlage.the_geom = geos_geom
                    messages.success(request, "Geometrie wurde erfolgreich aus der GML-Datei geladen.")
                except Exception as e:
                    messages.warning(request, f"Beim Laden der GML-Datei ist ein Fehler aufgetreten: {str(e)}")
            
            offenlage.save()
            messages.success(request, "Offenlage wurde erfolgreich hinzugefügt.") 
            return redirect('offenlage:offenlagedashboard')
    else:
        form = OffenlageForm()

    return render(request, 'addoffenlage.html', {'form': form})


@login_required(login_url="user:login")
def detailOffenlage(request, id):
    offenlage = get_object_or_404(Offenlage, id=id)
    # Kullanıcının offfennlage'yi sahibi olup olmadığını kontrol et
    if offenlage.owned_by_user != request.user:
        messages.warning(request, "Bu veriyi görüntüleme yetkiniz yok.")
        return redirect('offenlage:offenlagedashboard')

    return render(request, "detailOffenlage.html", {"offenlage": offenlage})


@login_required(login_url="user:login")
def updateOffenlage(request, id):
    offenlage = get_object_or_404(Offenlage, id=id)
    # Kullanıcının offfennlage'yi sahibi olup olmadığını kontrol et
    if offenlage.owned_by_user != request.user:
        messages.warning(request, "Sie haben keine Berechtigung, diese Daten zu aktualisieren.")
        return redirect('offenlage:index')

    form = OffenlageForm(request.POST or None, request.FILES or None, instance=offenlage)

    if form.is_valid():
        offenlage = form.save(commit=False)
        offenlage.changed = timezone.now()
        offenlage.owned_by_user = request.user
        # GML-Datei prüfen
        gml_file = request.FILES.get('gml_file')
        if gml_file:
            try:
                # GML dosyasını işleme al
                with fiona.BytesCollection(gml_file.read()) as src:
                    for feature in src:
                        geom = feature['geometry']
                        shapely_geom = shape(geom)
                        wkt_geom = shapely_geom.wkt
                        geos_geom = GEOSGeometry(wkt_geom)
                        offenlage.the_geom = geos_geom
                messages.success(request, "Geometrie wurde erfolgreich aus der GML-Datei geladen.")
            except Exception as e:
                messages.warning(request, f"Beim Laden der GML-Datei ist ein Fehler aufgetreten: {str(e)}")
        
        offenlage.save()
        messages.success(request, "Offenlage wurde erfolgreich aktualisiert.") 
        return redirect("offenlage:offenlagedashboard")

    return render(request, "updateOffenlage.html", {"form": form})


@login_required(login_url="user:login")
def deleteOffenlage(request, id):
    offenlage = get_object_or_404(Offenlage, id=id)
    
    # Kullanıcının offfennlage'yi sahibi olup olmadığını kontrol et
    if offenlage.owned_by_user != request.user:
        messages.warning(request, "Sie haben keine Berechtigung, diese Daten zu löschen.")
        
        return redirect("offenlage:index")
    
    # Eğer silme isteği POST ile geldiyse
    if request.method == 'POST':
        offenlage.delete()
        messages.success(request, "Offenlage wurde erfolgreich gelöscht")
        return redirect("offenlage:offenlagedashboard")
    
    # Eğer GET isteği ise kullanıcıdan onay iste
    return render(request, "confirm_delete_offenlage.html", {'offenlage': offenlage})
