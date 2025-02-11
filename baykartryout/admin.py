from django.contrib import admin

# Register your models here.

from .models import Part, Assembly, UsedPart

admin.site.register(Part)
admin.site.register(Assembly)
admin.site.register(UsedPart)