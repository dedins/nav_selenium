#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import csv
import os
import platform
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import datetime
import getpass
import re
import argparse

def month_converter(month):
	months = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic']
	months_complete = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
	if month in months:
		return months.index(month) + 1
	elif month in months_complete:
		return months_complete.index(month) +1
	else:
		pass

def error_screen(type):
	time.sleep(1)
	i = datetime.datetime.now()
	driver.save_screenshot('error_%s-%s-%s_%s:%s:%s.png' % (i.day, i.month, i.year, i.hour, i.minute, i.second))
	print '[-] '+col.split("|")[0]+'h - '+header[colnum]+'/'+mese+'/'+anno+' - '+row[0]+' - KO   -->   '+str(type)+' - screenshot error_%s-%s-%s_%s:%s:%s.png' % (i.day, i.month, i.year, i.hour, i.minute, i.second)

def WeekendDay():
	time.sleep(2)
	try:
		Newlines()
	except Exception, e:
		error_screen("errore generico")
		GoBack()
		Newlines()
	try:
		Datafunc()
	except Exception, e:
		error_screen("inserimento data")
	try:
		fine = driver.find_element_by_id("hord")
		fine.clear()
		fine.send_keys(col.split("|")[0])
	except Exception, e:
		error_screen("inserimento ore")
	try:
		### EXPERIMENTAL
		try:
			Commentfunc()
		except Exception, e:
			pass		
		###################
		Commessa()
		Savefunc()
		print '[+] %sh - %s/%s/%s - %s - OK' % (col.split("|")[0], header[colnum],mese,anno, row[0])
	except Exception, e:
		error_screen("commessa %s non trovata" % (row[0]))
		GoBack()

def Newlines():
	time.sleep(1)
	newline = driver.find_element_by_id("listaRigheOdT_btnNew")
	newline.click()

def Commessa():
	time.sleep(1)
	findcom = driver.find_element_by_id("btnRicercaCommessa")
	findcom.click()
	time.sleep(1)
	searchcom = driver.find_element_by_id("searchCodCommessa")
	searchcom.send_keys(row[0].split('-')[0])
	searchfase = driver.find_element_by_id("searchFase")
	searchfase.send_keys(row[0].split('-')[1])
	filtro = driver.find_element_by_id("listaCommesse_btnFiltra")
	filtro.click()
	time.sleep(1)
	# trova id con regex
	src = driver.page_source
	p = re.compile(ur'(?s)(?<="listaCommesse_Key">).*?(?=</td><td role="gridcell")')
	id_commessa = re.search(p, src).group()
	selectcom = driver.find_element_by_id(id_commessa)
	selectcom.click()
	time.sleep(1)

def Datafunc():
	time.sleep(1)
	selectdata = driver.find_element_by_id("Data")
	selectdata.clear()
	selectdata.send_keys(header[colnum]+'/'+mese+'/'+anno)
	km = driver.find_element_by_id("KmPercorsi")
	km.click()

def Savefunc():
	saveriga = driver.find_element_by_id("btnSalva")
	saveriga.click()
	time.sleep(1)

def GoBack():
	escape = driver.find_element_by_id('MainPanel')
	escape.send_keys(Keys.ESCAPE)
	goback = driver.find_element_by_id('btnBack')
	goback.click()
	
def Commentfunc():
	time.sleep(1)
	find_comment = driver.find_element_by_id("Note")
	find_comment.clear()
	find_comment.send_keys(col.split("|")[1])

# argparse
parser = argparse.ArgumentParser(description='input file csv')
parser.add_argument('-f','--file', help='nome file csv', required=True)
args = vars(parser.parse_args())

# avvio PhantomJS
sys =  platform.system()
FNULL = open(os.devnull, 'w')
#subprocess.call('./phantomjs --webdriver=4444 --ssl-protocol=any --ssl-ciphers=any --ignore-ssl-errors=true', shell=True)
if sys == 'Windows':
	try:
		subprocess.Popen('c:\\phantomjs.exe --webdriver=4444 --ssl-protocol=any --ssl-ciphers=any --ignore-ssl-errors=true', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
	except Exception, e:
		error_screen("phantomjs non trovato")
elif sys == 'Darwin':
	try:
		subprocess.Popen('phantomjs --webdriver=4444 --ssl-protocol=any --ssl-ciphers=any --ignore-ssl-errors=true', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
	except Exception, e:
		error_screen("phantomjs non trovato")

user_agent = (
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
	"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = user_agent

crm_host = raw_input("CRM Host:");
username = raw_input("Username:");
passphrase = getpass.getpass("Password:");

time.sleep(1)
try:
	driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.PHANTOMJS.copy())
	driver.set_window_size(1600, 900)
	print "------------------------------------------------"
	driver.get(crm_host)
except Exception, e:
	error_screen("phantomjs")
else:
	print "Apro Navision - "+driver.current_url
	print "------------------------------------------------" 

# login
try:
	login = driver.find_element_by_id("UserName")
	login.send_keys(username)
	password = driver.find_element_by_id("Password")
	password.send_keys(passphrase)
	password.send_keys(Keys.RETURN)
except Exception, e:
	error_screen("login non riuscito")

# Gestione consuntivazione
try:
	menu1 = driver.find_element_by_id("menu1")
	menu1.click()
except Exception, e:
	print "Errore menu"

# nuovo rapportino
time.sleep(1)
try:
	newrap = driver.find_element_by_id("listaOdT_btnNew")
	newrap.click()
except Exception, e:
	print "Errore rapportino"

# apro csv
try:
	ifile  = open(args['file'], "rb")
	reader = csv.reader(ifile, delimiter=',')
except Exception, e:
	print "[-] File csv non trovato"
	print "Metti consuntivazione.csv in questa cartella"
else:
	rownum = 0
	for row in reader:
		# Save header row.
		if rownum == 0:
			header = row
			## DEBUG
			#print header
			#####################
			mese_raw = header[1]
			mese = str(month_converter(mese_raw.lower()))
			anno = header[0]
		else:
			colnum = 0
			for col in row:
				## DEBUG 
				#print col
				################
				try:
					if col[0].isdigit() is True or col[0] == "-":
						WeekendDay()
					colnum += 1
				except Exception, e:
					pass
		rownum += 1
	ifile.close()
	print "-------------------------------"
	print "Fatto!"
