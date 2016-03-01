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

def getLinks(url, cont):
	try:
		response = urllib2.urlopen(url)
	except:
		print('Cannot read HTML: ' + url)
		return False
	response = urllib2.urlopen(url)
	html = response.read()
	content = StringIO(html)
	for line in content:
		for ext in cont.getExtensions():
			if ext in line:
				try:
					link = re.search("href=\"(.+?)\"", line).group(1)
					link = url + link
					print(link)
					cont.addLink(link)
				except:
					print("Could not find link with extension: " + ext + " in line " + line)


def checkUrl(url):
	try:
		response = urllib2.urlopen(url)
	except:
		print("Cannot read HTML: " + url)
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
		#Gets URL data
		else:
			cont.addUrl(row[0])

	#All objects are now read in
	data.close

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

	successes = []
	for url in container.getUrls():
		if(checkUrl(url)):
			successes.append(True)
		else:
			successes.append(False)

	index = 0
	for val in successes:
		if val:
			getLinks(container.getUrl(index), container)
		index += 1

	download(container)

main()