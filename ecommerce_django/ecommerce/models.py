from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Tabella che contiene le categorie
class Categorie(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

# Tabella che contiene i prodotti
class Prodotti(models.Model):
    id = models.AutoField(primary_key=True)
    fornitore = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    immagine = models.ImageField()
    venduti = models.IntegerField(default=0)
    titolo = models.CharField(max_length=20)
    categoria = models.ForeignKey(Categorie, on_delete=models.CASCADE, default="")
    disponibile = models.BooleanField(default=True)
    quantità = models.IntegerField(default=1)
    media_valutazione = models.FloatField(default=0)
    scheda_tecnica = models.CharField(max_length=2000)
    prezzo = models.FloatField()

    def __str__(self):
        return self.titolo

# Tabella che contiene le recensioni dei prodotti
class Recensioni(models.Model):
    id = models.AutoField(primary_key=True)
    prodotto = models.ForeignKey(Prodotti, on_delete=models.CASCADE, default="")
    user_recensione = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    stelle = models.FloatField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    descrizione = models.CharField(max_length=300)

    def __str__(self):
        return str(self.id)

# Tabella che contiene le vendite
class Vendite(models.Model):
    id = models.AutoField(primary_key=True)
    acquistatore = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_acquistatore' ,default="")
    fornitore = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_fornitore', default="")
    prodotto_venduto = models.ForeignKey(Prodotti, on_delete=models.CASCADE, default="")
    quantità = models.IntegerField(default=0)

    def __str__(self):
        return str(self.acquistatore.username)

# Tabella che contiene le recensioni dei fornitori
class RecensoniFornitori(models.Model):
    id = models.AutoField(primary_key=True)
    fornitore = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_fornitore', default="")
    user_recensione = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    recensione = models.CharField(max_length=300)
    stelle = models.FloatField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return str(self.fornitore.username)

# Tabella che contiene i fornitori con punteggio <= di 2
class BlackList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return str(self.user)
