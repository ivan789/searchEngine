#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import subprocess
from fnmatch import fnmatch
from .forms import PostForm, PostForm2, searchWeb
from django.core.urlresolvers import reverse
import sys
import re
from algoritam import Algoritam
import copy




''' 
	Ova funkcija skenira predani direktorij i subdirectory i trazi sve dokumente u njemu,
	funkcija kao argument prima ime direktorija i to kroz web formu, te pravi dakle indexiranje za cijeli direktorij i
	njegove poddirektorije! Funkcija za svaki dokument zapisuje sljedece:
	<title>README.txt</title>
	<text>
	Roboto webfont source: https://www.google.com/fonts/specimen/Roboto
	Weights used in this project: Light (300), Regular (400), Bold (700)
	</text>
	</page>
	<page>
	<id>489</id>, nakon toga kreira indexe za svaku rijec i naslov, te na posljetku na osnovu indexa
	moguce napraviti pretrazivanje cijelog direktorija, i to tako da ovaj search engine vraca same indexe ili
	rijeci, ovisno koju kombinaciju primjenite, kako je navedeno u README dokumentu!
'''
def static2(request):
	pattern = "*.txt"
	i = 0
	if request.method == "POST":
		try:
			form = PostForm(data=request.POST)
			if form.is_valid():

				my_file = 'MojaKolekcijaFajlova.dat'
				my_file2= 'indexi.dat'
				my_file3= 'Index2option.dat'
				my_file4= 'naslovIndex.dat'
				if os.path.isfile(my_file):
					os.remove("MojaKolekcijaFajlova.dat")
				if os.path.isfile(my_file2):
					os.remove("indexi.dat")
				if os.path.isfile(my_file3):
					os.remove("Index2option.dat")
				if os.path.isfile(my_file4):
					os.remove("naslovIndex.dat")

				direkt = form.cleaned_data['dokument']
				direktorij =str('/')+direkt
				print direktorij
				
				for path, subdirs, files in os.walk(str(direktorij)):
					for name in files:
						if fnmatch(name, pattern):
							print os.path.join(path, name)
							with open(os.path.join(path, name)) as f:
								i += 1
								with open("MojaKolekcijaFajlova.dat", "a") as f1:
									f1.write("<page>\n")
									f1.write("<id>" + str(i) + "</id>\n")
									f1.write("<title>" + str(name) + "</title>\n")
									f1.write("<text>\n")
									for line in f:
										f1.write(line)
									f1.write("</text>\n")
									f1.write("</page>\n")
				if os.path.isfile(my_file):
					os.system("python kreirajIndex.py eliminiramRijeci.dat MojaKolekcijaFajlova.dat indexi.dat")
					os.system("python kreiranjeIDIndexa.py eliminiramRijeci.dat MojaKolekcijaFajlova.dat Index2option.dat naslovIndex.dat")
				#return HttpResponseRedirect(reverse('search'))
		except:
			print 'Error tijekom parsanja fajlova!'
	else:
		form = PostForm()
	return render(request, 'skenerdirektorija.html', {'form': form})

''' 
	Ova funkcija sluzi za dodavanje indexiranje naknadno dodanih fajlova, tj
	ako smo vec prije pokrenuli indexiranje i ne zelimo ponovno pokretati indexiranje za sve dokumente koje smo 
	prethodno indexirali nego samo za ove novododane, tada pozivamo na frontendu ovu funkciju kroz formu, i to tako da joj predamo 
	ime fajla i funkcija ce npraviti indexe samo za taj novo dodani fajl, a ova veliki u samoj funkciji je postavljen kako
	neki id od kojeg pocinje brojanje novododanih fajlova!

'''
def static1(request):
	
	i = 100000000
	if request.method == "POST":
		form = PostForm2(data=request.POST)
		if form.is_valid():
			fajl = form.cleaned_data['fajl']
			print fajl
			if os.path.isfile(fajl):
				with open(fajl) as f:
					i += 1
					with open("MojaKolekcijaFajlova.dat", "a") as f1:
						f1.write("<page>\n")
						f1.write("<id>" + str(i) + "</id>\n")
						f1.write("<title>" + str(fajl) + "</title>\n")
						f1.write("<text>\n")
						for line in f:
							f1.write(line)
						f1.write("</text>\n")
						f1.write("</page>\n")


		return HttpResponseRedirect(reverse('dokumenti'))
	else:
		form = PostForm2()

	return render(request, 'dokumenti.html', {'form': form})


''' 
	Ova funkcija sluzi za primanje onoga sto je korisnik predao u search formu,
	a ovo je ostavljeno da korisnik sam sebi po zelji definira na koji nacin ce raditi engine,
	dakle sto ce mu se kao rezultat pretraživanja vracati indexi ili rijeci, dakle ima mogucnost
	da odabere jednu od dvije moguce opcije prilozenu u opisu README! (Dakle ostavljeno
	da korisnik sam odabere i definira kako zeli da mu radi engine!)
'''

def search(request):

	if request.method == "POST":
		word = request.POST['test']
		print word	
	return render(request, 'search.html')


