from django.contrib import admin
from reversion.admin import VersionAdmin

from grid.models import Element, Feature, Grid, GridHack

class GridHackInline(admin.TabularInline):
    model = GridHack
    
class GridAdmin(VersionAdmin):
    inlines = [
        GridHackInline,
    ]

admin.site.register(Element, VersionAdmin)
admin.site.register(Feature, VersionAdmin)
admin.site.register(Grid, GridAdmin)
admin.site.register(GridHack, VersionAdmin)
