from django.contrib import admin

from reservations.models import Avail, Table, Reservation, Timestart


admin.site.register(Avail)
admin.site.register(Table)

admin.site.register(Reservation)
admin.site.register(Timestart)

