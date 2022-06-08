"""ecommerce_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ecommerce import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls), #url pagina admin
    path('home/', views.home, name="home"), #url pagina home
    path('login/', views.loginPage, name="login"), #url pagina login utente
    path('register/', views.registerPage, name="register"), #url pagina registrazione Acquistatore
    path('registerfornitore/', views.registerPageFornitore, name="registerfornitore"),  #url pagina registrazione Fornitore
    path('logout/', views.logoutUser, name="logout"), #url richiesta di logout
    path('addproduct/', views.addProduct, name="addproduct"), #url pagina aggiunta prodotto
    path('vendite/', views.vendite, name="vendite"), #url richiesta delle vendite di un fornitore
    path('ricerca/', views.ricerca, name="ricerca"), #url richiesta di ricerca
    path('list/<int:id>', views.adminlist, name="list"), #url pagina dell'admin per visualizzare i gruppi
    path('updateproduct/<int:id>', views.updateProduct, name="updateproduct"), #url pagina di modifica prodotto
    path('deleteproduct/<int:id>', views.deleteProduct, name="deleteproduct"), #url pagina di eliminazione prodotto
    path('productdetail/<int:id>', views.productDetail, name="productDetail"), #url pagina per i dettagli del prodotto 
    path('addrecensione/<int:id>', views.addRecensione, name="addrecensione"), #url pagina per aggiunta recensione a prodotto
    path('addrecensionefornitore/<int:id>', views.addRecensioneFornitore, name="addrecensionefornitore"), #url pagina per aggiunta recensione al fornitore
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
