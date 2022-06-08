from cmath import log
from math import prod
import re
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.db.models import Q

from .forms import CreateUserForm
from .forms import ProductForm
from .forms import RecensioniForm
from .forms import VenditaForm
from .forms import RecensioniFornitoreForm
from .forms import MyCheckBox

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from json import dumps
from .models import Prodotti
from .models import Recensioni
from .models import Vendite
from .models import RecensoniFornitori
from .models import BlackList
from .models import Categorie
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che utilizzo per controllare se un utente è fornitore o meno
def user_check(user):
    return user.groups.filter(name='Fornitore').exists()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che utilizzo per vedere se un utente è un admin
def user_check_admin(user):
    return user.groups.filter(name='Admin').exists()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la visualizzazione e le richieste post alla pagina di login
def loginPage(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            messages.info(request, "Username o Password incorretto")
            return render(request, 'ecommerce/login.html', context)
    
    return render(request, 'ecommerce/login.html', context)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la visualizzazione e le richieste post alla pagina di registrazione dell'acquirente
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            register_user = form.save(commit=False)
            register_user.save()
            
            fornitori_group = Group.objects.get(name='Acquirente')
            register_user.groups.add(fornitori_group)

            user = form.cleaned_data.get('username')
            messages.success(request, 'Account creato con successo ' + user)
            return redirect(loginPage)

    context = {'form': form}
    return render(request, 'ecommerce/register.html', context) 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la visualizzazione e le richieste post alla pagina di registrazione del fornitore
def registerPageFornitore(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            register_user = form.save(commit=False)
            register_user.save()
            
            fornitori_group = Group.objects.get(name='Fornitore')
            register_user.groups.add(fornitori_group)

            user = form.cleaned_data.get('username')
            messages.success(request, 'Account creato con successo ' + user)
            return redirect(loginPage)
    context = {'form': form}
    return render(request, 'ecommerce/register.html', context) 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la richiesta di logout
def logoutUser(request):
    logout(request)
    return redirect(home)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la visualizzazione e le richieste post di ricerca della pagina di home
def home(request):
    products = Prodotti.objects.all()
    product = sorted(products, key=lambda x: x.media_valutazione, reverse=True)
    form = MyCheckBox(request.POST or None)
    if request.method == "POST":
        form = MyCheckBox(request.POST or None)
        if form.is_valid():
            if request.POST.get("prezzo", False):
                product = sorted(products, key=lambda x: x.prezzo, reverse=True)
                context = {
                    "ricercati" : "Prezzo",
                    "products" : product,
                    'form':form
                }
                return render(request, 'ecommerce/index.html', context)
            else : 
                product = sorted(products, key=lambda x: x.media_valutazione, reverse=True)
                context = {
                    "ricercati" : "",
                    "products" : product,
                    'form':form
                }

    return render(request, 'ecommerce/index.html', {'products': product, 'form':form})
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la visualizzazione delle vendite ad un fornitore, i decoratori mi servono per controllare che l'utente loggato sia un fornitore e che si sia effettivamente loggati
@user_passes_test(user_check, login_url = loginPage)
@login_required(login_url=loginPage)
def vendite(request):
    user = User.objects.get(pk=request.user.id)
    vendite = Vendite.objects.filter(fornitore = user)
    return render(request, 'ecommerce/vendite.html', {'vendite': vendite})
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la richiesta di aggiunta di un prodotto, i decoratori servono a controllare che si è un fornitore e che si sia loggati
@user_passes_test(user_check, login_url = loginPage)
@login_required(login_url=loginPage)
def addProduct(request):
    form = ProductForm()
    user = User.objects.get(pk=request.user.id)        

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            bbb = form.save(commit=False)
            bbb.fornitore = user
            bbb.save()
            return redirect(home)

    if user.last_name == "stop" or user.last_name == "delete":
        messages.info(request, "A causa delle tue recensioni personali come fornitore non ti è più consentito pubblicare articoli")
        flag = 1
    else : flag = 0

    context = {
        "form":form,
        "flag":flag
    }
        
    return render(request, 'ecommerce/addproduct.html', context)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la visualizzazione e le richieste post alla pagina di dettagli del prodotto
def productDetail(request, id):
    form = VenditaForm()
    product = Prodotti.objects.get(id = id)
    recensioni = Recensioni.objects.filter(prodotto = product)
    recensionifornitori = RecensoniFornitori.objects.filter(fornitore = product.fornitore)
    prodraccomandati = list()
    prodall = list()

    #Se user è autenticato allora fa system raccomandation
    if request.user.is_authenticated:
        user_acquisto = User.objects.get(pk=request.user.id)
        user_fornitore = User.objects.get(id=product.fornitore.id)
        product = Prodotti.objects.get(pk=id)

        #System raccomandation: se A compra X e B ha comprato X e Y, ad A mostro Y
        acquisti_user = Vendite.objects.filter(acquistatore = request.user) #tutti acquisti dell'utente loggato
        if len(acquisti_user) != 0 : #ha acquistato almeno un prodotto 
            prodraccomandati = list()
            for acquisto in acquisti_user: #per ogni acquisto
                prodottovendite = Vendite.objects.filter(Q(prodotto_venduto = acquisto.prodotto_venduto) & ~Q(acquistatore = request.user))  #lista delle vendite di quel prodotto
                for prodottovendita in prodottovendite:
                    objs = Vendite.objects.filter(Q(acquistatore = prodottovendita.acquistatore) & ~Q(prodotto_venduto = prodottovendita.prodotto_venduto)) #lista delle vendite dei prodotti acquistati da un acquistatore che ha acquistato anche il prodotto
                    prodraccomandati.extend(objs) 
        
        #tolgo i doppioni
        for prod in prodraccomandati:
            if prod.prodotto_venduto not in prodall : prodall.append(prod.prodotto_venduto)
        
        #rimuovo l'articolo corrente se è tra i consigliati
        if product in prodall : prodall.remove(product)

    if request.method == 'POST':
        form = VenditaForm(request.POST)
        if form.is_valid():
            bbb = form.save(commit=False)
            if bbb.quantità > product.quantità : 
                messages.info(request, "Quantità sel. maggiore del disponibile")
            else :
                bbb.acquistatore = user_acquisto
                bbb.fornitore = user_fornitore
                bbb.prodotto_venduto = product
                product.quantità -= bbb.quantità
                product.venduti += bbb.quantità
                if product.quantità == 0: product.disponibile = False
                product.save()
                bbb.save()
                messages.info(request, "Hai acquistato " + str(bbb.quantità) + " articoli con successo")

    context = {
        "data" : product,
        "recensioni" : list(recensioni),
        "form":form,
        "recensionifornitore":recensionifornitori,
        "productraccomandation" :prodall
    }

    return render(request, 'ecommerce/productdetail.html', context)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la richiesta di aggiunta di una recensione di un prodotto
@login_required(login_url=loginPage)
def addRecensione(request, id):
    form = RecensioniForm()
    prod = Prodotti.objects.get(pk=id) #oggetto prod
    user = User.objects.get(pk=request.user.id) #oggetto user che fa recensione
    if prod.fornitore.id == user.id : return redirect(loginPage) #nel caso in cui il fornitore del prodotto provi a farsi una autovalutazione del prodotto

    if request.method == 'POST':
        form = RecensioniForm(request.POST)
        if form.is_valid():
            bbb = form.save(commit=False)
            bbb.prodotto = prod
            bbb.user_recensione = user
            bbb.save()

            #aggiorno media del prodotto
            recensioni = Recensioni.objects.filter(prodotto = prod)
            somma = 0
            media = 0
            for recensione in recensioni:
                somma = somma + recensione.stelle
            media = somma / len(recensioni)
            prod.media_valutazione = format(media, ".1f")
            prod.save()
            messages.info(request, "Hai inserito la recensione con successo.")
        else : messages.info(request, "Si sono verificati dei problemi, recensione non inserita")
    context = {
        "form":form
    }
    return render(request, 'ecommerce/addrecensione.html', context)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la richiesta di update del prodotto, i decoratori servono a controllare che si è un fornitore e che si sia loggati
@user_passes_test(user_check, login_url = loginPage)
@login_required(login_url=loginPage)
def updateProduct(request, id):
    product = Prodotti.objects.get(pk=id)
    form = ProductForm(instance = product)
    user = User.objects.get(pk=request.user.id)
    if product.fornitore.id != user.id : return redirect(loginPage)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            bbb = form.save(commit=False)
            if bbb.quantità > 0 : bbb.disponibile = True
            bbb.save()
            return redirect(home)
    context = {
        "form":form
    }
    return render(request, 'ecommerce/updateproduct.html', context)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la richiesta di delete del prodotto
def deleteProduct(request, id):
    product = Prodotti.objects.get(pk=id)
    user = User.objects.get(pk=request.user.id)
    if product.fornitore.id != user.id : return redirect(loginPage)
    product.delete()
    return redirect(home)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la richiesta ricerca dalla barra di ricerca nella home, le corrispondenze sono oltre che per titolo anche per categoria e fornitore
def ricerca(request):
    if request.method == 'POST':
        ricercati = request.POST['ricercati']
        totval = list()
        form = MyCheckBox(request.POST or None)

        #corrispondenza valori dal titolo
        valori = Prodotti.objects.filter(titolo__contains=ricercati)
        totval.extend(valori)

        #corrispondenza valori dalle categorie
        categorie = Categorie.objects.filter(nome__contains=ricercati)
        for cat in categorie:
            prodcat = Prodotti.objects.filter(categoria = cat)
            totval.extend(prodcat)
        
        #corrispondenza valori dal fornitore
        fornitore = User.objects.filter(username__contains=ricercati)
        for forn in fornitore:
            prodforn = Prodotti.objects.filter(fornitore = forn)
            totval.extend(prodforn)
        

        context = {
            "ricercati" : ricercati,
            "products" : totval,
        }
        return render(request, 'ecommerce/index.html', context)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la richiesta di aggiunta di una recensione per un fornitore, mi fa anche il check nel caso di aggiunta nella blacklist
@login_required(login_url=loginPage)
def addRecensioneFornitore(request, id):
    form = RecensioniFornitoreForm()
    user = User.objects.get(pk=request.user.id) # oggetto user che fa recensione
    fornitore = User.objects.get(pk=id) # oggetto fornitore che subisce recensione
    if fornitore.id == user.id : 
        return redirect(loginPage) # nel caso in cui il fornitore provi a farsi una autovalutazione

    if request.method == 'POST':
        form = RecensioniFornitoreForm(request.POST)
        if form.is_valid():
            bbb = form.save(commit=False)
            bbb.fornitore = fornitore
            bbb.user_recensione = user
            bbb.save()

            # calcolo media punteggio del fornitore
            recensioni = RecensoniFornitori.objects.filter(fornitore = fornitore)
            somma = 0
            media = 0
            for recensione in recensioni:
                somma = somma + recensione.stelle
            media = somma / len(recensioni)
            
            if media > 4:
                fornitore.last_name = "go"
                # dare possibilità di pubblicare articoli
            if media > 2 and media <= 4 and len(recensioni) >= 5:
                fornitore.last_name = "stop"
                # stoppare possibilità di pubblicare articoli
            if media >= 0 and media <= 2 and len(recensioni) >= 5:
                BlackList.objects.create(user = fornitore)

                fornitore.last_name = "delete"
                # gli articoli e il fornitore vengono eliminati e username inserito in una blacklist

            fornitore.first_name = format(media, ".1f")
            fornitore.save()
            messages.info(request, "Hai inserito la recensione con successo.")
        else : messages.info(request, "Si sono verificati dei problemi, recensione non inserita")

    context = {
        "form":form
    }
    return render(request, 'ecommerce/addrecensione.html', context)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# metodo che mi gestisce la richiesta di visualizzazione delle liste di utenti per l'amministratore
@user_passes_test(user_check_admin, login_url = loginPage)
@login_required(login_url=loginPage)
def adminlist(request, id):
    if id == 0 : 
        list = BlackList.objects.all()
        filter = "Blacklist Fornitori"
    if id == 1 : 
        list = User.objects.filter(groups__name='Acquirente')
        filter = "Lista Acquirenti"
    if id == 2 : 
        list = User.objects.filter(groups__name='Fornitore')
        filter = "Lista Fornitori"
    context = {
        "list":list,
        "filter":filter
    }
    return render(request, 'ecommerce/list.html', context)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -