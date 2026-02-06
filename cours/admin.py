
# Register your models here.
from django.contrib import admin
from .models import Cours, Enseignants, User, Paiement,Lecon,Section

admin.site.register(Cours)
admin.site.register(Enseignants)
admin.site.register(User)
admin.site.register(Paiement)
admin.site.register(Lecon)
admin.site.register(Section)