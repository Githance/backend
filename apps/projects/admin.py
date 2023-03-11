from django.contrib import admin

from .models import Project, ProjectStatus, ProjectType

admin.site.register(ProjectStatus)
admin.site.register(ProjectType)


class ProjectTypeInline(admin.TabularInline):
    model = Project.types.through
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (ProjectTypeInline,)
