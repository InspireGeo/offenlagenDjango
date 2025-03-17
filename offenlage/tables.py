import django_tables2 as tables
from .models import Offenlage
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse
from datetime import datetime

class OffenlageTable(tables.Table):
    action = tables.Column(empty_values=(), verbose_name='Actions')

    class Meta:
        model = Offenlage
        template_name = "django_tables2/bootstrap.html"
        fields = ("title", "stadt", "offenlage_beginn", "offenlage_ende", "action")
        order_by = ('custom_sort')

    def order_custom_sort(self, queryset, is_descending):
        today = timezone.now().date()

        def get_color_priority(record):
            if record.offenlage_beginn and record.offenlage_beginn <= today and (record.offenlage_ende is None or record.offenlage_ende >= today):
                return (1, None, None)  # Yeşil (Aktif)
            elif record.offenlage_beginn and record.offenlage_beginn > today:
                return (2, None, None)  # Mavi (Henüz başlamamış)
            elif record.offenlage_ende and record.offenlage_ende < today:
                return (3, record.offenlage_ende, None)  # Kırmızı (Pasif)
            else:
                return (4, None, record.title.lower())  # Gri (Tarihi olmayanlar)

        queryset = sorted(
            queryset,
            key=lambda record: get_color_priority(record),
            reverse=is_descending
        )
        return queryset, True

    def render_action(self, record):
        return format_html(
            '<a href="/offenlage/offenlageupdate/{id}" class="btn btn-warning">Update</a>'
            '<a href="/offenlage/offenlagedelete/{id}" class="btn btn-danger">Delete</a>',
            id=record.id
        )

    def render_title(self, value, record):
        # Create the URL for the detail view of the offenlage
        url = reverse('offenlage:detailOffenlage', args=[record.id])
        # Return the title as a link with color formatting
        return format_html(
            '<a href="{}" class="{}">{}</a>',
            url,
            self._get_title_class(record),  # Renk sınıflandırması
            value
        )

    def render_offenlage_beginn(self, value, record):
        # Tarihi 'dd/mm/yyyy' formatında göster
        formatted_date = value.strftime('%d/%m/%Y') if value else ''
        return self._color_value(formatted_date, record)
    
    def render_stadt(self, value, record):
        return self._color_value(value, record)

    def render_offenlage_ende(self, value, record):
        # Tarihi 'dd/mm/yyyy' formatında göster
        formatted_date = value.strftime('%d/%m/%Y') if value else ''
        return self._color_value(formatted_date, record)

    def _color_value(self, value, record):
        today = timezone.now().date()
        if record.offenlage_beginn and record.offenlage_beginn > today:
            return format_html('<span class="text-info">{}</span>', value)  # Mavi (Henüz başlamamış)
        elif record.offenlage_ende and record.offenlage_ende < today:
            return format_html('<span class="text-danger">{}</span>', value)  # Kırmızı (Pasif)
        elif record.offenlage_beginn and record.offenlage_beginn <= today and (record.offenlage_ende is None or record.offenlage_ende >= today):
            return format_html('<span class="text-success">{}</span>', value)  # Yeşil (Aktif)
        else:
            return format_html('<span class="text-secondary">{}</span>', value)  # Gri (Tarihi olmayanlar)

    def _get_title_class(self, record):
        """
        Renk sıralama önceliklerine göre verileri sınıflandır.
        Yeşil > Mavi > Kırmızı > Gri
        """
        today = timezone.now().date()
        if record.offenlage_beginn and record.offenlage_beginn <= today and (record.offenlage_ende is None or record.offenlage_ende >= today):
            return 'text-success'  # Yeşil
        elif record.offenlage_beginn and record.offenlage_beginn > today:
            return 'text-info'  # Mavi
        elif record.offenlage_ende and record.offenlage_ende < today:
            return 'text-danger'  # Kırmızı
        else:
            return 'text-secondary'  # Gri
