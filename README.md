#Installazione Applicazione Web

###Segui questa guida per la corretta installazione
Per utilizzare questa webapp è necessario aver installato python (testato da 3.8+). Suggerisco di usare virtualenv (o altro equivalente), se non ce l'hai, puoi installarlo con il tuo gestore di pacchetti. Per me su MacOs con bash, sarà qualcosa del genere:

`pip install virtualenv`

Ora puoi creare la tua virtualenv

`virtualenv <nome_virualenv>`

Ora devi attivarla

`source <nome_virualenv>/bin/activate`

Nella cartella dell'applicazione web avvia il comando per installare tutti i pacchetti

`(<nome_virualenv>) pip install -r requirements.txt`

Se hai fatto tutto correttamente adesso potrai avviare il server con 

`python manage.py runserver`

oppure 

`(<nome_virualenv>) python manage.py runserver`

Per accedere all'applicazione web dirigiti su : 

`http://127.0.0.1:8000/home/`

oppure su 

`http://localhost:8000/home/`