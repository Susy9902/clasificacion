from django.contrib import admin

# Register your models here.

from system.models import DB_global,DB_grupos, DB_objetos, DB_objetos_rasgos, DB_rasgo_dominio, DB_rasgos


admin.site.register(DB_rasgos)
admin.site.register(DB_global)
admin.site.register(DB_grupos)
admin.site.register(DB_objetos)
admin.site.register(DB_objetos_rasgos)
admin.site.register(DB_rasgo_dominio)

