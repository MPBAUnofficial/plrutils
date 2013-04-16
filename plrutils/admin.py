from django.contrib import admin
from plrutils.models import GraphFunction, Database


class GraphFunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'params', 'database', 'id')
    readonly_fields = ('id',)

admin.site.register(GraphFunction, GraphFunctionAdmin)
admin.site.register(Database)