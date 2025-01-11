# 4IPDW
# Projet de Developpement WEB
## 1 - Setup:
- python: v3.13.1
- pip: v24.3.1
- django: v5.1.4
### Verifier les versions:
```bash
python --version
pip --version
python -m django --version
```
## 2 - Creation/Activation de l'environnement virtuel:
### - Creation:
```
python3 -m venv .env
```
### - Sourcer l'environnement:
```bash
source .env/bin/activate
```
### - Verifier l'environnement virtuel
```bash
which python

[...path...]/.env/bin/python
```
### - Desactivation de l'environnement virtuel (ne pas executer):
```bash
deactivate
```
## 3 - Installation/mise a jour
#### - pip:
```bash
pip install --upgrade pip
```
#### - django:
```bash
pip install -r requirements.txt
```
## 4 - Verifier les settings
Aller dans **./src/Press/settings.py**
- *Ligne 26*: (garder DEBUG á True car toujours en developpement)
>DEBUG=True
- *Ligne 28*: 
Rajouter les eventuels host autorisé
>ALLOWED_HOSTS=['localhost', '127.0.0.1'] 
- *Ligne 88 à 99*: Verifier les informations de connection à la DB (WAMP/MAMP/LAMP)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'press_2024_v03',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306', 
    }
}
```
## 5 - Lancement serveur
Se trouver dans le dossier src
```bash
cd src
```
Demarrer serveur
```bash
python3 manage.py runserver
```
Acceder au site via http://127.0.0.1:8000
## 6 - DB et media
### Source github: 
#### - Ajout de la table t_static: Chercher le fichier ./doc/static.sql et executer sur phpmyadmin
#### - Les image sont deja dans le repo: ./src/static/media
### Source Moodle/isfce:
#### - Ajout de la table t_static: Chercher le fichier ./doc/static.sql et executer sur phpmyadmin
#### - placer les fichier images dans: ./src/static/media
## 7 - Lien utile:
- [github 4ipw3](https://github.com/iMomobxl/4ipw3-project.git)
- [doc django](https://docs.djangoproject.com/fr/5.1/)
- [localhost admin django](http://127.0.0.1:8000/admin) login: admin - passwd: admin
- [tuto1](https://www.synbioz.com/blog/tech/image-placeholder)