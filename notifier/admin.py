from django.contrib import admin
from .models import OutletModel, StockHistory, NotificationRequest

# Register your models here.

class StockHistoryInline(admin.StackedInline):
    model = StockHistory
    max_num = 10
    classes = ('collapse',)
    fields = ('stock_count',)
    ordering = ('-timestamp',)


class OutletAdmin(admin.ModelAdmin):
    model = OutletModel
    list_display = ('name', 'last_checked') #'current_stock', 'last_checked')
    readonly_fields = ('current_stock', 'last_checked') #'stock_history', 'last_checked')
#    inlines = [StockHistoryInline]

    def history_length(self, obj):
        return obj.stockhistory_set.count()

    def last_checked(self, obj):
        first = obj.stockhistory_set.order_by('-timestamp').first()
        return first.timestamp if first is not None else None

    def current_stock(self, obj):
        first = obj.stockhistory_set.order_by('-timestamp').first()
        return first.stock_count if first is not None else None

    def stock_history(self, obj):
        return [x.stock_count for x in obj.stockhistory_set.order_by('timestamp').all() if x is not None]


class NotificationRequestsAdmin(admin.ModelAdmin):
    list_display = ('model', 'created', 'email', 'sent')

admin.site.register(StockHistory)
admin.site.register(OutletModel, OutletAdmin)
admin.site.register(NotificationRequest, NotificationRequestsAdmin)
