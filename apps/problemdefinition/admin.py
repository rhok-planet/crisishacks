from django.contrib import admin
from reversion.admin import VersionAdmin

from problemdefinition.models import Element, Feature, ProblemDefinition, ProblemDefinitionHack

class ProblemDefinitionHackInline(admin.TabularInline):
    model = ProblemDefinitionHack

class ProblemDefinitionAdmin(VersionAdmin):
    inlines = [
        ProblemDefinitionHackInline,
    ]

admin.site.register(Element, VersionAdmin)
admin.site.register(Feature, VersionAdmin)
admin.site.register(ProblemDefinition, ProblemDefinitionAdmin)
admin.site.register(ProblemDefinitionHack, VersionAdmin)
