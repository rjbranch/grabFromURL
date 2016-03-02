__author__ = 'Ryan'
import urllib2
from cStringIO import StringIO
import re
import sys
import os
import errno
import csv

class Site:
	#Default constructor
	def __init__(self):
		self.name = ""
		self.term = ""
		self.url = ""
		self.page = 0
		self.links = []

	#Constructor Method
	def __init__(self, term_, url_, page_):
		self.name = ""
		self.term = term_
		self.url = url_
		self.page = page_
		self.links = []

	#Set function for name
	def setName(self, nameIn):
		self.name = nameIn

	#Get function for name
	def getName(self):
		return self.name

	#Set function for term
	def setTerm(self, termIn):
		self.term = termIn

	#Get function for term
	def getTerm(self):
		return self.term

	#Set function for url
	def setUrl(self, urlIn):
		self.url = urlIn

	#Get function for url
	def getUrl(self):
		return self.url

	#Set function for page
	def setPage(self, numIn):
		self.page = numIn

	#Get function for page
	def getPage(self):
		return self.page

	#Function to add a string to the end of "links"
	def addLink(self, linkIn):
		self.links.append(linkIn)

	#Function to return the link at a given index of "links"
	def getLink(self, index):
		return self.links[index]

	#Function to return the entire "links" list
	def getLinks(self):
		return self.links

class Container:
	#Default constructor
	def __init__(self):
		self.fileName = "default.txt"
		self.folderName = "default_txt"
		self.searchTerms = []
		self.sites = []
		self.extensions = []
		self.rowNum = 0
		self.numPages = 1

	#Makes tree of directories to store results
	def makeFolders(self):
		for term in self.searchTerms:
			for i in range(self.numPages):
				try:
					os.makedirs(self.folderName + "/" + term + "/" + str(i + 1))
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

	#Function to add a Site to the end of "sites"
	def addSite(self, siteIn):
		self.sites.append(siteIn)

	#Function to return the Site at a given index of "sites"
	def getSite(self, index):
		return self.sites[index]

	#Function to return the entire "sites" list
	def getSites(self):
		return self.sites

	#Function to add a string to the end of "extensions"
	def addExtension(self, extensionIn):
		self.extensions.append(extensionIn)

	#Function to return the extension at a given index of "extensions"
	def getExtension(self, index):
		return self.extensions[index]

	#Function to return the entire "extensions" list
	def getExtensions(self):
		return self.extensions

	#Set function for rowNum
	def setRowNum(self, numIn):
		self.rowNum = numIn

	#Get function for rowNum
	def getRowNum(self):
		return self.rowNum

	#Set function for numPages
	def setNumPages(self, numIn):
		self.numPages = numIn

	#Get function for numPages
	def getNumPages(self):
		return self.numPages

def buildLinks(sit, exts):
	url = sit.getUrl()
	try:
		response = urllib2.urlopen(url)
	except:
		print('Cannot read HTML: ' + url)
		return False
	html = response.read()
	content = StringIO(html)
	for line in content:
		for ext in exts:
			if ext in line:
				try:
					link = re.search("href=\"(.+?)" + ext + "\"", line).group(1)
					if ">" not in link:
						link = url + link + ext
						sit.addLink(link)
					break
				except:
					#This often occurs if a link is preceded by an icon,
					#for example "sound2.gif" preceding a .mp3 file.
					pass

def checkUrl(url):
	title = ""

	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
		response = opener.open(url)
	except:
		print('Cannot parse HTML: ' + url)
		return title

	html = response.read()
	content = StringIO(html)
	for line in content:
		if "<title>Index of " in line:
			try:
				title = re.search("<title>Index of (.+?)</title>", line).group(1)
				break
			except:
				#This can occur if the HTML of the page is formatted strangely,
				#for example if the title is spread throughout multiple lines
				pass
	return title

def fileInput(cont):
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
	cont.makeFolders()

def parseGoogle(cont, searchTerm, index):
	url = getSearchURL(searchTerm, index)

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
			cont.addSite(Site(searchTerm, link, index))

def buildURLs(cont):
	for phrase in cont.getSearchTerms():
		for i in range(cont.getNumPages()):
			parseGoogle(cont, phrase, i)

def makeFilename(nameIn):
	nameOut = ""
	for char in nameIn:
		if char in "\\/:*?\"<>|":
			nameOut += "-"
		else:
			nameOut += char
	return nameOut

def getSearchURL(term, pageNum):
	tempName = ""
	for char in term:
		if (char == ' '):
			tempName += "+"
		else:
			tempName += char
	return "https://www.google.com/search?q=" + tempName + "&start=" + str((pageNum - 1) * 10)

def download(cont):
	for site in cont.getSites():
		for link in site.getLinks():
			path = cont.getFolderName() + "/" + site.getTerm() + "/" + str(site.getPage() + 1)
			if site.getName()[0] != "/":
				path = path + "/"
			path = path +  site.getName()
			try:
				os.makedirs(path)
			except OSError as exception:
				if exception.errno != errno.EEXIST:
					raise
			try:
				f = urllib2.urlopen(link)
				print("Downloading " + link)
				path = path + "/" + os.path.basename(link)
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

	for site in container.getSites():
		directoryName = checkUrl(site.getUrl())
		if(directoryName != ""):
			site.setName(directoryName)
			print("DIRECTORY NAME: " + directoryName)
			successes.append(True)
		else:
			successes.append(False)

	index = 0
	for val in successes:
		if val:
			buildLinks(container.getSites()[index], container.getExtensions())
		index += 1

	download(container)

main()