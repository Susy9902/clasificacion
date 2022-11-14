from cProfile import Profile
from genericpath import exists
from operator import truediv
from tkinter import PROJECTING
from unicodedata import category, name
from urllib import response
from xml.dom.minidom import Document

from msilib.schema import Class

from django.test import TestCase, Client
from django.test import SimpleTestCase

from django.urls import reverse, resolve
from system.views.default import index, ayuda, documentacion

from django.contrib.auth.models import User

from system.models import DB_global, DB_rasgos, DB_grupos, DB_objetos, DB_objetos_rasgos, DB_rasgo_dominio

import json


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, index)

    def test_ayuda_url_is_resolved(self):
        url = reverse('ayuda')
        self.assertEquals(resolve(url).func, ayuda)

    def test_documentacion_url_is_resolved(self):
        url = reverse('documentacion')
        self.assertEquals(resolve(url).func, documentacion)

#Prueba unitaria
class DBglobal_TestCase(TestCase):
    def test_pruebaGlobal_is_resolved(self):
        modelo = DB_global()        
        modelo.nombre = 'paciente'
        modelo.criterio = '1'
        modelo.calculado = '1'
        modelo.umbral = '0.4'
        modelo.created = True
        modelo.save()

        exists = DB_global.objects.filter(nombre='paciente').exists()
        self.assertEquals(exists, True)

        modelo.nombre = 'sexo'
        modelo.save()
        yes_exists = DB_global.objects.filter(nombre='sexo').exists()
        self.assertEquals(yes_exists, True)

        modelo.delete()

        non_exists = DB_global.objects.filter(nombre='sexo').exists()
        self.assertEquals(non_exists, False)

    def test_pruebaRasgos_is_resolved(self):
        modelo = DB_global()        
        modelo.nombre = 'paciente'
        modelo.criterio = '1'
        modelo.calculado = '1'
        modelo.umbral = '0.4'
        modelo.created = True
        modelo.save()
        rasgos = DB_rasgos()
        rasgos.nombre = 'sexo'
        rasgos.criterio = '2'
        rasgos.db_global_id = modelo
        rasgos.save()

        exists = DB_rasgos.objects.filter(nombre='sexo').exists()
        self.assertEquals(exists, True)

        rasgos.nombre = 'tiempo'
        rasgos.save()
        yes_exists = DB_rasgos.objects.filter(nombre='tiempo').exists()
        self.assertEquals(yes_exists, True)

        rasgos.delete()
        non_exists = DB_rasgos.objects.filter(nombre='tiempo').exists()
        self.assertEquals(non_exists, False)
        