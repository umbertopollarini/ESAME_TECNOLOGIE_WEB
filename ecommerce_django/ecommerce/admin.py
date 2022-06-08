from django.contrib import admin
from .models import Prodotti
from .models import Recensioni
from .models import Categorie
from .models import Vendite
from .models import RecensoniFornitori
from .models import BlackList

# Register your models here.
admin.site.register(Recensioni)
admin.site.register(Prodotti)
admin.site.register(Categorie)
admin.site.register(Vendite)
admin.site.register(RecensoniFornitori)
admin.site.register(BlackList)