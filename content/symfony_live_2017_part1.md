Title: Retour sur le Symfony Live Paris 2017 - Jour 1
Date: 2017-04-13 09:00
Category: Events
Tags: Symfony, PHP
Authors: Jérémy Fournaise

![SymfonyLive 2017 - Isics]({filename}/images/sflive2017_01.png)

La 9e édition du SymfonyLive Paris avait lieu les 30 et 31 mars 2017 à la Cité Internationale Universitaire de Paris.

Deux jours de conférences techniques, retours d'expériences et présentations de produits en rapport avec l'écosystème Symfony... Nous n'allons pas vous le cacher c'est un moment qu'on attend chez Isics (d'autant plus qu'on est **partenaire SensioLabs**) ! Une partie de l'équipe a donc naturellement fait le déplacement.

Qu'y avait-il à retenir sur la première journée de l'événement ?


## Symfony4

C'est sans surprise Fabien Potencier en personne qui a démarré cette journée de conférences avec notamment deux sujets :

### Symfony4 (sans blague !)

* Ca arrive bientôt ! (fin novembre 2017)
* PHP7 requis
* Dans la continuité de Symfony3, l'architecture se rapproche encore plus des standards de linux (répertoire etc pour stocker les fichiers de configuration, fichier .env pour gérer les variables d'environnement / ...)
* Les composants embarqués par défaut dans les versions précédentes sont maintenant optionnels - on part d'une version minimaliste (template symfony/skeleton) et on ajoute simplement ce dont on a besoin

### Symfony Flex

Le constat est simple : quelle est la valeur ajoutée lors de l'installation ou désinstallation d'un bundle ? On doit activer le bundle via le AppKernel.php, charger dans certains cas des routes supplémentaires, ajouter de la configuration ...

L'objectif de Symfony Flex est de faire tout ça pour vous. Il fonctionne via un plugin composer et propose :

* L'installation / désinstallation automatisée des bundles via un système de recettes
* La mise en place d'alias pour simplifier l'installation de bundles. Certains bundles seront sélectionnés par Sensio (ex : un composer require admin vous proposera directement le bundle EasyAdmin)

L'installation des bundles sans recette sera, bien sûr, toujours possible.

![SymfonyLive 2017 - Vlouppe / Spacefoot]({filename}/images/sflive2017_02.png)


## A la découverte du composant Serializer

Grégoire Pineau rappelle le principe de la sérialisation avant de passer au vif du sujet : le composant symfony/serializer.

Son constat : avant Symfony 2.7 le composant serializer de Symfony n'était pas utilisé. D'autres solutions telles que le JMSSerializer étaient bien plus complètes. Kevin Dunglas (notamment) a voulu inverser la tendance et a repris le composant en main.

Au final :

* Le composant reste limité comparé à JMS mais inclus la base nécessaire à la majorité des cas
* Plus léger donc plus rapide
* Plus simple d'utilisation (à vérifier...)

Mais :

* Sérialisation des erreurs pas intégrée de base (pour bientôt, PR en cours)
* Gestion des références circulaires : l'implémentation d'un handler est indispensable. Même si celle-ci a été fortement simplifiée depuis la 3.3 (merci @lyrixx) on aurait aimé quelque chose de plus transparent (comme le propose JMS).

En savoir plus : [https://speakerdeck.com/lyrixx/symfony-live-2017-serializer](https://speakerdeck.com/lyrixx/symfony-live-2017-serializer)


## Grâce aux tags Varnish, j'ai switché ma prod sur un Raspberry Pi

Jérémy Derussé nous fait la promesse suivante : switcher une app Symfony qui absorbe 1000 requêtes/seconde sur un serveur à 10$.

Il faut donc faire en sorte que le back-end ne soit plus appelé. Pour cela on ne précise plus de durée de vie sur les caches mais on s'arrange pour purger le cache de manière intelligente via une notion de tags.

En clair on peut s'arranger via des listeners pour tagger chaque resource lors de leur création / modification. Un article aura par exemple pour tag :

* Article-#ID
* Auteur-#ID
* Commentaire-#ID
* Commentaire-#ID2
* ...

Lors du flush d'une entité, on va s'arranger pour vider les caches possédants ce tag.

Cette solution a quelques limites :

* certains cas sont plus complexes à gérer : listings paginés / création d'entités / relation vide mise en cache ...
* ne fonctionne que si le nombre de HIT est bien plus important que le nombre de MISS
* ne fonctionne que pour de la lecture

En savoir plus : [https://www.slideshare.net/JrmyDeruss/grce-aux-tags-varnish-jai-switch-ma-prod-sur-raspberry-pi](https://www.slideshare.net/JrmyDeruss/grce-aux-tags-varnish-jai-switch-ma-prod-sur-raspberry-pi)


## JWT - Sécurisez vos APIs

André Tapia a ensuite abordé JWT (JSON Web Token). Il s'agit d'une solution d'authentification / sécurisation de web services basée sur un token sécurisé.

Pourquoi utiliser JWT ?

* Stateless
* Plus simple à mettre en place que le protocole Oauth
* Sécurisé

Le token est composé de 3 parties :

* Header : algorithme à utiliser / le type (JWT)
* Payload : propriétés (sub / exp / name / roles / ...)
* Signature : header et payload encodés en base 64, le tout chiffré avec l'algorithme choisi

Ainsi le header de chaque requête / réponse peut contenir un ensemble de données (via le payload), le tout de manière sécurisée (la signature sert à contrôler l'intégrité, mais bien penser au HTTPS !), et ainsi nous éviter de faire des requêtes supplémentaires pour contrôler les rôles d'un utilisateur par exemple.


Et l'intégration dans un projet Symfony ?

Long exemple d'utilisation de JWT via le composant Guard.
Pas forcément utile quand on voit les bundles existants à côté (ex : lexik/LexikJWTAuthenticationBundle / gesdinet/JWTRefreshTokenBundle)

En savoir plus : [https://fr.slideshare.net/AndrTapia/jwt-scurisez-vos-apis](https://fr.slideshare.net/AndrTapia/jwt-scurisez-vos-apis)


## Micro-Services Symfony chez Meetic : retour d'expérience après 2 ans de refonte

Nous avons déjà eu l'occasion de voir Etienne Broutin lors du Symfony Live 2015 pour la conférence "Meetic backend mutation with Symfony". Quel était l'objectif de cette refonte ? Découper leur API monolithique en micro-services Symfony.

Il revient deux ans plus tard pour faire un bilan sur ce projet.

Meetic c'est maintenant :

* 25 micro-services
* données isolées dans un micro-service
* pas de versionning des micro-services, cela implique que chaque modification doit être rétro compatible
* 100 serveurs et 1 milliard d'appels aux micro-services par jour

Intêret des micro-services pour Meetic ?

* Reprise / partage de micro-services entre différents projets : Meetic Affinity, scout24, ...
* Prise en main simplifiée pour les dévs : un micro-service peut être repris / compris en 1 à 2 jours par un développeur
* Déploiement continu : 15 mise en production par jour
* Meilleur appropriation du code / du projet par les développeurs


## Utiliser Webpack dans une application Symfony

Pour sa première conférence Alain Hippolyte nous explique comment intégrer Webpack a un projet Symfony2 (bye bye Assetic !).

Bonne présentation même si on pourrait lui reprocher de ne pas avoir assez mis en évidence la différence entre Webpack et les tasks runners tels que Gulp & Grunt.
De la même manière il aurait pu aborder l'une des forces de Webpack à savoir le chargement intelligent des dépendances.

En savoir plus : [https://www.slideshare.net/alainhippolyte1/utiliser-webpack-dans-une-application-symfony](https://www.slideshare.net/alainhippolyte1/utiliser-webpack-dans-une-application-symfony)


## Introduction to CQRS and Event Sourcing

![SymfonyLive 2017 - CQRS / Event Sourcing]({filename}/images/sflive2017_03.png)

Samuel Roze nous a introduit (huhu) au pattern CQRS (Command Query Responsibility Seggregation) et à l’event sourcing.

En gros, plutôt que de stocker de manière classique nos objets dans leur état final, nous allons plutôt stocker l'ensemble des événéments ayant eu lieu dans la vie de l'objet. Il suffira ensuite de rejouer ces différents événements pour reconstituer l'objet.

Concept très intéressant mais quelques réserves...

* Quid des objets avec beaucoup d'actions ? Risque de lenteurs ?!
* Comment sont gérer les suppressions ?
* Adaptable selon moi à des types de projets très limités

En somme introduction au CQRS et Event Sourcing intéressant mais aurait nécessité un peu plus d'exemples / cas concrets.


## Quoi de neuf dans Symfony depuis un an ?

Sarah Khalil intervient pour le dernier talk de la journée. Petit tour d'horizon des nouveautés depuis 1 an.

A noter :

* `SYMFONY__` déprécié - il faut maintenant utiliser `%env()%`
* Composer maintenant en charge du ClassLoader (merci PHP7 !)
* Simplification de l'autowiring
* Récupération des messages flash simplifiée
* Amélioration du composant Workflow
* Désormais possible de rechercher directement dans le contenu d'un dump()
* Nouveau data collector : cache
* Implémentation de la PSR-16 (cache)
* Possibilité maintenant d'utiliser le FQCN d'une classe comme id de service
* L'utilisation de pattern désormais possible pour charger un ensemble de fichiers de configuration
* 2 nouveaux composants : Lock & Dotenv
* Mise en place de features @experimental

Une bonne séance de rattrapage pour ceux qui ne suivent pas le blog Symfony !

En savoir plus : [https://speakerdeck.com/saro0h/symfonylive-paris-quoi-de-neuf-depuis-1-an](https://speakerdeck.com/saro0h/symfonylive-paris-quoi-de-neuf-depuis-1-an)

<br>

La journée s'est achevée par un apéritif avec la communauté.
De la bière et des chouettes rencontres, que demander de plus !


[A suivre ...](https://blog.isics.fr/retour-sur-le-symfony-live-paris-2017-jour-2.html)