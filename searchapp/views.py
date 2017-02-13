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

def static2(request):
	pattern = "*.txt"
	i = 0
	if request.method == "POST":
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
			return HttpResponseRedirect(reverse('search'))
	else:
		form = PostForm()
	return render(request, 'skenerdirektorija.html', {'form': form})

def static1(request):
	# ovdje dodajem jako veliki broj, da prepoznam dodavane fajlove naknadno, pri tome pretpostavljam da klijent nema vise fajlova od navedene jednakosti!
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




def search(request):
	if request.method == "POST":
		username = request.POST['rijec']
		print username


	return render(request, 'search.html')


