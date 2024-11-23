from django.contrib import admin

# Register your models here.

from gestion.models.person import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
