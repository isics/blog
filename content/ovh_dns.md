Title: Migrer 100 zones DNS chez OVH en 5 minutes
Date: 2017-01-09 10:00
Category: DevOps
Tags: OVH, API, Python
Authors: Nicolas Charlot

**UPDATE 09/01/2017 15h00 : ajout de la purge des secondaires**

Chez [Isics](http://www.isics.fr) on développe des sites depuis bientôt 13 ans et on les héberge aussi.
Nous avons commandé notre premier serveur dédié chez OVH en 2005. A l'époque le use case classique pour le hosting était d'opter pour la fameuse "release OVH". En gros un système prêt à l'emploi avec Apache, MySQL, PHP mais aussi un certain **Bind**.

On a tendance à préférer le sur mesure au prêt à porter. Du coup on a continué depuis toutes ces années à utiliser Bind. Il faut bien avouer que la valeur ajoutée n'est pas fulgurante ! Disposer de son propre serveur DNS offre certes des possibilités supplémentaires (avoir des logs par exemple) mais dans la majorité des cas d'utilisation, l'intérêt n'est pas évident. D'autant plus que comme tout service, il faut configurer oui mais il faut surtout maintenir en conditions opérationnelles... Bind a son lot de failles de sécurité et il faut veiller au grain pour passer les update rapidement.

A côté de ça, on est client chez OVH depuis 13 ans donc (3 chiffres dans notre nic-handle et ouais :)), et on a à disposition gratuitement leurs NS qui sont rapides, sécurisés, maintenus, redondés et facile à configurer via le manager et il y a mieux encore...

On a donc décidé de sortir le service DNS de notre infra et de tout migrer sur les NS d'OVH.

Sage décision ! Oui mais voilà on a plus de 100 zones DNS customizées actives. En tant que devs qui se respectent, la paresse est une de nos qualités. Hors de question de faire ça la mano. Alors on fait quoi chef ?


## L'API OVH à la rescousse (presque) !

Je vous avais bien dit qu'il y avait mieux encore !
L'API d'OVH permet aujourd'hui de piloter pratiquement tous leurs services : cloud, emails, téléphonie et bien entendu noms de domaines.

Ca sentait bon pour nous cette histoire. On adore ça les API chez [Isics](http://www.isics.fr) et [Spacefoot](http://spacefoot.com), et à toutes les sauces !
Sauf qu'il y a un hic :( (Il y a toujours un hic non ?) Hélas la documentation est super light et les méthodes laissent parfois dubatitifs tant dans leur prototype que dans leurs réponses.

Par exemple on s'aperçoit qu'il y a (au moins) 3 façons de voir les NS d'un nom de domaine :

    :::console
    GET /domain/zone/{zoneName}
    GET /domain/zone/{zoneName}/record/{id}
    GET /domain/{serviceName}/nameServer

Bon ok je suis mauvaise langue car il y a la zone d'un côté et les NS associés au domaine de l'autre. Là où ça devient perturbant c'est qu'il nous est arrivé d'obtenir des résultats divergeants sur les 3 méthodes...

Autre point noir : OVH ne fournit pour l'heure pas d'assistance sur ses API. On a quand même tenté quelques tickets et on a eu des bribes de réponses, mais souvent imprécises et avec un lag énorme (plusieurs semaines de balotage au final).

La seule façon d'obtenir une aide précieuse s'est avérée être la mailing-list [api@ml.ovh.net](mailto:api@ml.ovh.net). A propos je tiens à remercier particulièrement Eric Vergne sans qui nous n'aurions probablement pas pu aboutir.

Bon au final on ne vous a pas menti : on a bien migré nos 100 zones en quelques minutes :)
Avant d'y parvenir, on s'est creusé quelques heures...


## Authentification

On commence par s'identifier.
A ce niveau, [le guide d'OVH](https://www.ovh.com/fr/g934.premiers_pas_avec_lapi) fait le job.

Pour faire bref, on commence par obtenir les clés de l'appli [via ce formulaire](https://eu.api.ovh.com/createApp/).

Ensuite on demande un token d'authentification avec les accès qui vont bien.
Dans notre cas on va demander l'accès aux méthodes `GET`, `POST` et `PUT` sur le chemin `/domain/*` :

Via cURL ça donne :

    :::console
    $ curl -XPOST -H"X-Ovh-Application: VOTRECLEAPPLI" -H "Content-type: application/json" \
    https://eu.api.ovh.com/1.0/auth/credential  -d '{
        "accessRules": [
            {
                "method": "GET",
                "path": "/domain/*"
            },
            {
                "method": "POST",
                "path": "/domain/*"
            },
            {
                "method": "PUT",
                "path": "/domain/*"
            },
        ],
        "redirection":"https://www.onsenfou.com/"
    }

L'API doit vous redonner une réponse de ce genre :

    :::json
    {
        "validationUrl": "https://eu.api.ovh.com/auth/?credentialToken=PATATIPATATA",
        "consumerKey": "VOTRETOKEN",
        "state": "pendingValidation"
    }

Il ne reste plus qu'à rattacher ce token à votre identifiant client. Pour ce faire RDV sur l'URL `validationUrl` indiquée dans la réponse.

Cette fois on y est. On rentre dans le terrier du lapin blanc !


## Installation du client

On va utiliser le wrapper Python officiel développé par OVH. Son code source est dispo [sur Github](https://github.com/ovh/python-ovh).

Je vous épargne la création du VirtualEnv. On installe donc directement le client OVH via Pip :

    :::console
    $ pip install ovh

Par défaut, le client cherchera une conf dans le dossier local au sein du fichier `ovh.conf`.
On va donc le créer en y reportant les clés obtenues précédemment :

    :::config
    [default]
    endpoint=ovh-eu

    [ovh-eu]
    application_key=VOTRECLEAPPLI
    application_secret=VOTRECLESECRETEAPPLI
    consumer_key=VOTRETOKEN


## Premier appel

Ecrivons un premier script listant les noms de domaines que l'on gère :

    :::python
    import ovh

    client = ovh.Client()
    for domain in client.get('/domain'):
        print(domain)

Si tout va bien vous devez obtenir la liste de vos domaines :

    :::console
    mondomaine1.fr
    mondomaine1.com
    ...

On stockera cette liste dans un fichier `manager.txt` pour la suite du programme.

Notez qu'OVH met aussi à disposition un client web de son API : [https://api.ovh.com/console/](https://api.ovh.com/console/). C'est bien pratique pour se mettre au parfum des prototypes des méthodes (paramètres notamment) et pour jouer avec.


## Passons aux choses sérieuses

A présent que les connaissances sont faites, rentrons dans le vif du sujet.

### 1. Récupérer la liste des domaines à migrer

En 13 ans on en a vu passer des noms de domaines. Certains n'existent plus, d'autres ne sont plus gérés par nos soins.
Commençons donc par repérer les domaines actifs sur notre Bind.

D'abord listons tous les domaines gérés :

    :::console
    $ ls -1 /var/bind/pri | grep .hosts | cut -d. -f-2 > bind.txt

Regardons à présent quels domaines utilisent notre serveur. On va se faire un petit script Shell pour ça  :

    :::shell
    #!/bin/sh

    for DOMAIN in `cat $2`
    do
        dig -t NS +short $DOMAIN | grep -q $1 && echo $DOMAIN
    done

On lui passe l'adresse de notre serveur, et le fichier contenant les noms de domaines à checker. Ainsi :

    :::console
    $ ./using_ns.sh monserveur.tld bind.txt > to_migrate.txt

Et on obtient la liste des serveurs réellement actifs.

_Remarque : préférez lancer cette commande hors du serveur lui-même car il s'utilise certainement lui-même pour résoudre._


Enfin regardons quels domaines ne sont pas gérés par OVH :

    :::console
    $ comm -23 to_migrate.txt manager.txt

On a ici la liste des noms de domaines non gérés par OVH.
Ca peut paraître délicat si OVH ne le gère pas et que nous n'en voulons plus non plus mais il n'en n'est rien !
Et oui ils sont quand même sympas chez OVH. On peut maintenant gérer les zones DNS de noms de domaines dont il ne sont même pas registrar !

Importez donc à la main les éventuels absents dans votre manager OVH (Domaines / Ajouter une zone DNS) :

![Ajouter une zone DNS]({filename}/images/screenshot_add_zone.png)

Bien entendu il faudra par la suite mettre les NS d'OVH au niveau de leurs registrars respectifs (Amen, Gandi, etc.).



### 2. Activation des zones DNS

Allez back to Python !

On va maintenant activer les zones DNS des domaines à migrer :

    :::python
    with open('to_migrate.txt') as fp:
        for line in fp:
            domain = line.strip()
            client.post('/domain/{}/activateZone'.format(domain))


### 3. Récupération des NS OVH

OVH commence a avoir quelques serveurs :)
Chaque nom de domaine est ainsi associé à 2 NS.

Pour les récupérer :

    :::python
    ovh_ns = client.get('/domain/zone/{}'.format(domain))['nameServers']

Ca s'est compliqué pour certains noms de domaines chez nous où cette liste était vide.

Du coup un petit reset de la zone a sauvé la mise :

    :::python
    ovh_ns = client.get('/domain/zone/{}'.format(domain))['nameServers']
    if len(ovh_ns) < 2:
        client.post('/domain/zone/{}/reset'.format(domain), minimized=False)
        ovh_ns = client.get('/domain/zone/{}'.format(domain))['nameServers']


### 4. Import de la zone

Au préalable copiez toutes les zones de votre bind dans un dossier `zones`.

Tout d'abord on remplace les NS dans la zone par ceux d'OVH que l'on a récupérés :

    :::python
    import re

    zone = open('zones/{}.hosts'.format(domain)).read()
    for i, old_ns in enumerate(re.findall('IN\s+NS\s+(.*)$', zone, re.MULTILINE)):
        zone = zone.replace(old_ns, ovh_ns[i]+'.')

Ensuite on demande l'import de cette zone. C'est un process asynchrone chez OVH. Le premier appel API nous retourne un identifiant de tâche. On va checker tous les 10 secondes si elle est terminée ou non.

    :::python
    import time

    task = client.post(
        '/domain/zone/{}/import'.format(domain),
        zoneFile=zone)
    while True:
        time.sleep(10)
        if client.get('/domain/zone/{}/task/{}'.format(domain, task['id']))['status'] == 'done':
            break


### 5. Modification des NS

La zone est en place. On peut basculer !

J'ai été tenté de penser que l'API permettant de passer sur des NS _"hosted"_ aurait fait le travail mais ce n'est pas simple...

C'est même l'inverse, il faut commencer par s'assurer que les NS sont en _"external"_ pour avoir le droit de les modifier ensuite :

    :::python
    client.put('/domain/{}'.format(domain), nameServerType='external')

Et donc on modifie les NS. Encore un petit cadeau à cette étape : l'API retourne une exception si les NS sont déjà bons :)

    :::python
    try:
        client.post('/domain/{}/nameServers/update'.format(domain), nameServers=[{'host': ns} for ns in ovh_ns])
    except ovh.exceptions.APIError as err:
        if str(err) != 'Name server are already good':
            raise err

Autre surprise possible, s'il existe des tâches passées en erreur sur ce domaine ou sur sa zone, l'API vous retournera une exception _"Our robot is working on your domain's DS records. Please wait"_. Ca c'est pas cool car ces tâches sont dans un statut définitif. On ne devrait pas être bloqué...

Qu'à cela ne tienne, on va supprimer ces tâches au préalable. Mais attention, on ne peut pas toutes les supprimer :)

    :::python
    tasks = client.get('/domain/{}/task'.format(domain), status='error')
    for task in tasks:
        client.post('/domain/{}/task/{}/cancel'.format(domain, task))

    tasks = client.get('/domain/zone/{}/task'.format(domain), status='error')
    for task in tasks:
        if client.get('/domain/zone/{}/task/{}'.format(domain, task))['function'] != 'DnssecEnable':
            client.post('/domain/zone/{}/task/{}/cancel'.format(domain, task))

Et ensuite ? Ben on repasse en "hosted" puisque c'est bien ce dont il s'agit :

    :::python
    client.put('/domain/{}'.format(domain), nameServerType='hosted')


### 6. Bonus : activer DNSSEC

Cerise on the cake, on va en profiter pour activer [DNSSEC](https://www.ovh.com/fr/domaines/service_dnssec.xml) :

    :::python
    client.post('/domain/zone/{}/dnssec'.format(domain))


## Never assume, always check!

Cette phrase n'est [pas de chez nous](https://www.blablacar.in/about-us/culture) mais on ne peut qu'adhérer, et à 100% !

A ce stade, OVH a en principe repris la main ou plutôt a commencé à reprendre la main. Et oui, n'oublions pas les fameux délais de propagation qui peuvent prendre jusqu'à plusieurs jours.

Pour surveiller que le plan s'est déroulé sans accroc, on peut vérifier différentes choses :

- Réutiliser notre petit script Shell pour s'assurer que notre ancien serveur n'est plus dans aucun NS
- Activer les logs de requête sur Bind et observer qu'elles disparaissent petit à petit
- Et bien entendu jeter un petit coup d'oeil sur le manager OVH, ça ne mange pas de pain !

Si vous aviez des noms de domaines non gérés par OVH, c'est maintenant que vous pouvez basculer les NS.


## Plus tard...

Plusieurs jours sont passés. Vous avez bien vérifié que toutes les requêtes étaient traitées par les NS d'OVH.

On va donc pouvoir remercier les serveurs secondaires :

    :::python
    server = 'VotreAncienNS'
    domains = client.get('/dedicated/server/{}/secondaryDnsDomains'.format(server))
    for domain in domains:
        client.delete('/dedicated/server/{}/secondaryDnsDomains/{}'.format(server, domain))
        print('Removed secondary DNS for {}'.format(domain))

## Share the love

Nos scripts Shell et Python [sont dispos ici](https://github.com/isics/ovh-api-scripts).

J'espère que ce post pourra débloquer certains sur l'API `domain` d'OVH.

**N'hésitez surtout pas à nous faire part de typos ou d'imprécisions. D'autant plus que ce billet et le premier. Il marque la naissance du blog technique co-brandé Spacefoot & Isics. A ce propos : on recrute [chez Isics](http://www.isics.fr/) ET [chez Spacefoot](http://www.spacefoot.com) !!**

Et bonne année bien sûr !