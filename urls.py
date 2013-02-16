# -*- coding: utf-8 -*-  

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import views
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^$', direct_to_template, {'template': 'index.html'}),
    url(r'^talk/$', views.talk),
    url(r'^embed/$', views.embed),
    url(r'^commandments/$', direct_to_template, {'template': 'commandments.html', 'extra_context': {'subtitle': 'Commandments'}}),
    url(r'^factorial/$', direct_to_template, {'template': 'factorial.html', 'extra_context': {'subtitle': 'factorial'}}),
    url(r'^factorial-iter/$', direct_to_template, {'template': 'factorial-iter.html', 'extra_context': {'subtitle': 'factorial-iter'}}),
    url(r'^map/$', direct_to_template, {'template': 'map.html', 'extra_context': {'subtitle': 'map'}}),

    # chapter 1
    url(r'^car/$', direct_to_template, {'template': '1/car.html', 'extra_context': {'subtitle': 'car'}}),
    url(r'^cdr/$', direct_to_template, {'template': '1/cdr.html', 'extra_context': {'subtitle': 'cdr'}}),
    url(r'^cons/$', direct_to_template, {'template': '1/cons.html', 'extra_context': {'subtitle': 'cons'}}),
    url(r'^null/$', direct_to_template, {'template': '1/null.html', 'extra_context': {'subtitle': 'null?'}}),
    url(r'^atom/$', direct_to_template, {'template': '1/atom.html', 'extra_context': {'subtitle': 'atom?'}}),
    url(r'^eq/$', direct_to_template, {'template': '1/eq.html', 'extra_context': {'subtitle': 'eq?'}}),

    # chapter 2
    url(r'^lat/$', direct_to_template, {'template': '2/lat.html', 'extra_context': {'subtitle': 'lat?'}}),
    url(r'^member/$', direct_to_template, {'template': '2/member.html', 'extra_context': {'subtitle': 'member?'}}),

    # chapter 3
    url(r'^rember/$', direct_to_template, {'template': '3/rember.html', 'extra_context': {'subtitle': 'rember'}}),
    url(r'^firsts/$', direct_to_template, {'template': '3/firsts.html', 'extra_context': {'subtitle': 'firsts'}}),
    url(r'^insertR/$', direct_to_template, {'template': '3/insertR.html', 'extra_context': {'subtitle': 'insertR'}}),
    url(r'^insertL/$', direct_to_template, {'template': '3/insertL.html', 'extra_context': {'subtitle': 'insertL'}}),

    # chapter 4
    url(r'^add/$', direct_to_template, {'template': '4/add.html', 'extra_context': {'subtitle': '+'}}),
    url(r'^sub/$', direct_to_template, {'template': '4/sub.html', 'extra_context': {'subtitle': '-'}}),
    url(r'^mult/$', direct_to_template, {'template': '4/mult.html', 'extra_context': {'subtitle': '×'}}),
    url(r'^tupadd/$', direct_to_template, {'template': '4/tupadd.html', 'extra_context': {'subtitle': 'tup+'}}),
    url(r'^gt/$', direct_to_template, {'template': '4/gt.html', 'extra_context': {'subtitle': '>'}}),
    url(r'^lt/$', direct_to_template, {'template': '4/lt.html', 'extra_context': {'subtitle': '<'}}),
    url(r'^eq2/$', direct_to_template, {'template': '4/eq2.html', 'extra_context': {'subtitle': '='}}),
    url(r'^expt/$', direct_to_template, {'template': '4/expt.html', 'extra_context': {'subtitle': '↑'}}),
    url(r'^div/$', direct_to_template, {'template': '4/div.html', 'extra_context': {'subtitle': '÷'}}),
    url(r'^length/$', direct_to_template, {'template': '4/length.html', 'extra_context': {'subtitle': 'length'}}),
    url(r'^pick/$', direct_to_template, {'template': '4/pick.html', 'extra_context': {'subtitle': 'pick'}}),
    url(r'^rempick/$', direct_to_template, {'template': '4/rempick.html', 'extra_context': {'subtitle': 'rempick'}}),
    url(r'^no-nums/$', direct_to_template, {'template': '4/no-nums.html', 'extra_context': {'subtitle': 'no-nums'}}),

    # chapter 5
    url(r'^rembers/$', direct_to_template, {'template': '5/rembers.html', 'extra_context': {'subtitle': 'rember*'}}),

    # chapter 6
    url(r'^add2/$', direct_to_template, {'template': '6/add2.html', 'extra_context': {'subtitle': '+'}}),  
    url(r'^numbered/$', direct_to_template, {'template': '6/numbered.html', 'extra_context': {'subtitle': 'numbered?'}}),  
    url(r'^value/$', direct_to_template, {'template': '6/value.html', 'extra_context': {'subtitle': 'value'}}),  
    url(r'^value2/$', direct_to_template, {'template': '6/value2.html', 'extra_context': {'subtitle': 'value2'}}),  

    # chapter 7
    url(r'^set/$', direct_to_template, {'template': '7/set.html', 'extra_context': {'subtitle': 'set?'}}),
    url(r'^makeset/$', direct_to_template, {'template': '7/makeset.html', 'extra_context': {'subtitle': 'makeset'}}),
    url(r'^subset/$', direct_to_template, {'template': '7/subset.html', 'extra_context': {'subtitle': 'subset?'}}),
    url(r'^intersect/$', direct_to_template, {'template': '7/intersect.html', 'extra_context': {'subtitle': 'intersect'}}),
    url(r'^union/$', direct_to_template, {'template': '7/union.html', 'extra_context': {'subtitle': 'union'}}),
    url(r'^xxx/$', direct_to_template, {'template': '7/xxx.html', 'extra_context': {'subtitle': 'xxx'}}),
    url(r'^a-pair/$', direct_to_template, {'template': '7/a-pair.html', 'extra_context': {'subtitle': 'a-pair?'}}),
    url(r'^fun/$', direct_to_template, {'template': '7/fun.html', 'extra_context': {'subtitle': 'fun?'}}),

    # chapter 8
    url(r'^rember-f/$', direct_to_template, {'template': '8/rember-f.html', 'extra_context': {'subtitle': 'rember-f'}}),  
    url(r'^eq-c/$', direct_to_template, {'template': '8/eq-c.html', 'extra_context': {'subtitle': 'eq?-c'}}),  

    # chaptet 9
    url(r'^eternity/$', direct_to_template, {'template': '9/eternity.html', 'extra_context': {'subtitle': 'eternity'}}),  
    url(r'^will-stop/$', direct_to_template, {'template': '9/will-stop.html', 'extra_context': {'subtitle': 'will-stop?'}}), 
    url(r'^length1/$', direct_to_template, {'template': '9/length1.html', 'extra_context': {'subtitle': 'length1'}}),   
    url(r'^mk-length/$', direct_to_template, {'template': '9/mk-length.html', 'extra_context': {'subtitle': 'mk-length'}}),  
)
