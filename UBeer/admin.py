from django.contrib import admin
from UBeer.models import Establishments, Transactions, Riders, Trips


class EstablishmentsAdmin(admin.ModelAdmin):
    pass


class TransactionsAdmin(admin.ModelAdmin):
    pass


class RidersAdmin(admin.ModelAdmin):
    pass


class TripsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Establishments, EstablishmentsAdmin)
admin.site.register(Transactions, TransactionsAdmin)
admin.site.register(Riders, RidersAdmin)
admin.site.register(Trips, TripsAdmin)
