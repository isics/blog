#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Isics'
SITENAME = 'blog.isics.fr'
SITEURL = 'http://localhost:8000/'

THEME = 'themes/flex'

PATH = 'content'

TIMEZONE = 'Europe/Paris'


SITETITLE = 'blog.isics.fr'
SITESUBTITLE = 'Le blog technique d\'Isics'
SITEDESCRIPTION = 'Le blog technique d\'Isics'
MAIN_MENU = False
FAVICON = '/images/favicon.ico'
SITELOGO = '/images/table_ping_pong.jpg'
DISQUS_SITENAME = 'blog-isics'

STATIC_PATHS = ['css', 'images']
CUSTOM_CSS = 'css/custom.css'

# Default theme language.
I18N_TEMPLATES_LANG = 'en'
DEFAULT_LANG = 'fr'
LOCALE = 'fr_FR'
OG_LOCALE = 'fr_FR'

JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}


PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['i18n_subsites']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('à propos', 'http://www.isics.fr/'),)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/isicsfr'),
          ('facebook', 'https://www.facebook.com/isicsfr'),
          ('github', 'https://github.com/isics/'),)

DEFAULT_PAGINATION = False

MENUITEMS = (('Catégories', '/categories.html'),
             ('Tags', '/tags.html'),
             ('Auteurs', '/authors.html'),
             ('Archives', '/archives.html'),)

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


SUMMARY_MAX_LENGTH = 200

CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version': '4.0',
    'slug': 'by-sa'
}


AUTHORS_INFOS = {
    'jeremy-fournaise': {
        'image': '/images/jeremy-fournaise.png',
        'role': 'Chef de projet web & mobile chez <a href="http://www.isics.fr" target="_blank">Isics</a>',
        'twitter': 'https://twitter.com/jfournaise'
    },
    'nicolas-charlot': {
        'image': '/images/nicolas-charlot.png',
        'role': 'Co-fondateur & CEO <a href="http://www.isics.fr" target="_blank">Isics</a>, Co-fondateur & CTO <a href="http://www.spacefoot.com" target="_blank">Spacefoot</a>',
        'twitter': 'https://twitter.com/ncharlot'
    }
}
