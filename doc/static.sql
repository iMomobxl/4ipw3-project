DROP TABLE IF EXISTS `t_static`;
CREATE TABLE IF NOT EXISTS `t_static` (
  `id_sta` int NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `title_sta` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `url_sta` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_sta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_sta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT into `t_static` (`id_sta`, `title_sta`, `url_sta`, `content_sta`)
VALUES (1, 'A propos', 'about',
        '<p class="h1 text-primary text-center mb-3">Application "Site de presse" <br>
<i>Mohamed Ali Bacha</i> et <i>Mehdi Soltan</i></p>
        <p class="h2">Setup et installation:</p>
        <p>Voir <a href="https://github.com/iMomobxl/4ipw3-project">README.md</a></p>
        <br>
        <hr>
        <br>
        <p class="h2">Liste des pages:</p>
        <ol class="list-group list-group-numbered">
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Acceuil/Home
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/home/">/home/</a></h6>
            </li>
            <p>Affiche les articles de la categorie "on n''est pas des pigeons" (max 9 pour respecter le layout de la maquette)</p>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Recherche/Search
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/recherche/">/recherche/</a></h6>
            </li>
            <div class="px-5">
            <h5>Option de recherche:</h5>
            <ul>
                <li class="h6">Par mot dans le titre</li>
                <li class="h6">Par mot dans le hook</li>
                <li class="h6">Par mot dans le contenu</li>
                <li class="h6">Par date</li>
                <li class="h6">Par catégorie</li>
                <li class="h6">Par readtime (minimum 1 par defaut)</li>
            </ul>
            <h5>Option d''affichage:</h5>
            <ul>
                <li class="h6">Nombre d''article á afficher, par palier de 10</li>
                <li class="h6">Ajout d''un bouton Max qui desactive l''option precedente</li>
                <li class="h6">Ordre croissant/decroissant par date</li>
            </ul>
            </div>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Favoris
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/favoris/">/favoris/</a></h6>
            </li>
            <p>Liste des favoris de CHAQUES utilsateur logé</p>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Liste de date
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/date_list/">/date_list/</a></h6>
            </li>
                <p> Affiche dans une liste les dates disponible, avec les articles correspondant a cette date.</p>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                About
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/about/">/about/</a></h6>
            </li>
                <p>La page about va chercher dans la DB (table t_static) son contenu.</p>
                <p>Possibilité de modifier son contenu dans la page <a href="/user/">/user/</a> en tand que Admin</p>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Login
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/login/">/login/</a></h6>
            </li>
            <p>Pour se connecter en tand que User ou Admin</p>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                User
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/user/">/user/</a></h6>
            </li>
            <p>Page personnel pour les preferences d''affichage (detail voir section fonctionnalité)</p>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Sponsors
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/sponsors/">/sponsors/</a></h6>
            </li>
            <p>Affiche les eventuels sponsors</p>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Erreur 404
                <h6 class="ms-auto p-2 bd-highlight align-middle"></h6>
            </li>
            <p>Affiche une page "personnalisé" en cas d''erreur dans l''url</p><p>Exemple: <a href="/ceci_est_un_test_url/">/ceci_est_un_test_url/</a></p>
        </ol>
        <br>
        <hr>
        <br>
        <p class="h2 pt-3">Les fonctionnalités ajouté/imposé</p>
        <ol class="list-group list-group-numbered">
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Base de donnée Mysql
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/test-mysql/">/test-mysql/</a></h6>
            </li>
            <ul>
            <li>a connection se fait sur une DB mysql (exterieur: WAMP, LAMP, MAMP, autre...)</li>
                <li>La page <a href="/test-mysql/">/test-mysql/</a> affiche les tables presente dans la DB ainsi que leur propriete.</li>
            <li>Voir fichier .src/Press/settings.py pour les informations de connection</li>
            </ul>
            <br>
             <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Panier d''article favoris
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/favoris/">/favoris/</a></h6>
            </li>
            <ul>
                <li>Ajout d''un favoris: /favoris/add/[id_art]</li>
                - Verifie si le l''article est bien dans la table t_article
                <br>
                - Verifie si l''article n.est pas deja present dans le "panier" <a href="/favoris/">/favoris/</a>
                <li>Suppression d''un favoris: /favoris/del/[id_art]</li>
                - Verifie si l''article se trouve bien dans le panier favoris
                <br>
                - Verifie dans la DB pas necessaire car il a ete verifier au moment de l''ajout.
                <li>Liste des favoris de chaques utilsateur: /favoris/</li>
                - Possibilité de selectionner plusieurs articles á supprimer
                <li>Nous avons decidé qu''un utilisateur DOIT être logé pour pouvoir rajouter des articles dans son panier.<br>
                - Des boutons "Ajout Favoris" et "Supprimer Favoris" ont été rajouté à chaques article consulté
            (par exemple: <a href="/article/5578">/article/5578</a>)</li>
                <li>La sauvegarde des favoris se fait par les COOKIES (voir <a href="/user/">/user/</a> en tand que Admin)</li>
                <li>La stucture des cookies a été implementer de cette maniere:
                <br>[ { ''name'': ''id_article'' }, { ''name'': ''id_article'' }, ... ]
                <br>ainsi nous pouvons différentier les favoris de chaques utilisateur enregistré/logé par son nom.
                </ul>
            <br>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Formulaire de recherche
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/user/">/recherche/</a></h6>
            </li>
                <p>Choix imposé:</p>
                <ul>
                    <li class="h6">Recherche d''articles par : readtime min max (cursor)</li>
                </ul>
                <p>Contenu supplémentaire</p>
                <ul>
                    <li class="h6">Bouton reset : retire les valeurs du formulaire (refresh)</li>
                    <li class="h6">Bouton Max : désactive le champ "Nombre d''article" et affiche tout les resultats obtenue</li>
                    <li class="h6">Fonction Javascript (eventListener) qui indique la valeur du curseur ReadTime en direct</li>
                    <li class="h6">Lorsque le résultat de la recherche est null, les valeurs de la recherche sont conservé pour pouvoir pauffiner la recherche (en cas d''erreur de faute de frappe par exemple)</li>
                    <li>Requete SQL dans la fonction pour recherche le MIN/MAX dans la DB t_article ainsi que la liste des articles pour le formulaire</li>
                </ul>
            <br>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Identification (API)
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/login/">/login/</a></h6>
            </li>
            <ul>
                <li>Requete API sur <a href="https://playground.burotix.be/login/?login=admin&passwd=admin">Burotix</a></li>
                <li>Enregistre les valeurs des cles: identified, name et role dans des variables session de meme nom.</li>
            </ul>
            <br>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Menu de navigation: fichier csv
            </li>
            <ul>
                <li class="h6">Dossier src/app/asset/menu.csv</li>
                <li class="h6">Fonction dans context_processors.py</li>
                <li class="h6">Le fichier se compose de (id|name|access), l''option access a ete rajouté pour l''affichage du menu en fonction de l''utilisateur logé (tout le monde n''a pas acces a tout sauf l''admin evidement)</li>
            </ul>
            <br>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                System de messagerie à la navbar
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/sponsors/">/sponsors/</a></h6>
            </li>
            <ul>
                <li>Vert (Success) en cas de succes de l''operation demandé </li>
                <li>Jaune (Warning) en cas d''erreur</li>
            </ul>
            <br>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Option de presentation: Modification de la font-color/border
                <h6 class="ms-auto p-2 bd-highlight align-middle">Lien: <a href="/user/">/user/</a></h6>
            </li>
            <p>Choix imposé:</p>
            <ul>
                <li class="h6">4 choix possibles: Noir (par défaut), bleu, rouge et vert</li>
                <li class="h6">3 choix possibles: None (par défaut), thin et thick</li>
            </ul>
            <p>Contenu supplementaire:</p>
            <ul>
                <li class="h6">Choix de la catégorie á afficher: par défaut "on n''est pas des pigeons"</li>
                <li class="h6">Gestion en cas d''erreur de chargement d''image: script javascript <a href="/static/app/js/imageNotFound.js">imageNotFound.js</a></li>
            </ul>
            <p>(voir: <a href="/user/">/user/</a> Vous devez être logé!)</p>
            <br>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Manipulation des données JSON (API)
            </li>
            <ul>
                <li class="h6">Requete API sur: <a href="http://playground.burotix.be/adv/banner_for_isfce.json">Burotix/Banner</a></li>
                <li class="h6">Ajout d''une classe "sponsor" dans style.css</li>
                <li class="h6">Possibiliter d''afficher plusieurs banniere (en fonction de la reponse API)</li>
                <li class="h6">Affichage de la réponse API (en mode Admin uniquement!)</li>
            </ul>
            <br>
            <li class="d-flex bd-highlight list-group-item h3 font-weight-bold pb-0 ps-3">
                Source des pages statiques: Database
            </li>
            <p>Une table t_static a ete crée avec les champs:</p>
            <ul>
                <li class="h6">id_sta : id unique / primary key</li>
                <li class="h6">title_sta : Titre de la page static</li>
                <li class="h6">url_sta : le nom de l''url</li>
                <li class="h6">content_sta : le contenu de la page static</li>
            </ul>
            <p>Il est possible de modifier directement le contenu de la page about dans <a href="/user/">/user/</a> (vous devez etre logé en tand qu''admin)</p>
            <br>
        </ol> ');
