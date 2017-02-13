# -*- coding: utf-8 -*-
from django import forms

class PostForm(forms.Form):
    dokument = forms.CharField(label='Upišite ime direktorija', max_length=100)

class PostForm2(forms.Form):
    fajl = forms.CharField(label='Upišite puno putanju s imenom dokumenta (npr. /home/test.txt)', max_length=100)

class searchWeb(forms.Form):
    rijec = forms.CharField(max_length=100)