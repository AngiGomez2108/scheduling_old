from django.contrib import admin

# Register your models here.
from .models import Department, City, DocumentType, PersonType, Person, Place, Process, State, Citation, Functionary

admin.site.register(Department)
admin.site.register(City)
admin.site.register(DocumentType)
admin.site.register(PersonType)
admin.site.register(Person)
admin.site.register(Place)
admin.site.register(Process)
admin.site.register(State)
admin.site.register(Citation)
admin.site.register(Functionary)