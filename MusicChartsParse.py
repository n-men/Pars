#-*- coding: utf-8 -*-


def main():
	Charts = CollectCharts()

	
def CollectCharts():
	Charts =[]
	
	Charts.append([0,'Muzofon',muzofon()])
	
	top = TopParse('https://play.google.com/store/music/collection/topselling_paid_track', 
					[['div','class','details'],
					['a','class','subtitle'],
					['a','class','title']],
					LineBegin=5, LineEnd=-2)
	Charts.append([1,'GooglePlay',top])
	
	top = TopParse('http://www.shazam.com/ru/charts/top-100/russia', 
					[['div','class','ti__details'],
					['p','class','ti__artist'],
					['p','class','ti__title']],
					Headers=True)
	Charts.append([2,'Shazam',top])
	
	top = TopParse('http://www.deezer.com/playlist/1116189381', 
					[['tr','class','song'],
					['td','class','artist'],
					['td','class','track']])
	Charts.append([3,'Deezer',top])
	
	top = TopParse('http://zaycev.net/', 
					[['div','class','musicset-track__title'],
					['div','class','musicset-track__artist'],
					['div','class','musicset-track__track-name']])
	Charts.append([4,'Zaycev.net',top])
	
	top = TopParse('https://zvooq.com/playlist/1062105/', 
					[['span','class','track-name'],
					['span','class','track-artist'],
					['span','class','track-title']])
	Charts.append([5,'Zvooq',top])
	
	
	print(u'\nСобраны ТОП-ы ресурсов: Ресурс - Количество треков')
	for chart in Charts: print (chart[1]+' - '+str(len(chart[2])))
	
	return Charts
	
def TopParse(UrlParse, TagArray, LineBegin=0, LineEnd=0, Headers=False):	# парсим страницу ресурса, выбираем названиz исполнителя и трека
	
	page = PageParse(Url=UrlParse, PageHeaders=Headers)
	TOP = []
															# выбираем элементы, содержащие названия исполнителя и трека
	for track in page.body.find_all(TagArray[0][0], attrs={TagArray[0][1]:TagArray[0][2]}):
	
		artist = GetString(track, TagArray[1])				# определяем название исполнителя									
															# определяем название трека
		track_name = GetString(track, TagArray[2], LineB=LineBegin, LineE=LineEnd)
		TOP.append([artist,track_name])

	return TOP

def GetString(TagLine, TagParam, LineB=0, LineE=0):	# выбираем и преобразуем текст по тэгам
		
	TagText = TagLine.find(TagParam[0], attrs={TagParam[1]:TagParam[2]})
	TagText = TagText.get_text()

														# убираем номера/тире перед/после названия трека
	if LineB>0: TagText = TagText[LineB:]	
	if LineE>0: TagText = TagText[:LineE]
	
	TagText = TagText.strip()							# удаляем пробельные символы в начале и конце строки
	TagText = translit(TagText)							# переводим транслитом
	
	return TagText

def PageParse(Url,PageHeaders):
	import urllib2
	from bs4 import BeautifulSoup
	
	if PageHeaders == True:
		import requests
		req = urllib2.Request(url)
		req.add_header("User-Agent", "Mozilla/5.0")
		source = urllib2.urlopen(req)
	else:
		source = urllib2.urlopen(Url)

	html =  source.read()
	soup = BeautifulSoup(html, "html.parser")

	return soup

def translit(input):								# translit+lower
	from trans import trans
	translited = trans(input)
	return translited.lower()


def muzofon():
	page = PageParse(Url='http://muzofon.com/',PageHeaders=False)
	TOP = []

	for img_tag in page.find_all('img'):		# для картинок сделали аналогиченый тэг a с классом tracktop
		a_tag = img_tag.parent
		a_tag.decompose()

	for track in page.body.find_all('a', attrs={'class':'tracktop'}):
		artist = track.find('strong').get_text() # название исполнителя выделено жирным
		artist = translit(artist)
		
		track.find('strong').decompose()
		
		track_name = track.get_text()
		track_name = track_name.strip()		# убираем пустые строки
		track_name = track_name[2:]			# убираем тире перед названием трека
		track_name = translit(track_name)
		
		TOP.append([artist,track_name])

	return TOP

	
if __name__ == "__main__":
	main()
	
	
	
	
	
	
	
	
