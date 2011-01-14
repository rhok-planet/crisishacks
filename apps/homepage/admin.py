from django.contrib import admin

from homepage.models import Dpotw, Gotw, Tab, ProblemTab

class ProblemTabAdmin(admin.ModelAdmin):

    list_display = ('problemdefinition', 'order', )
    list_editable = ('order', )

admin.site.register(ProblemTab, ProblemTabAdmin)

class TabAdmin(admin.ModelAdmin):

    list_display = ('grid', 'order', )
    list_editable = ('order', )

admin.site.register(Tab, TabAdmin)

admin.site.register(Dpotw)
admin.site.register(Gotw)
