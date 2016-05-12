#/usr/local/Cellar/python3
#-*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
from lxml import etree
import shutil
import os
from subprocess import call
import sys


review = {'id': None, 'title': None, 'creator': None, 'date': None, 'content': None}
#Para una futura versión, otra variable para coger también los datos del hotel si fuera necesario
env = Environment(loader=FileSystemLoader(os.getcwd() + '/templates'), trim_blocks=True, lstrip_blocks=True)

#archivoXMI es la ruta donde haya un archivo XMI
def saveReviewData(archivoXMI):
	xmiFile = str(archivoXMI)
	xmiName = xmiFile.split('/')[len(xmiFile.split('/'))-1]
	review['id'] = (xmiName.split('_')[1]+'_'+xmiName.split('_')[2]+xmiName.split('_')[3]).split('.')[0]
	tree = etree.parse(xmiFile)
	root = tree.getroot()
	#Parseamos toda la información del xml y lo metemos en el diccionario review
	review['creator'] = root.find("{http:///de/aitools/ie/uima/type/arguana.ecore}RatingData").get('author')
	review['date'] = root.find("{http:///de/aitools/ie/uima/type/arguana.ecore}RatingData").get('date')
	try:
		content = root.find("{http:///uima/cas.ecore}Sofa").get("sofaString").split('\n\n')[1]
		content2 = content.replace("\"","\'")
		review['content'] = content2
	except:
		print("REVIEW SIN TÍTULO 1/2") #Comprobar si da error y cuantas veces
		review['content'] = root.find("{http:///uima/cas.ecore}Sofa").get("sofaString")
		review['title'] = ""
		return
	title = (root.find("{http:///uima/cas.ecore}Sofa").get("sofaString").split('\n\n')[0]).replace("\"","\'")
	review['title'] = title



def saveOpinionsData(archivoXMI):
	opinions = []
	xmiFile = str(archivoXMI)
	xmiName = xmiFile.split('/')[len(xmiFile.split('/')) - 1]
	tree = etree.parse(xmiFile)
	root = tree.getroot()
	i = 1
	for element in root.findall("{http:///de/aitools/ie/uima/type/arguana.ecore}Opinion"):
		#Para una futura versión, cambiar a una lista vacia dentro de el feature y luego ir añadiendo objetos:
		#opinion = {'id': None, 'polarity': None, 'feature': [],'text': {'beginIndex': None, 'endIndex': None}}
		opinion = {'id': None, 'polarity': None, 'feature': {'beginIndex': None, 'endIndex': None},
				   'text': {'beginIndex': None, 'endIndex': None}}
		opinion['polarity']=element.get('polarity')
		opinion['text']['beginIndex'] = element.get('begin')
		opinion['text']['endIndex'] = element.get('end')
		for element in root.findall("{http:///de/aitools/ie/uima/type/arguana.ecore}ProductFeature"):
			if (int(element.get('begin')) >= int(opinion['text']['beginIndex'])) and (int(element.get('end')) <= int(opinion['text']['endIndex'])):
				if opinion['feature']['beginIndex'] == None:
					opinion['feature']['beginIndex'] = element.get('begin')
					opinion['feature']['endIndex'] = element.get('end')

			elif int(element.get('begin')) < int(opinion['text']['beginIndex']):
				opinion2 = {'id': None, 'polarity': None, 'feature': {'beginIndex': None, 'endIndex': None},'text': {'beginIndex': None, 'endIndex': None}}
				opinion2['feature']['beginIndex'] = element.get('begin')
				opinion2['feature']['endIndex'] = element.get('end')
				#Recorre array opinions por si ya se ha metido esa feature antes
				flag = 0
				for element in opinions:
					if opinion2['feature']['beginIndex'] ==  element['feature']['beginIndex']:
						flag = 1
				if flag != 1:
					opinion2['id'] = review['id'] + "_" + str(i) 
					opinions.append(opinion2)
					i += 1

		opinion['id'] = review['id'] + "_" + str(i) #importante cambiar review despues para ordenar las opinions.
		opinions.append(opinion)
		i += 1
	return opinions
	#Pone ids que faltan a las opinions(las que estan vacias con solo una feature sin opinion.text)
	#for element in opinions:
		#if element['id'] == None:
		#	element['id'] = review['id']+"_"+str(opinions.index(element)+1)
	#print(opinions)

def fillTemplates(opinions, noComma):

	post_template = env.get_template('post_template.jsonld')
	file.write(post_template.render(opinions_= opinions, review_= review, noComma = noComma))

######## Empieza el programa del script ########
# Comprobamos que el usuario introduce algún parámetro


if len(sys.argv) == 2:
	command = sys.argv[1]
	parameter = ""
elif len(sys.argv) ==3:
	command = sys.argv[1]
	parameter = sys.argv[2]
else:
	print("Usage: \n extractData.py <command> [parameter] \n\n General Options: \n \t -h, --help \t\t Show help \n  \t -c,--convert \t\t Convert a list of documents belonging to a corpus into a corpus in JSON-LD format \n")
	print( "The parameter will be a arguana corpus in xmi")
	sys.exit()

#Procesamos el parametro introducido
if (command == "-h" or command == "--help") and (len(sys.argv) == 2):
	print("Usage: \n extractData.py <command> [parameter] \n General Options: \n -h, --help \t Show help \n -c,--convert \t Convert a list of documents belonging to a corpus into a corpus in JSON-LD format \n")
	sys.exit()

elif (command == "-c" or command == "--convert") and (len(sys.argv) == 3):
		#shutil.copy2(str(parameter), os.getcwd()+'/xmiFiles')

		dirlist = os.listdir(parameter)
		filelist = []
		for element in dirlist:
			if os.path.isdir(os.path.abspath(parameter+element)):
				filelist.append(os.listdir(os.path.abspath(parameter+element)))
				print(os.listdir(os.path.abspath(parameter+element)))
		i = 1

		file = open(os.getcwd() + "/corpus.jsonld", "w")
		base_template = env.get_template('base_template.jsonld')
		file.write(base_template.render())
		for xmiFiles in filelist:
			for xmi in xmiFiles:
				if(xmi.split('.')[1] == "xmi"):
					xmiPath = parameter+dirlist[i]+"/"+xmi
					#Para conseguir quitar la coma en el último xml
					noComma = False
					if xmiFiles == filelist[-1]:
						if xmi == xmiFiles[-1]:
							noComma = True
					#Abrimos, rellenamos plantilla y vamos saliendo
					print(xmiPath)
					saveReviewData(xmiPath)
					fillTemplates(saveOpinionsData(xmiPath), noComma)

			i+= 1
		bottom_template = env.get_template('bottom_template.jsonld')
		file.write(bottom_template.render())
		file.close()

else:
	print("Introduce un parámetro y argumento válidos")