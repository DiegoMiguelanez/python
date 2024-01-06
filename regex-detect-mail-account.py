#!/usr/bin/python3
import re


pattern = re.compile("^[a-zA-Z0-9\.\-\_]+@{1}[a-zA-Z0-9]+\.{1}[a-zA-Z]{2,3}$")

#Comprobar si es correo

print(pattern.search("prueba@gmail.com"))
print(pattern.search("prueba.mail@drok3.es"))
print(pattern.search("pru-eba@gma22il.com"))
print(pattern.search("prue_ba@gmail.co"))