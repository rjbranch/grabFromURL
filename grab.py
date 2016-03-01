__author__ = 'Ryan'
import urllib2
from cStringIO import StringIO
import re
import sys
import os
import errno
import csv

class Container:
	#Default constructor
	def __init__(self):
		self.fileName = "default.txt"
		self.folderName = "default_txt"
		self.searchTerms = []
		self.urls = []
		self.extensions = []
		self.links = []
		self.rowNum = 0

	#Makes a directory with the name folderName, if one doesn't already exist
	def makeFolder(self):
		try:
			os.makedirs(self.folderName)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	#Set function for fileName
	def setFileName(self, nameIn):
		self.fileName = nameIn

	#Get function for fileName
	def getFileName(self):
		return self.fileName

	#Set function for folderName
	def setFolderName(self, nameIn):
		self.folderName = nameIn

	#Get function for folderName
	def getFolderName(self):
		return self.folderName

	#Function to add a string to the end of "searchTerms"
	def addSearchTerm(self, termIn):
		self.searchTerms.append(termIn)

	#Function to return the search term at a given index of "searchTerms"
	def getSearchTerm(self, index):
		return self.searchTerms[index]

	#Function to return the entire "searchTerms" list
	def getSearchTerms(self):
		return self.searchTerms

	#Function to add a string to the end of "urls"
	def addUrl(self, urlIn):
		self.urls.append(urlIn)

	#Function to return the url at a given index of "urls"
	def getUrl(self, index):
		return self.urls[index]

	#Function to return the entire "urls" list
	def getUrls(self):
		return self.urls

	#Function to add a string to the end of "extensions"
	def addExtension(self, extensionIn):
		self.extensions.append(extensionIn)

	#Function to return the extension at a given index of "extensions"
	def getExtension(self, index):
		return self.extensions[index]

	#Function to return the entire "extensions" list
	def getExtensions(self):
		return self.extensions

	#Function to add a string to the end of "links"
	def addLink(self, linkIn):
		self.links.append(linkIn)

	#Function to return the link at a given index of "links"
	def getLink(self, index):
		return self.links[index]

	#Function to return the entire "links" list
	def getLinks(self):
		return self.links

	#Set function for rowNum
	def setRowNum(self, numIn):
		self.rowNum = numIn

	#Get function for rowNum
	def getRowNum(self):
		return self.rowNum

def getLinks(cont, i):
	url = cont.getUrl(i)
	try:
		response = urllib2.urlopen(url)
	except:
		print('Cannot read HTML: ' + url)
		return False
	html = response.read()
	content = StringIO(html)
	for line in content:
		for ext in cont.getExtensions():
			if ext in line:
				try:
					link = re.search("href=\"(.+?)" + ext + "\"", line).group(1)
					link = url + link + ext
					cont.addLink(link)
					break
				except:
					#This often occurs if a link is preceded by an icon,
					#for example "sound2.gif" preceding a .mp3 file.
					pass

def checkUrl(url):
	try:
		response = urllib2.urlopen(url)
	except:
		print("Cannot parse HTML: " + url)
		return False
	response = urllib2.urlopen(url)
	html = response.read()
	content = StringIO(html)
	for line in content:
		if "<title>Index of " in line:
			return True
	return False

def fileInput(cont):
	cont.makeFolder()
	data = open(cont.getFileName(), 'rb')
	reader = csv.reader(data)

	for row in reader:
		#Gets extension data
		if (cont.getRowNum() == 0):
			for col in row:
				cont.addExtension(col)
			cont.setRowNum(cont.getRowNum() + 1)
		#Gets search term data
		else:
			cont.addSearchTerm(row[0])

	#All objects are now read in
	data.close

def parseGoogle(cont, url):
	print("CANDIDATES:")
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
		response = opener.open(url)
	except:
		print('Cannot read Google Search HTML: ' + url)
		return False
	html = response.read()
	try:
		links = re.findall("href=\"http(.+?)\"", html)
	except:
		print("Could not retrieve links from search results page.")
	for link in links:
		if "google" not in link:
			link = "http" + link
			if (link[-1] != '/'):
				link = link + '/'
			print(link)
			cont.addUrl(link)

def buildURLs(cont):
	for phrase in cont.getSearchTerms():
		parseGoogle(cont, getSearchURL(phrase, 1))

def getSearchURL(term, pageNum):
	tempName = ""
	for char in term:
		if (char == ' '):
			tempName += "+"
		else:
			tempName += char
	return "https://www.google.com/search?q=" + tempName + "&start=" + str((pageNum - 1) * 10)

def download(cont):
	for link in cont.getLinks():
		try:
			f = urllib2.urlopen(link)
			print("Downloading " + link)
			path = cont.getFolderName() + "/" + os.path.basename(link)
			with open(path, "wb") as file:
				file.write(f.read())
		except:
			print("ERROR: Could not download " + link)

def main():
	container = Container()
	container.setFileName
	if(len(sys.argv) == 2):
		container.setFileName(sys.argv[1])
		tempName = ""
		for char in sys.argv[1]:
			if (char == '.'):
				tempName += "_"
			else:
				tempName += char
		container.setFolderName(tempName)

	fileInput(container)
	buildURLs(container)

	successes = []
	for url in container.getUrls():
		if(checkUrl(url)):
			successes.append(True)
		else:
			successes.append(False)

	index = 0
	for val in successes:
		if val:
			getLinks(container, index)
		index += 1

	download(container)

main()