from django.contrib import admin
from reversion.admin import VersionAdmin

from hack.models import Category, Hack, Deployment, Repo, Commit, Version

class DeploymentInline(admin.TabularInline):
    model = Deployment

class HackAdmin(VersionAdmin):

    save_on_top = True
    search_fields = ("title",)
    list_filter = ("category","repo")
    list_display = ("title", "created", )
    date_hierarchy = "created"
    inlines = [
        DeploymentInline,
    ]
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "category", "repo", "repo_url", "usage", "created_by", "last_modified_by")
        }),
        ("Pulled data", {
            "classes": ("collapse",),
            "fields": ("repo_description", "repo_watchers", "repo_forks", "repo_commits", "participants")
        }),
    )

class CommitAdmin(VersionAdmin):
    list_filter = ("hack",)


admin.site.register(Category, VersionAdmin)
admin.site.register(Hack, HackAdmin)
admin.site.register(Repo, VersionAdmin)
admin.site.register(Commit, CommitAdmin)
admin.site.register(Version, VersionAdmin)
