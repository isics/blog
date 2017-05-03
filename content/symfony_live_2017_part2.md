Title: Retour sur le Symfony Live Paris 2017 - Jour 2
Date: 2017-05-02 09:15
Category: Events
Tags: Symfony, PHP
Authors: Julien Pottier

Vous avez pu lire notre retour sur cette [première journée du Symfony Live](https://blog.isics.fr/retour-sur-le-symfony-live-paris-2017-jour-1.html) bien remplie. Revenons à présent sur le jour 2. C'est parti !

## Qui veut gagner une carrière de développeur ?

Première présentation sous forme de jeu pour bien commencer la journée ! Thomas GX (commitstrip) nous a bien fait rire en revenant sur des sujets polémiques du développement web (temps de développement, troll sur la meilleure techno ou encore les workflows pas toujours simples à mettre en place).

Un très bon début de journée pour se remettre de la soirée précédente ;)

![SymfonyLive 2017 - Isics]({filename}/images/sflive2017_04.jpg)

*photo issue du compte Twitter du [SymfonyLive](https://twitter.com/symfony_live)*


## Architecture Inutile ?

En lisant le titre, vous avez sûrement envie de répondre "non !" (enfin j'espère). Heureusement Jérôme Vieilledent ne s'est pas arrété à cette réponse évidente et nous a montré que l'architecture ça compte et qu'on a eu un long périple pour en arriver où on en est.

On est d'abord passé par un code "spaghetti" ("je mets ce code ici, parce que pourquoi pas...").
Puis un code "lasagne" ("je mets ce code ici, parce que c'est sa place").
Pour finir actuellement sur une tendance de code "ravioli" ("je mets ce code ici parce que c'est son rôle").

De grands principes (qu'il est nécessaire de respecter) ont été mis en place pour arriver à ce genre d'architecture, tels que :

* S.O.L.I.D. : **S**ingle Responsibility Principle **O**pen/Closed principle **L**iskov substitution principle **I**nterface seggregation principle **D**ependency Inversion Principle
* K.I.S.S : **K**eep **I**t **S**tupidly **S**imple
* ou encore D.R.Y. : **D**on't **R**epeat **Y**ourself

Jerôme nous a illustré ce manque d'architecture par un cas concret sur lequel il a dû intervenir. Un code ultra monolitique, difficile à comprendre et quasiment impossible à modifier sans connaitre le fonctionnement complet et les cas limites.
La refactorisation l'a emmené d'une classe à plus d'une vingtaine, mais chacune ayant un rôle unique, le tout étant mieux maintenable et évolutif.

![SymfonyLive 2017 - Isics]({filename}/images/sflive2017_05.jpg)

*photo issue du compte Twitter du [SymfonyLive](https://twitter.com/symfony_live)*

En savoir plus : [https://speakerdeck.com/lolautruche/architecture-inutile](https://speakerdeck.com/lolautruche/architecture-inutile)

## Déployer une app Symfony dans un PaaS

Le principe du PaaS (Platform As A Service) est de construire une application fonctionnelle depuis notre base de code, et de façon automatique.

Tristan Darricau nous démontre que ce n'est pas aussi simple que ça. En effet, pour avoir une application fonctionnelle il faut connaitre l'architecture matérielle nécessaire ainsi que les différents accès aux services tiers (mots de passes / clé d'API, base de données...). Il est donc nécessaire de passer par une phase de build avant de lancer notre exécutable.

Le build se reposera sur la description de l'infrastructure présente dans le code ainsi que des variables d'environnement afin de définir des valeurs de configuration nécessaires à nos services.

En savoir plus : [https://speakerdeck.com/nicofuma/symfony-live-paris-2017](https://speakerdeck.com/nicofuma/symfony-live-paris-2017)

## Sécurité web : et si on continuait à tout casser ?

Alain Tiemblo nous a expliqué comment se prémunir d'attaques qui permettraient à des pirates de subtiliser des informations sensibles.

Que ce soit par DDOS ou simplement par Injection SQL, la nature de ce qui peut être dérobé (des mots de passe ou directement de l'argent) nous conforte dans l'idée que la sécurité n'est pas à prendre à la légère.

Certains algorithmes de hashage (le SHA-1 par exemple), encore largement utilisé dans le milieu professionnel, ne sont plus considérés comme sûrs car il est possible de trouver une autre source qui aurait la même valeur hashée.

Alain illustre ce problème de sécurité avec un exemple concret chez BlaBlaCar : les remboursements. Un pirate qui obtiendrait l'accès à votre compte pourrait se faire rembourser votre argent sur son propre compte PayPal.

Il faut donc bien veiller à la sécurité de la connexion (HTTPS / authentification sur 2 facteurs...) si on ne veut pas voir fuiter ces informations sur la toile !

## Créer des WebApps modernes avec Symfony, ReactJS et API Platform

C'est sans surprise Kévin Dunglas qui nous a présenté une façon rapide de concevoir des API : API Platform (v2).

Avec ce framework (basé sur Symfony), il suffit de décrire les modèles de données et on se retrouve avec une API REST dont les réponses respectent les spécifications JSON-LD et Hydra.

Attention toutefois, ces API sont orientées ressources et non services (car générées sur les modèles justement).

Chez Isics, on avait testé API Platform v1 et les performances nous avaient laissés dubitatif. A retester donc !

En savoir plus : [https://dunglas.fr/2017/04/api-platform-2-1-when-symfony-meets-reactjs-symfony-live-2017/](https://dunglas.fr/2017/04/api-platform-2-1-when-symfony-meets-reactjs-symfony-live-2017/)

## Tout ce qu’un dev devrait savoir à propos d’Unicode

Nicolas Grekas nous a ensuite présenté Unicode. On ne va pas se mentir, Unicode, on l'utilise tous, mais on sait peu tout ce qu'implique ce format de représentation des caractères et la compléxité qu'elle cache !

Entre les caractères présents dans une seule langue (ß), les caractères combinés (œ, Ú, les emojis...) ou encore les caratères ayant une forte ressemblance ("i" majuscule et "l"), la comparaison de chaînes informatiques et visuelles peut avoir des résultats très différents et peut vite devenir un casse-tête !

Nicolas a su titiller notre intérêt avec un sujet qui paraissait simple, et pourtant... fort intéressant !

![SymfonyLive 2017 - Isics]({filename}/images/sflive2017_06.jpg)

*photo issue du compte Twitter du [SymfonyLive](https://twitter.com/symfony_live)*

En savoir plus : [https://speakerdeck.com/nicolasgrekas/tout-ce-quun-dev-devrait-savoir-a-propos-dunicode](https://speakerdeck.com/nicolasgrekas/tout-ce-quun-dev-devrait-savoir-a-propos-dunicode)

## Optimisations de performances avec PHP7

Étant présent à la SymfonyCon Paris 2015, on avait déjà eu un avant goût des optimisations apportées à PHP7, là aussi présentées par Julien Pauli.

A l'époque PHP7 en était à ses tous débuts. Depuis on a pu constater cette grande amélioration de performances sur nos différents projets.

Au menu de ces optimisations :

* Le compilateur utilise maintenant un AST (Abstract Syntax Tree)
* Les structures de données natives contiennent 2x moins de pointeurs (saut mémoire)
* les tableaux statiques (clés entières ordonnées de façon croissante) sont traités lors de la phase de compilation

La compilation en PHP7 est donc bien plus lente et complexe qu'en PHP5.6. Cependant l'utilisation d'OPCache permet de compiler plus rarement et de profiter des optimisations sur le temps d'exécution (et la consommation mémoire).

A noter au niveau des versions de PHP :

* PHP 7.2 sortira en fin d'année 2017
* PHP 5 ne sera plus maintenu à partir du 31 décembre 2018 *(security support étendu d'un an)*
* PHP 8 ne sortira pas avant 2020

*(source [http://php.net/supported-versions.php](http://php.net/supported-versions.php))*

![SymfonyLive 2017 - Isics]({filename}/images/sflive2017_07.jpg)

*photo issue du compte Twitter du [SymfonyLive](https://twitter.com/symfony_live)*

En savoir plus : [https://www.slideshare.net/jpauli/symfony-live-2017php7performances](https://www.slideshare.net/jpauli/symfony-live-2017php7performances)
