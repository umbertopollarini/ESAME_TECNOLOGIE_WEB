from django.test import TestCase
from .models import Prodotti
from .models import Categorie
from pathlib import Path
import os
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class URLTests(TestCase):
    def setUp(self):
        self.img = SimpleUploadedFile(name='test_image.jpg', content=open("media/61LujmgHXiS._AC_SX679__bfNsVWf.jpg", 'rb').read(), content_type='image/jpeg')
        self.forn = User.objects.create(username="user", email='user@gmail.com', password="Adminpsw1")
        self.cat = Categorie.objects.create(nome = "prova")
        self.obj = Prodotti.objects.create(fornitore=self.forn, immagine=self.img, titolo='testprova', categoria = self.cat, scheda_tecnica= "prova", prezzo = 10)
    
    #test raggiungibilità pagina di home
    def testhomepage(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
    
    #test raggiungibilità pagina di login
    def testloginpage(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
    
    #test raggiungibilità pagina di registrazione
    def testregisterpage(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    #test raggiungibilità pagina di creazione prodotto
    def testaddproductpage(self):
        response = self.client.get('/addproduct/', follow=True)
        self.assertEqual(response.status_code, 200)
    
    #test raggiungibilità pagina di aggiornamento prodotto
    def testupdateproductpage(self):
        response = self.client.get('/updateproduct/' + str(self.obj.id), follow=True)
        self.assertEqual(response.status_code, 200)
    
    #test raggiungibilità pagina di recap di admin
    def testadminrecappage(self):
        response = self.client.get('/list/0', follow=True)
        self.assertEqual(response.status_code, 200)

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.group = Group(name="Fornitore")
        self.group.save()

        basedir = Path(__file__).resolve().parent.parent
        self.pth = os.path.join(basedir, 'media')

        self.cat = Categorie.objects.create(nome = "prova")
        self.image = SimpleUploadedFile(name='prova.jpg', content=open(self.pth + "/61LujmgHXiS._AC_SX679__bfNsVWf.jpg", 'rb').read(), content_type='image/jpeg')

        self.fornitore = User.objects.create(username="user", email='user@gmail.com')
        self.fornitore.groups.add(self.group)
        self.fornitore.set_password("123456789")
        self.fornitore.save()

        self.fornitore2 = User.objects.create(username="acquistatore", email='acquistatore@gmail.com')
        self.fornitore2.groups.add(self.group)
        self.fornitore2.set_password("123456789")
        self.fornitore2.save()

        self.logged_in = self.client.login(username="user", password="123456789")

        self.obj = Prodotti.objects.create(fornitore=self.fornitore, immagine=self.image, titolo='testprova', categoria = self.cat, scheda_tecnica= "prova", prezzo = 10)
        self.obj2 = Prodotti.objects.create(fornitore=self.fornitore2, immagine=self.image, titolo='testprova', categoria = self.cat, scheda_tecnica= "prova", prezzo = 10)

        self.prodotto_url = reverse("addproduct")
        self.recensioneprodotto_url = reverse("addrecensione", args = [self.obj2.id])
        self.recensionefornitore_url = reverse("addrecensionefornitore", args = [self.fornitore2.id])

        

    def testrecensioneprodottosenza_testo(self):
        response = self.client.post(self.recensioneprodotto_url, {
            'stelle' : "4",
        }, follow = True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/addrecensione.html')

    def testrecensioneprodottosenza_voto(self):
        response = self.client.post(self.recensioneprodotto_url, {
            'descrizione' : "prova",
        }, follow = True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/addrecensione.html')

    def testrecensionefornitoresenza_testo(self):
        response = self.client.post(self.recensioneprodotto_url, {
            'stelle' : "6",
        }, follow = True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/addrecensione.html')

    def testrecensionefornitoresenza_voto(self):
        response = self.client.post(self.recensioneprodotto_url, {
            'recensione' : "prova",
        }, follow = True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/addrecensione.html')

    def testinserimentoprodottosenza_immagine(self):
        response = self.client.post(self.prodotto_url, {
            'titolo' : "prova",
            'scheda_tecnica' : "prova",
            'categoria' : self.cat,
            'quantità' : "100",
            'prezzo' : "100"
        }, follow = True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/addproduct.html')

    def testinserimentoprodottosenza_titolo(self):
        response = self.client.post(self.prodotto_url, {
            'immagine' : self.image,
            'scheda_tecnica' : "prova",
            'categoria' : self.cat,
            'quantità' : "100",
            'prezzo' : "100"
        }, follow = True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/addproduct.html')

    def testinserimentoprodottosenza_categoria(self):
        response = self.client.post(self.prodotto_url, {
            'titolo' : "prova",
            'immagine' : self.image,
            'scheda_tecnica' : "prova",
            'quantità' : "100",
            'prezzo' : "100"
        }, follow = True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/addproduct.html')

    def testinserimentoprodottosenza_quantità(self):
        response = self.client.post(self.prodotto_url, {
            'titolo' : "prova",
            'immagine' : self.image,
            'categoria' : self.cat,
            'scheda_tecnica' : "prova",
            'prezzo' : "100"
        }, follow = True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/addproduct.html')

    def testinserimentoprodottosenza_scheda_tecnica(self):
        response = self.client.post(self.prodotto_url, {
            'titolo' : "prova",
            'immagine' : self.image,
            'categoria' : self.cat,
            'quantità' : "100",
            'prezzo' : "100"
        }, follow = True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/addproduct.html')

    def testinserimentoprodottosenza_prezzo(self):
        response = self.client.post(self.prodotto_url, {
            'titolo' : "prova",
            'immagine' : self.image,
            'categoria' : self.cat,
            'quantità' : "100",
            'scheda_tecnica' : "prova",
        }, follow = True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/addproduct.html')