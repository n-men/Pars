#-*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import numpy as np
import os
import sys


def main():
	muzofon()
	gplay()
	yandex()
	shazam()
	deezer()
	zaycev()
	zvooq()
	
def muzofon():
	page = PageParse(url='http://muzofon.com/')
	TOP = []
	for track in page.body.find_all('a', attrs={'class':'track'}):
	
		artist = track.find('strong').get_text() # название исполнителя выделено жирным
		#artist = artist.encode(sys.stdout.encoding,  errors='ignore')
		artist = artist.encode('ascii', errors='ignore')
		
		#from transliterate import translit, get_available_language_codes
		#artist = translit(artist, 'ru')
		
		track.find('strong').decompose()
		
		track_name = track.get_text()
		track_name = track_name.encode(sys.stdout.encoding,  errors='ignore')
		track_name = track_name.strip()		# убираем пустые строки
		track_name = track_name[2:]			# убираем тире перед названием трека
		
		TOP.append([artist,track_name])

	return TOP
	
def gplay():
	page = PageParse(url='https://play.google.com/store/music/collection/topselling_paid_track')
	TOP = []
	
	for track in page.body.find_all('div', attrs={'class':'details'}):
	
		artist = track.find('a', attrs={'class':'subtitle'})
		artist = artist.get_text()

		track_name = track.find('a', attrs={'class':'title'})
		track_name = track_name.get_text()
		track_name = track_name[5:-2]			# убираем номер перед названием трека и пробелы до и после
	
		TOP.append([artist,track_name])

	return TOP

def yandex():
	page = PageParse(url='https://music.yandex.ru/genre/all/tracks')
	TOP = []
	
	for track in page.body.find_all('div', attrs={'class':'track__name-wrap'}):
	
		artist = track.find('div', attrs={'class':'track__artists nw'})
		artist = artist.get_text()

		track_name = track.find('a', attrs={'class':'track__title link'})
		track_name = track_name.get_text()
	
		TOP.append([artist,track_name])

	return TOP

def shazam():	# пришлось прописать заголовки
	page = ShazamPageParse(url='http://www.shazam.com/ru/charts/top-100/russia')
	TOP = []
	
	for track in page.body.find_all('div', attrs={'class':'ti__details'}):
	
		artist = track.find('p', attrs={'class':'ti__artist'})
		artist = artist.get_text()
		artist = artist.strip()		# убираем пустые строки

		track_name = track.find('p', attrs={'class':'ti__title'})
		track_name = track_name.get_text()
		track_name = track_name.strip()		# убираем пустые строки
		#track_name = track_name[5:-2]			# убираем номер перед названием трека и пробелы до и после
	
		TOP.append([artist,track_name])

	return TOP
	
def deezer():
	page = PageParse(url='http://www.deezer.com/playlist/1116189381')
	TOP = []
	
	for track in page.body.find_all('tr', attrs={'class':'song'}):
		
		artist = track.find('td', attrs={'class':'artist'})
		artist = artist.get_text()
		artist = artist.strip()		# убираем пустые строки
		
		track_name = track.find('td', attrs={'class':'track'})
		track_name = track_name.get_text()
		track_name = track_name.strip()		# убираем пустые строки
	
		TOP.append([artist,track_name])

	return TOP
	
def zaycev():
	page = PageParse(url='http://zaycev.net/')
	TOP = []
	
	for track in page.body.find_all('div', attrs={'class':'musicset-track__title'}):
		
		artist = track.find('div', attrs={'class':'musicset-track__artist'})
		artist = artist.get_text()
		
		track_name = track.find('div', attrs={'class':'musicset-track__track-name'})
		track_name = track_name.get_text()
	
		TOP.append([artist,track_name])

	return TOP
	
def zvooq():	# возвращает только первые 20 треков
	page = PageParse(url='http://zvooq.ru/playlist/2800526/')
	TOP = []
	
	for track in page.body.find_all('span', attrs={'class':'track-name'}):

		artist = track.find_all('span', attrs={'class':'track-artist'})
		artist = artist[0].get_text()

		track_name = track.find('span', attrs={'class':'track-title'})
		track_name = track_name.get_text()
	
		TOP.append([artist,track_name])

	return TOP

def PageParse(url):
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, "html.parser")
	return soup

def ShazamPageParse(url):
	import requests
	req = urllib2.Request(url)
	req.add_header("User-Agent", "Mozilla/5.0")
	source = urllib2.urlopen(req)
	html =  source.read()
	soup = BeautifulSoup(html, "html.parser")
	return soup

	
if __name__ == "__main__":
	main()
	
	
	
	
	
	
	
	